conversation_history = {}

def get_history(chat_id):
    return conversation_history.setdefault(chat_id, [])

def add_message(chat_id, role, content):
    history = get_history(chat_id)

    history.append(
        {
            "role": role,
            "content": content
        }
    )

    if len(history) > 10:
        history[:] = history[-10:]


