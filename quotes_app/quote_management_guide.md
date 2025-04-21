# Quote Management Guide

This guide provides comprehensive instructions for installing, using, and maintaining the quotes application.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install Flask
   ```
4. Run the application:
   ```bash
   flask run
   ```

## Usage

### Viewing Quotes

- **Home Page**:
  - Visit the homepage to see a random quote
  - Use the category dropdown to filter quotes by category
  - Click "New Quote" to see another random quote from the selected category

- **All Quotes Page**:
  - Browse the complete collection with advanced filtering and sorting options
  - Use pagination controls to navigate through multiple pages of quotes
  - Adjust the number of quotes displayed per page (5, 10, 25, or 50)
  - Filter quotes by category using the dropdown menu
  - Sort quotes by date added, author name, or rating
  - Choose ascending or descending sort order

### Adding Quotes

1. Click the "Add Quote" button
2. Fill in the quote text (max 500 characters)
3. Add the author name (max 100 characters)
4. Select a category from the dropdown
5. Submit the form

### Rating Quotes

1. Navigate to the All Quotes page
2. Find the quote you want to rate
3. Click on a star (1-5) in the rating section to submit your rating
4. The average rating will update immediately

### Sharing Quotes

1. Find a quote you want to share
2. Click the "Share" button to reveal sharing options
3. Choose from:
   - Twitter: Share directly to Twitter
   - Facebook: Share to your Facebook timeline
   - Email: Send the quote via email
   - Copy to clipboard: Copy the quote text and author to paste elsewhere

## Data Storage

Quotes are stored in `quotes_collection.json` in the following format:
The data structure includes:
- `text`: The quote content
- `author`: The person who said or wrote the quote
- `category`: The thematic category of the quote
- `ratings`: (Optional) Array of all individual ratings
- `rating`: (Optional) Average rating calculated from all ratings

## API Documentation

The application provides a RESTful API for programmatic access to quotes.

### GET /api/quotes

Retrieve quotes with optional filtering parameters.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| category  | string | Filter quotes by category (case-insensitive) |
| author    | string | Filter quotes by author (case-insensitive, partial match) |
| random    | boolean | Set to 'true' to get a single random quote |
| limit     | integer | Maximum number of quotes to return |
| offset    | integer | Number of quotes to skip (for pagination) |

#### Examples

1. Get all quotes:
   ```
   GET /api/quotes
   ```

2. Get quotes in the "Funny" category:
   ```
   GET /api/quotes?category=funny
   ```

3. Get quotes by Albert Einstein:
   ```
   GET /api/quotes?author=einstein
   ```

4. Get a random quote from the "Tech" category:
   ```
   GET /api/quotes?category=tech&random=true
   ```

5. Pagination example (get 5 quotes, starting from the 10th):
   ```
   GET /api/quotes?limit=5&offset=10
   ```

### POST /api/rate_quote

Rate a quote on a scale of 1-5.

#### Request Body (JSON)

- `quote_id`: The ID of the quote to rate (integer)
- `rating`: Rating value from 1 to 5 (integer)

#### Response (JSON)

## Troubleshooting

### Common Issues

1. **Missing Quotes File**:
   - If `quotes_collection.json` is missing, the application will create a new empty quotes collection.
   - Add at least one quote to enable full functionality.

2. **JavaScript Not Loading**:
   - Ensure the `static/js/quotes.js` file is properly loaded.
   - Check the browser console for any JavaScript errors.

3. **Rating or Sharing Not Working**:
   - Verify that you're using a modern browser that supports the Fetch API and Clipboard API.
   - Ensure JavaScript is enabled in your browser.

## Best Practices

1. **Adding Quotes**:
   - Avoid duplicates by checking if a quote already exists
   - Keep quote text concise and focused
   - Use consistent capitalization for authors and categories

2. **Category Management**:
   - Use existing categories when possible for better organization
   - Create new categories only when needed
   - Use title case for category names (e.g., "Motivation", "Tech", "Wisdom")

3. **Development**:
   - Always back up the quotes collection before making changes
   - Test new features thoroughly, especially with large quote collections
   - Follow the existing code patterns when adding new functionality