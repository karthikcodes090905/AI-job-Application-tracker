import re

app = Flask(__name__)

def is_first_integer_odd(query: str) -> str:
    if not query:
        return "NO"
        
    # Match any number sequence: optional sign, digits, optional decimal part
    for match in re.finditer(r'[-+]?\d+(?:\.\d+)?', query):
        val = match.group()
        start, end = match.span()
        
        # EDGE CASE 1: Ignore numbers embedded inside words (e.g., "user123")
        # Check the character immediately before and after the match
        if start > 0 and query[start-1].isalpha():
            continue
        if end < len(query) and query[end].isalpha():
            continue
            
        # EDGE CASE 2 & 3: Ensure it is actually an integer, not a float.
        # `5.5` gets matched fully by the regex, so we just check if a '.' is inside it.
        if '.' not in val:
            # We found our first truly valid standalone integer!
            number = int(val)
            return "YES" if number % 2 != 0 else "NO"
            
    return "NO"

@app.route('/', methods=['POST'])
def check_odd():
    try:
        data = request.get_json(silent=True) or {}
        query = data.get('query', '')
        
        if not isinstance(query, str):
            return jsonify({"output": "NO"})
            
        output = is_first_integer_odd(query)
        return jsonify({"output": output})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
