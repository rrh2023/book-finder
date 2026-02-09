import json
import urllib.request
import urllib.parse

def lambda_handler(event, context):
    """
    AWS Lambda function to search for books using Google Books API
    WITH PROPER CORS HEADERS
    """
    
    # Define CORS headers to use in ALL responses
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS preflight request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        description = body.get('description', '')
        
        if not description:
            return {
                'statusCode': 400,
                'headers': cors_headers,  # ← CORS headers in error response
                'body': json.dumps({'error': 'Description is required'})
            }
        
        # Search Google Books API
        books = search_google_books(description)
        
        # ← THIS IS WHERE YOU ADD CORS HEADERS
        return {
            'statusCode': 200,
            'headers': cors_headers,  # ← CORS headers in success response
            'body': json.dumps({'books': books})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,  # ← CORS headers in exception response
            'body': json.dumps({'error': 'Internal server error'})
        }

def search_google_books(query, max_results=10):
    """
    Search for books using Google Books API
    """
    # Encode the query
    encoded_query = urllib.parse.quote(query)
    
    # Build the API URL
    url = f"https://www.googleapis.com/books/v1/volumes?q={encoded_query}&maxResults={max_results}"
    
    try:
        # Make the request
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        # Parse the results
        books = []
        items = data.get('items', [])
        
        for item in items:
            volume_info = item.get('volumeInfo', {})
            
            # Extract book information
            book = {
                'title': volume_info.get('title', 'Unknown Title'),
                'authors': ', '.join(volume_info.get('authors', [])),
                'description': truncate_description(volume_info.get('description', '')),
                'thumbnail': get_thumbnail(volume_info),
                'publishedDate': volume_info.get('publishedDate', ''),
                'pageCount': volume_info.get('pageCount'),
                'categories': ', '.join(volume_info.get('categories', []))
            }
            
            books.append(book)
        
        return books
        
    except Exception as e:
        print(f"Error searching books: {str(e)}")
        return []

def get_thumbnail(volume_info):
    """
    Get the best available thumbnail image
    """
    image_links = volume_info.get('imageLinks', {})
    
    # Prefer larger images
    return (
        image_links.get('thumbnail') or 
        image_links.get('smallThumbnail') or 
        None
    )

def truncate_description(description, max_length=300):
    """
    Truncate description to a reasonable length
    """
    if not description:
        return ''
    
    if len(description) <= max_length:
        return description
    
    # Find the last space before max_length
    truncated = description[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + '...'