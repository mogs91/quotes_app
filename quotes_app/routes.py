# quotes_app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json
import random
import os
from markupsafe import escape

# Create a Blueprint for organizing routes
main = Blueprint('main', __name__)

def load_quotes():
    """
    Load quotes from the JSON file.
    
    Returns:
        list: A list of quote dictionaries or an empty list if file not found
    """
    json_path = os.path.join(os.path.dirname(__file__), 'quotes_collection.json')
    try:
        with open(json_path, 'r') as file:
            return json.load(file)['quotes']
    except FileNotFoundError:
        # Return empty list if no quotes file exists yet
        return []

def save_quotes(quotes):
    """
    Save quotes to the JSON file.
    
    Args:
        quotes (list): List of quote dictionaries to save
    """
    json_path = os.path.join(os.path.dirname(__file__), 'quotes_collection.json')
    with open(json_path, 'w') as file:
        json.dump({'quotes': quotes}, file, indent=4)

def is_duplicate_quote(quotes, text, author):
    """
    Check if a quote with the same text and author already exists.
    
    Args:
        quotes (list): List of quote dictionaries
        text (str): Text of the quote to check
        author (str): Author of the quote to check
        
    Returns:
        bool: True if duplicate exists, False otherwise
    """
    return any(
        q['text'].lower().strip() == text.lower().strip() 
        and q['author'].lower().strip() == author.lower().strip() 
        for q in quotes
    )

def get_all_categories(quotes):
    """
    Extract all unique categories from the quotes collection.
    
    Args:
        quotes (list): List of quote dictionaries
        
    Returns:
        list: Sorted list of unique categories
    """
    categories = set()
    for quote in quotes:
        if 'category' in quote:
            categories.add(quote['category'])
    return sorted(list(categories))

@main.route("/")
def home():
    """
    Display the home page with a random quote, optionally filtered by category.
    
    URL Parameters:
        category (str, optional): Category to filter quotes by
        
    Returns:
        Rendered template with quote and category information
    """
    quotes = load_quotes()
    selected_category = request.args.get('category', 'all')
    
    # Get all available categories for the dropdown
    categories = get_all_categories(quotes)
    
    # Filter quotes by category if needed
    if selected_category != 'all' and quotes:
        filtered_quotes = [q for q in quotes if q.get('category') == selected_category]
        # If there are no quotes in this category, use all quotes
        if filtered_quotes:
            quotes = filtered_quotes
    
    if quotes:
        # Select a random quote from the filtered or complete list
        myquotes = random.choice(quotes)
    else:
        # Provide a default quote if no quotes are available
        myquotes = {
            "text": "No quotes available", 
            "author": "System", 
            "category": "None"
        }
    
    return render_template('index.html', 
                          myquotes=myquotes, 
                          categories=categories, 
                          selected_category=selected_category)

