# Tavus API Wrapper for Django

This Django application provides a comprehensive wrapper for the Tavus Conversational Video Interface (CVI) API, allowing you to create and manage AI-powered video conversations with replicas.

## Features

### Conversation Management
- **Create Conversation**: Start a new conversation with a replica
- **Get Conversation**: Retrieve details of a specific conversation
- **List Conversations**: Get all conversations
- **End Conversation**: Terminate a conversation
- **Delete Conversation**: Remove a conversation

### Replica Management
- **Create Replica**: Create a new AI replica
- **Get Replica**: Retrieve replica details
- **List Replicas**: Get all replicas
- **Delete Replica**: Remove a replica
- **Rename Replica**: Update replica name

### Persona Management
- **Create Persona**: Create a new persona for replicas
- **Get Persona**: Retrieve persona details
- **List Personas**: Get all personas
- **Update Persona**: Modify persona settings
- **Delete Persona**: Remove a persona

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Add your Tavus API key to `main/settings.py`:

```python
TAVUS_API_KEY = 'your-actual-tavus-api-key-here'
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start the Server

```bash
python manage.py runserver
```

## API Endpoints

All endpoints require authentication via the `X-API-TOKEN` header with the value configured in your constants.

### Conversations

- `POST /tavus-api-calls/conversations/` - Create a new conversation
- `GET /tavus-api-calls/conversations/list/` - List all conversations
- `GET /tavus-api-calls/conversations/{conversation_id}/` - Get conversation details
- `POST /tavus-api-calls/conversations/{conversation_id}/end/` - End a conversation
- `DELETE /tavus-api-calls/conversations/{conversation_id}/delete/` - Delete a conversation

### Replicas

- `POST /tavus-api-calls/replicas/` - Create a new replica
- `GET /tavus-api-calls/replicas/list/` - List all replicas
- `GET /tavus-api-calls/replicas/{replica_id}/` - Get replica details
- `DELETE /tavus-api-calls/replicas/{replica_id}/delete/` - Delete a replica
- `PATCH /tavus-api-calls/replicas/{replica_id}/rename/` - Rename a replica

### Personas

- `POST /tavus-api-calls/personas/` - Create a new persona
- `GET /tavus-api-calls/personas/list/` - List all personas
- `GET /tavus-api-calls/personas/{persona_id}/` - Get persona details
- `PATCH /tavus-api-calls/personas/{persona_id}/patch/` - Update a persona
- `DELETE /tavus-api-calls/personas/{persona_id}/delete/` - Delete a persona

## Usage Examples

### Creating a Conversation

```bash
curl -X POST http://localhost:8000/tavus-api-calls/conversations/ \
  -H "Content-Type: application/json" \
  -H "X-API-TOKEN: FOOBAR1" \
  -d '{
    "replica_id": "r79e1c033f",
    "persona_id": "p5317866",
    "conversation_name": "A Meeting with Hassaan",
    "conversational_context": "You are about to talk to Hassaan, one of the cofounders of Tavus.",
    "custom_greeting": "Hey there Hassaan, long time no see!",
    "properties": {
      "max_call_duration": 3600,
      "enable_recording": true,
      "enable_closed_captions": true
    }
  }'
```

### Listing Conversations

```bash
curl -X GET http://localhost:8000/tavus-api-calls/conversations/list/ \
  -H "X-API-TOKEN: FOOBAR1"
```

### Ending a Conversation

```bash
curl -X POST http://localhost:8000/tavus-api-calls/conversations/c123456/end/ \
  -H "X-API-TOKEN: FOOBAR1"
```

## Demo Interface

Visit `http://localhost:8000/tavus-api-calls/demo/` to access the interactive demo interface that allows you to test the API endpoints through a web interface.

## Request/Response Format

### Create Conversation Request

```json
{
  "replica_id": "r79e1c033f",
  "persona_id": "p5317866",
  "callback_url": "https://yourwebsite.com/webhook",
  "conversation_name": "A Meeting with Hassaan",
  "conversational_context": "You are about to talk to Hassaan...",
  "custom_greeting": "Hey there Hassaan, long time no see!",
  "properties": {
    "max_call_duration": 3600,
    "participant_left_timeout": 60,
    "participant_absent_timeout": 300,
    "enable_recording": true,
    "enable_closed_captions": true,
    "apply_greenscreen": true,
    "language": "english"
  }
}
```

### Create Conversation Response

```json
{
  "conversation_id": "c123456",
  "conversation_name": "A Meeting with Hassaan",
  "status": "active",
  "conversation_url": "https://tavus.daily.co/c123456",
  "replica_id": "r79e1c033f",
  "persona_id": "p5317866",
  "created_at": "2024-12-19T10:30:00Z"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

- `400 Bad Request` - Invalid request data or missing required fields
- `401 Unauthorized` - Invalid or missing API token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "error": "Error description"
}
```

## Configuration

The wrapper uses the following configuration:

- **API Base URL**: `https://tavusapi.com/v2`
- **Authentication**: API key via `x-api-key` header
- **Content Type**: `application/json`

## Security Notes

- Always keep your Tavus API key secure and never commit it to version control
- Use environment variables or Django's settings for sensitive configuration
- The demo interface includes the API token for testing - remove this in production

## Dependencies

- Django 5.1.3+
- requests
- Python 3.8+

## File Structure

```
tavus-api-calls/
├── tavus_client.py          # Core Tavus API client
├── views.py                 # Django views for API endpoints
├── urls.py                  # URL routing
├── templates/
│   └── tavus_demo.html     # Demo interface
└── README.md               # This file
```
