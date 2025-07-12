# Webhook Repository

Flask application that receives GitHub webhooks and displays repository activity in real-time.

## Features

- Receives GitHub webhooks for Push, Pull Request, and Merge events
- Stores events in MongoDB with proper schema
- Real-time UI that polls every 15 seconds
- Clean, minimal design with event categorization
- Responsive design for mobile devices

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup MongoDB

Install MongoDB locally or use MongoDB Atlas:
```bash
# Local MongoDB (macOS)
brew install mongodb-community
brew services start mongodb-community

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MongoDB URI if different from default
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 5. Configure GitHub Webhook

1. Go to your action-repo Settings > Webhooks
2. Add webhook URL: `http://your-domain.com/webhook`
3. Select events: Push, Pull requests
4. Content type: application/json

## API Endpoints

- `POST /webhook` - Receives GitHub webhook events
- `GET /api/events` - Returns latest events as JSON
- `GET /` - Main UI dashboard

## MongoDB Schema

```javascript
{
  action_type: "push" | "pull_request" | "merge",
  author: "string",
  to_branch: "string",
  from_branch: "string" | null,
  timestamp: Date,
  request_id: "string"
}
```

## Event Formats

**Push**: `"{author}" pushed to "{to_branch}" on {timestamp}`

**Pull Request**: `"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}`

**Merge**: `"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}`

## Deployment

For production deployment, consider:
- Use a production WSGI server (gunicorn)
- Set up proper MongoDB authentication
- Use environment variables for sensitive data
- Set up HTTPS for webhook security