@main.route("/add", methods=["GET", "POST"])
def add_quote():
    """
    Handle the add quote page and form submission.
    
    GET: Display the form for adding a new quote
    POST: Process the submitted form, validate inputs, and save the new quote
    
    Returns:
        For GET: Rendered add_quote template
        For POST: Redirect to home page or back to form with error message
    """
    if request.method == 'POST':
        # Extract form data
        text = request.form.get('text', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', '').strip()
        
        # Validate required fields
        if not text or not author or not category:
            flash("Quote, author, and category are all required!", "error")
            return redirect(url_for('main.add_quote'))
            
        # Validate field lengths
        if len(text) > 500 or len(author) > 100:
            flash("Quote or author name is too long!", "error")
            return redirect(url_for('main.add_quote'))

        quotes = load_quotes()
        
        # Check for duplicate quotes
        if is_duplicate_quote(quotes, text, author):
            flash("This quote already exists!", "error")
            return redirect(url_for('main.add_quote'))

        # Escape the input to prevent XSS attacks
        safe_text = escape(text)
        safe_author = escape(author)
        safe_category = escape(category)
        
        # Add the new quote to the collection
        quotes.append({
            "text": safe_text, 
            "author": safe_author,
            "category": safe_category
        })
        
        # Save the updated quotes collection
        save_quotes(quotes)
        flash("Quote added successfully!", "success")
        return redirect(url_for('main.home'))

    # For GET requests, just render the form
    return render_template("add_quote.html")

@main.route("/api/quotes", methods=["GET"])
def api_quotes():
    """
    API endpoint to retrieve quotes with optional filtering parameters.
    
    Query Parameters:
        category (str, optional): Filter quotes by category
        author (str, optional): Filter quotes by author
        random (bool, optional): Return a single random quote if set to 'true'
        limit (int, optional): Limit the number of quotes returned (default: all)
        offset (int, optional): Number of quotes to skip (for pagination)
    
    Returns:
        JSON response with matching quotes and metadata
    """
    # Load quotes from JSON file
    quotes = load_quotes()
    
    # Extract query parameters
    category = request.args.get('category')
    author = request.args.get('author')
    random_quote = request.args.get('random', '').lower() == 'true'
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', 0, type=int)
    
    filtered_quotes = quotes
    
    # Apply category filter if specified
    if category:
        filtered_quotes = [q for q in filtered_quotes if q.get('category', '').lower() == category.lower()]
    
    # Apply author filter if specified
    if author:
        filtered_quotes = [q for q in filtered_quotes if author.lower() in q.get('author', '').lower()]
    
    # Get total count before applying pagination or random selection
    total_count = len(filtered_quotes)
    
    # Return a random quote if requested
    if random_quote:
        if filtered_quotes:
            return jsonify({
                'quote': random.choice(filtered_quotes),
                'status': 'success',
                'total_matching': total_count
            })
        else:
            return jsonify({
                'quote': None,
                'status': 'success',
                'total_matching': 0,
                'message': 'No matching quotes found'
            })
    
    # Apply pagination
    if offset > 0:
        filtered_quotes = filtered_quotes[offset:]
    
    if limit is not None:
        filtered_quotes = filtered_quotes[:limit]
    
    # Build response
    response = {
        'quotes': filtered_quotes,
        'status': 'success',
        'total_matching': total_count,
        'returned_count': len(filtered_quotes),
        'metadata': {
            'category_filter': category,
            'author_filter': author,
            'offset': offset,
            'limit': limit
        }
    }
    
    # Add pagination links if applicable
    if limit is not None:
        next_offset = offset + limit
        if next_offset < total_count:
            # Create the next page URL
            next_url = url_for('main.api_quotes', _external=True)
            params = []
            if category:
                params.append(f'category={category}')
            if author:
                params.append(f'author={author}')
            if limit:
                params.append(f'limit={limit}')
            params.append(f'offset={next_offset}')
            
            if params:
                next_url += '?' + '&'.join(params)
                
            response['links'] = {
                'next': next_url
            }
    
    return jsonify(response)

@main.route("/quotes")
def view_all_quotes():
    """
    Display all quotes with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Number of quotes per page (default: 10)
        category (str): Optional category filter
        sort (str): Sort by field (default: 'id', options: 'id', 'author', 'rating')
        order (str): Sort order (default: 'asc', options: 'asc', 'desc')
    
    Returns:
        Rendered template with paginated quotes
    """
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'id')
    sort_order = request.args.get('order', 'asc')
    
    # Limit per_page to reasonable values
    if per_page < 1:
        per_page = 1
    elif per_page > 50:
        per_page = 50
    
    # Load quotes
    quotes = load_quotes()
    
    # Filter by category if specified
    if category and category != 'all':
        quotes = [q for q in quotes if q.get('category', '').lower() == category.lower()]
    
    # Get all available categories for the dropdown
    categories = get_all_categories(quotes)
    
    # Add index to quotes for sorting by id
    for i, quote in enumerate(quotes):
        quote['id'] = i
    
    # Sort quotes
    reverse = sort_order.lower() == 'desc'
    if sort_by == 'author':
        quotes.sort(key=lambda q: q.get('author', '').lower(), reverse=reverse)
    elif sort_by == 'rating':
        quotes.sort(key=lambda q: q.get('rating', 0), reverse=reverse)
    else:  # Default sort by id
        quotes.sort(key=lambda q: q['id'], reverse=reverse)
    
    # Calculate pagination
    total_quotes = len(quotes)
    total_pages = (total_quotes + per_page - 1) // per_page
    
    # Ensure page is within bounds
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # Get quotes for current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_quotes)
    page_quotes = quotes[start_idx:end_idx]
    
    # Create pagination metadata
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_quotes': total_quotes,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
    }
    
    return render_template(
        'all_quotes.html',
        quotes=page_quotes,
        pagination=pagination,
        categories=categories,
        selected_category=category or 'all',
        sort_by=sort_by,
        sort_order=sort_order
    )

@main.route("/api/rate_quote", methods=["POST"])
def rate_quote():
    """
    API endpoint to rate a quote.
    
    JSON Payload:
        quote_id (int): ID of the quote to rate
        rating (int): Rating value (1-5)
    
    Returns:
        JSON response with success/error status
    """
    # Get quote ID and rating from request
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Missing JSON payload'
        }), 400
    
    quote_id = data.get('quote_id')
    rating = data.get('rating')
    
    # Validate input
    if quote_id is None:
        return jsonify({
            'status': 'error',
            'message': 'Missing quote ID'
        }), 400
    
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({
            'status': 'error',
            'message': 'Rating must be an integer between 1 and 5'
        }), 400
    
    # Load quotes
    quotes = load_quotes()
    
    # Check if quote ID is valid
    if quote_id < 0 or quote_id >= len(quotes):
        return jsonify({
            'status': 'error',
            'message': 'Invalid quote ID'
        }), 404
    
    # Update rating
    if 'ratings' not in quotes[quote_id]:
        quotes[quote_id]['ratings'] = []
    
    quotes[quote_id]['ratings'].append(rating)
    
    # Calculate average rating
    quotes[quote_id]['rating'] = round(sum(quotes[quote_id]['ratings']) / len(quotes[quote_id]['ratings']), 1)
    
    # Save quotes
    save_quotes(quotes)
    
    return jsonify({
        'status': 'success',
        'message': 'Rating saved successfully',
        'new_rating': quotes[quote_id]['rating']
    })