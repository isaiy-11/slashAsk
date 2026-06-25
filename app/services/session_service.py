import redis
import json
import os

# Connect to Redis
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

# Time to Live for session (24 hours)
SESSION_TTL = 86400

def get_session(session_id):
    """Retrieves session history from Redis."""
    key = f"chat_history:{session_id}"
    history_json = redis_client.get(key)
    
    if history_json:
        return json.loads(history_json)
    return []

def add_message(session_id, role, content):
    """Appends a message to the session history in Redis."""
    key = f"chat_history:{session_id}"
    
    # Get current session
    session = get_session(session_id)
    
    # Append new message
    session.append({
        "role": role,
        "content": content
    })
    
    # Save back to Redis with TTL
    redis_client.setex(
        key,
        SESSION_TTL,
        json.dumps(session)
    )

def get_history(session_id):
    """Alias for get_session."""
    return get_session(session_id)