import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# ==========================
# Conversation Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(

id INTEGER PRIMARY KEY AUTOINCREMENT,

title TEXT

)
""")

# ==========================
# Messages Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(

id INTEGER PRIMARY KEY AUTOINCREMENT,

conversation_id INTEGER,

role TEXT,

message TEXT

)
""")

conn.commit()

# ==========================
# Create New Chat
# ==========================

def create_chat(title="New Chat"):

    cursor.execute(
        "INSERT INTO conversations(title) VALUES(?)",
        (title,)
    )

    conn.commit()

    return cursor.lastrowid


# ==========================
# Save Message
# ==========================

def save_message(conversation_id, role, message):

    cursor.execute(
        """
        INSERT INTO messages
        (conversation_id, role, message)
        VALUES (?, ?, ?)
        """,
        (conversation_id, role, message)
    )

    conn.commit()


# ==========================
# Load Messages
# ==========================

def load_messages(conversation_id):

    cursor.execute(
        """
        SELECT role, message
        FROM messages
        WHERE conversation_id=?
        ORDER BY id
        """,
        (conversation_id,)
    )

    return cursor.fetchall()


# ==========================
# All Chats
# ==========================

def get_all_chats():

    cursor.execute(
        """
        SELECT id, title
        FROM conversations
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()


# ==========================
# Delete Chat
# ==========================

def delete_chat(conversation_id):

    cursor.execute(
        "DELETE FROM messages WHERE conversation_id=?",
        (conversation_id,)
    )

    cursor.execute(
        "DELETE FROM conversations WHERE id=?",
        (conversation_id,)
    )

    conn.commit()