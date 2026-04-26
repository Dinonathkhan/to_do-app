from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection, init_db
from models import Todo, TodoCreate, TodoUpdate
from typing import List
import traceback

app = FastAPI(title="Todo API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message": "Todo API is running", "docs": "/docs"}

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# CREATE - Add a new todo
@app.post("/api/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = connection.cursor()
        query = "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s)"
        values = (todo.title, todo.description, todo.completed)
        
        cursor.execute(query, values)
        connection.commit()
        todo_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        # Fetch and return the created todo
        return get_todo_by_id(todo_id)
    except Exception as e:
        print(f"Error creating todo: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error creating todo")

# READ - Get all todos
@app.get("/api/todos", response_model=List[Todo])
def get_todos():
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM todos ORDER BY created_at DESC"
        cursor.execute(query)
        todos = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return todos
    except Exception as e:
        print(f"Error fetching todos: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error fetching todos")

# READ - Get a single todo by ID
@app.get("/api/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM todos WHERE id = %s"
        cursor.execute(query, (todo_id,))
        todo = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return todo
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching todo: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error fetching todo")

# UPDATE - Update a todo
@app.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = connection.cursor(dictionary=True)
        
        # Check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        existing_todo = cursor.fetchone()
        if existing_todo is None:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Build update query dynamically
        update_fields = []
        values = []
        
        if todo_update.title is not None:
            update_fields.append("title = %s")
            values.append(todo_update.title)
        if todo_update.description is not None:
            update_fields.append("description = %s")
            values.append(todo_update.description)
        if todo_update.completed is not None:
            update_fields.append("completed = %s")
            values.append(todo_update.completed)
        
        if not update_fields:
            cursor.close()
            connection.close()
            return existing_todo
        
        values.append(todo_id)
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = %s"
        
        cursor.execute(query, values)
        connection.commit()
        
        # Fetch updated todo
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        updated_todo = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating todo: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error updating todo")

# DELETE - Delete a todo
@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    try:
        connection = get_db_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = connection.cursor()
        
        # Check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        if cursor.fetchone() is None:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Delete the todo
        query = "DELETE FROM todos WHERE id = %s"
        cursor.execute(query, (todo_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {"message": "Todo deleted successfully", "id": todo_id}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting todo: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error deleting todo")

