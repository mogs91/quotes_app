
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

- Visit the homepage to see a random quote
- Use the category dropdown to filter quotes by category
- Click "New Quote" to see another random quote from the selected category

### Adding Quotes

1. Click the "Add Quote" button
2. Fill in the quote text (max 500 characters)
3. Add the author name (max 100 characters)
4. Select a category from the dropdown
5. Submit the form

## Data Storage

Quotes are stored in `quotes_collection.json` in the following format:

```json
{
    "quotes": [
        {
            "text": "Quote text goes here",
            "author": "Author name",
            "category": "Category name"
        },
        ...
    ]
}
```