# Action Repository

This repository triggers webhooks on GitHub actions (Push, Pull Request, Merge).

## Setup Instructions

1. **Configure Webhook:**
   - Go to Settings > Webhooks in this repository
   - Add webhook URL: `https://your-webhook-endpoint.com/webhook`
   - Select events: Push, Pull requests
   - Content type: application/json

2. **Test Events:**
   - Push code to any branch
   - Create pull requests
   - Merge pull requests

## Webhook Events Monitored
- **Push**: Code pushed to any branch
- **Pull Request**: PR opened, closed, merged
- **Merge**: When PR is merged (detected via pull_request.merged = true)