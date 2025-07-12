from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
import json

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['github_webhooks']
collection = db['events']

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook events"""
    try:
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        
        if event_type == 'push':
            handle_push_event(payload)
        elif event_type == 'pull_request':
            handle_pull_request_event(payload)
            
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': str(e)}), 500

def handle_push_event(payload):
    """Process push events"""
    author = payload['pusher']['name']
    branch = payload['ref'].split('/')[-1]
    timestamp = datetime.utcnow()
    
    event_data = {
    'REQUEST_ID': payload.get('after', '')[:8],
    'AUTHOR': author,
    'ACTION': 'push',
    'FROM_BRANCH': None,
    'TO_BRANCH': branch,
    'TIMESTAMP': timestamp.isoformat()
}

    
    collection.insert_one(event_data)
    print(f"Push event stored: {author} pushed to {branch}")

def handle_pull_request_event(payload):
    """Process pull request events"""
    action = payload['action']
    author = payload['pull_request']['user']['login']
    from_branch = payload['pull_request']['head']['ref']
    to_branch = payload['pull_request']['base']['ref']
    timestamp = datetime.utcnow()
    
    if action == 'opened':
        event_data = {
            'action_type': 'pull_request',
            'author': author,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp,
            'request_id': str(payload['pull_request']['id'])
        }
        collection.insert_one(event_data)
        print(f"PR event stored: {author} created PR from {from_branch} to {to_branch}")
        
    elif action == 'closed' and payload['pull_request']['merged']:
        event_data = {
            'action_type': 'merge',
            'author': author,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp,
            'request_id': str(payload['pull_request']['id'])
        }
        collection.insert_one(event_data)
        print(f"Merge event stored: {author} merged {from_branch} to {to_branch}")

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/clear')
def clear_events():
    """Clear all events for testing"""
    collection.delete_many({})
    return jsonify({'status': 'cleared'})

@app.route('/api/events')
def get_events():
    """API endpoint to fetch latest events"""
    try:
        events = list(collection.find().sort('timestamp', -1).limit(50))
        
        # Filter out events without valid action_type and format remaining events
        valid_events = []
        for event in events:
            if event.get('action_type') in ['push', 'pull_request', 'merge']:
                event['_id'] = str(event['_id'])
                event['formatted_timestamp'] = format_timestamp(event.get('timestamp'))
                event['display_text'] = format_event_display(event)
                valid_events.append(event)
            
        return jsonify(valid_events)
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': str(e)}), 500

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if timestamp is None:
        return 'Unknown time'
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return timestamp
    return timestamp.strftime('%d %B %Y - %I:%M %p UTC')

def format_event_display(event):
    """Format event for display"""
    author = event.get('author', 'Unknown')
    timestamp = event.get('formatted_timestamp', 'Unknown time')
    
    if event.get('action_type') == 'push':
        return f'"{author}" pushed to "{event.get("to_branch", "unknown")}" on {timestamp}'
    elif event.get('action_type') == 'pull_request':
        return f'"{author}" submitted a pull request from "{event.get("from_branch", "unknown")}" to "{event.get("to_branch", "unknown")}" on {timestamp}'
    elif event.get('action_type') == 'merge':
        return f'"{author}" merged branch "{event.get("from_branch", "unknown")}" to "{event.get("to_branch", "unknown")}" on {timestamp}'
    
    return f'Unknown event by {author} on {timestamp}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)