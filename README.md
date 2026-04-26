# Todo API Project

A simple but functional Todo application with FastAPI backend and HTML/jQuery frontend using MySQL database.

## Project Structure

```
faat api project/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database connection and initialization
│   ├── models.py         # Pydantic models for request/response validation
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Example environment variables
└── frontend/
    └── index.html        # Frontend UI with jQuery
```

## Setup Instructions

### 1. Database Setup

First, create the MySQL database:

```sql
CREATE DATABASE todo_db;
```

Or if you want to use a different database name, update the `.env` file accordingly.

### 2. Backend Setup

1. Navigate to the backend folder:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values according to your MySQL setup:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=todo_db
```

5. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API documentation will be at: `http://localhost:8000/docs`

### 3. Frontend Setup

1. Navigate to the frontend folder:
```bash
cd frontend
```

2. Open `index.html` in your web browser

Alternatively, you can use a simple HTTP server:
```bash
python -m http.server 8080
```

Then visit: `http://localhost:8080`

## API Endpoints

- **GET** `/api/todos` - Get all todos
- **POST** `/api/todos` - Create a new todo
- **GET** `/api/todos/{id}` - Get a specific todo
- **PUT** `/api/todos/{id}` - Update a todo
- **DELETE** `/api/todos/{id}` - Delete a todo

## Features

### Backend
- ✓ Complete CRUD operations
- ✓ MySQL database integration
- ✓ CORS enabled for frontend communication
- ✓ Error handling
- ✓ Automatic database initialization

### Frontend
- ✓ Add new todos
- ✓ View all todos
- ✓ Edit existing todos
- ✓ Delete todos
- ✓ Mark todos as completed/uncompleted
- ✓ Beautiful and responsive UI
- ✓ Real-time updates
- ✓ Error and success messages

## Database Schema

```sql
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Troubleshooting

### API Connection Error
- Make sure the FastAPI backend is running on `http://localhost:8000`
- Check that CORS is properly configured

### Database Connection Error
- Verify MySQL is running
- Check database credentials in `.env` file
- Ensure the database `todo_db` exists

### Port Already in Use
- Change the port in the uvicorn command:
  ```bash
  uvicorn main:app --reload --port 8001
  ```
- Update the `API_URL` in `index.html` to match the new port

## Future Enhancements

- User authentication and authorization
- Categories/tags for todos
- Due dates and reminders
- Todo priority levels
- Filtering and sorting options
- Dark mode
