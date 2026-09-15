conversations = {}


def get_history(session_id):
    return conversations.get(session_id, [])


def add_message(session_id, role, message):
    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({
        "role": role,
        "message": message
    })
