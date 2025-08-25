import sqlite3
from uuid import uuid4
DB_PATH = "task_data.db"



def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "priority": row[4],
            "status": row[5],
            "project_id": row[6],
        }
        for row in rows
    ]
def update_task(task_id, updates):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET title=?, description=?, due_date=?, priority=?, status=?, project_id=?
        WHERE id=?
    """, (
        updates.get("title"),
        updates.get("description"),
        updates.get("due_date"),
        updates.get("priority"),
        updates.get("status"),
        updates.get("project_id"),
        task_id
    ))
    conn.commit()
    conn.close()
    return { "id": task_id, **updates }

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return { "status": "deleted", "id": task_id }
