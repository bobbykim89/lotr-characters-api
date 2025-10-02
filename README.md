# LOTR Characters API

## Overview

The LOTR Characters API is a RESTful API built with Django Rest Framework that uses Retrieval-Augmented Generation (RAG) to answer questions about characters from The Lord of the Rings universe. The API maintains conversation history and provides intelligent responses based on LOTR character information.

**Base URL:** `https://lotr-characters-api.vercel.app/`

**Version:** 1.0.0

---

## Technology Stack

- **Framework:** Django 5.2.6 with Django REST Framework 3.16.1
- **Database:** PostgreSQL (via psycopg 3.2.10)
- **Vector Database:** Qdrant 1.15.1
- **AI/ML:** OpenAI API 1.109.1
- **Python Version:** 3.x

---

## Authentication

Currently, this API does not require authentication. All endpoints are publicly accessible.

---

## Endpoints

### 1. Get or Create Conversation

Retrieves an existing conversation or creates a new one.

**Endpoint:** `GET /api/chat/conversations/`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | UUID | No | The unique identifier of an existing conversation |

**Response Codes:**

- `200 OK` - Successfully retrieved or created conversation
- `400 Bad Request` - Invalid conversation_id provided
- `404 Not Found` - Conversation with given ID does not exist

**Response Body:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "question": "Who is Gandalf?",
      "answer": "Gandalf is a wizard and one of the main characters...",
      "created_at": "2025-10-02T14:30:00Z"
    }
  ],
  "created_at": "2025-10-02T14:25:00Z"
}
```

**Example Requests:**

```bash
# Create a new conversation
curl -X GET "https://lotr-characters-api.vercel.app/api/chat/conversations/"

# Retrieve existing conversation
curl -X GET "https://lotr-characters-api.vercel.app/api/chat/conversations/?conversation_id=550e8400-e29b-41d4-a716-446655440000"
```

---

### 2. Send Message

Sends a question to the RAG pipeline, generates an AI response, and saves the message to the conversation.

**Endpoint:** `POST /api/chat/message/`

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What is the One Ring?"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | String (UUID) | Yes | The conversation ID to add the message to |
| `question` | String | Yes | The user's question about LOTR characters |

**Response Codes:**

- `200 OK` - Message successfully processed and saved
- `400 Bad Request` - Invalid request body or missing required fields
- `404 Not Found` - Conversation not found

**Response Body:**

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440002",
  "question": "What is the One Ring?",
  "answer": "The One Ring is a powerful artifact created by the Dark Lord Sauron...",
  "created_at": "2025-10-02T14:35:00Z"
}
```

**Example Request:**

```bash
curl -X POST "https://lotr-characters-api.vercel.app/api/chat/message/" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "question": "What is the One Ring?"
  }'
```

---

### 3. Get Message Log

Retrieves all messages in chronological order based on creation timestamp.

**Endpoint:** `GET /api/chat/message/log/`

**Query Parameters:** None

**Response Codes:**

- `200 OK` - Successfully retrieved message log

**Response Body:**

```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "question": "Who is Gandalf?",
    "answer": "Gandalf is a wizard and one of the main characters...",
    "created_at": "2025-10-02T14:30:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440002",
    "question": "What is the One Ring?",
    "answer": "The One Ring is a powerful artifact...",
    "created_at": "2025-10-02T14:35:00Z"
  }
]
```

**Example Request:**

```bash
curl -X GET "https://lotr-characters-api.vercel.app/api/chat/message/log/"
```

---

## Data Models

### Conversation Object

```json
{
  "id": "UUID (primary key)",
  "messages": "Array of Message objects",
  "created_at": "ISO 8601 datetime string"
}
```

### Message Object

```json
{
  "id": "UUID (primary key)",
  "question": "String - user's question",
  "answer": "String - AI-generated response",
  "created_at": "ISO 8601 datetime string"
}
```

---

## Error Handling

The API returns standard HTTP status codes and JSON error responses.

**Error Response Format:**

```json
{
  "error": "Error message describing what went wrong",
  "detail": "Additional details about the error (optional)"
}
```

**Common Error Codes:**

- `400 Bad Request` - Invalid request parameters or body
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

---

## Usage Examples

### Complete Workflow Example

```python
import requests
import json

BASE_URL = "https://lotr-characters-api.vercel.app"

# Step 1: Create a new conversation
response = requests.get(f"{BASE_URL}/api/chat/conversations/")
conversation = response.json()
conversation_id = conversation["id"]

print(f"Created conversation: {conversation_id}")

# Step 2: Ask a question
question_data = {
    "conversation_id": conversation_id,
    "question": "Tell me about Frodo Baggins"
}

response = requests.post(
    f"{BASE_URL}/api/chat/message/",
    headers={"Content-Type": "application/json"},
    data=json.dumps(question_data)
)

message = response.json()
print(f"Question: {message['question']}")
print(f"Answer: {message['answer']}")

# Step 3: Retrieve the conversation with all messages
response = requests.get(
    f"{BASE_URL}/api/chat/conversations/",
    params={"conversation_id": conversation_id}
)

full_conversation = response.json()
print(f"Total messages: {len(full_conversation['messages'])}")
```

### JavaScript/Fetch Example

```javascript
const BASE_URL = "https://lotr-characters-api.vercel.app";

async function chatWithAPI() {
  // Create new conversation
  const convResponse = await fetch(`${BASE_URL}/api/chat/conversations/`);
  const conversation = await convResponse.json();
  
  // Send a message
  const messageResponse = await fetch(`${BASE_URL}/api/chat/message/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      conversation_id: conversation.id,
      question: "Who is Aragorn?"
    })
  });
  
  const message = await messageResponse.json();
  console.log(`Answer: ${message.answer}`);
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. This may be added in future versions.

---

## Dependencies

The API is built using the following key dependencies:

- Django 5.2.6
- Django REST Framework 3.16.1
- OpenAI 1.109.1
- Qdrant Client 1.15.1
- PostgreSQL (psycopg 3.2.10)
- Python-dotenv 1.1.1

For a complete list of dependencies, refer to the requirements.txt file in the project repository.

---

## Support & Contact

For issues, questions, or contributions, please contact the development team or open an issue in the project repository.

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Conversation management
- RAG-based question answering
- Message logging functionality