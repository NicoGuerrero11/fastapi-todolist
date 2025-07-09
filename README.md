# fastapi-todolist

# 📝 FastAPI Todo List API

A REST API to manage personal tasks, with user authentication via JWT. Each user can register, log in, and manage their own ToDos. Built with FastAPI, SQLModel, and PostgreSQL.

---

## 🚀 Features

- Registration and login with JWT (Access & Refresh tokens)
- CRUD of tasks (ToDo) associated with users
- Security with Bearer authentication
- Modularized by versions (`app/v1`)
- Connection to PostgreSQL database (using SQLModel)
- Environment variables managed with `pydantic-settings`

---

## 🧱 Project Structure

```
fastapi-todo-api/
├── main.py
├── .env
├── app/
│   └── v1/
│       ├── dependencies/       # Token validation
│       ├── model/              # SQLModel models (User, Todo)
│       ├── router/             # API routes
│       ├── schema/             # Input/output schemas (Pydantic)
│       ├── scripts/            # JWT, hashing, verification
│       ├── service/            # Business logic
│       └── utils/              # DB connection and settings
```

---

## ⚙️ Technologies

- **FastAPI** - Modern web framework
- **SQLModel** - ORM over SQLAlchemy + Pydantic
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT (python-jose)** - Access tokens
- **Passlib** - Password hashing
- **Uvicorn** - ASGI server

---

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-todo-api.git
cd fastapi-todo-api
```

2. Create a virtual environment and install:
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

3. Create your `.env` file (already included):
```
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=super_secret_key
```

4. Run the server:
```bash
uvicorn main:app --reload
```

---

## 🧪 Main Endpoints

### 🔐 Authentication

- `POST /api/auth/register` → User registration  
- `POST /api/auth/login` → Login and token delivery  
- `POST /api/auth/refresh` → Access token renewal  
- `GET /api/auth/me` → View logged-in user data  

### ✅ Todos

- `GET /api/todos` → View all user tasks  
- `POST /api/todos` → Create new task  
- `GET /api/todos/{todo_id}` → View a specific task  
- `PATCH /api/todos/{todo_id}` → Update a task  
- `DELETE /api/todos/{todo_id}` → Delete a task  

> All routes are protected by a JWT middleware.

---

## 🧩 Models

### User (`user_model.py`)
```python
class User(SQLModel, table=True):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    password: str
```

### Task (`todo_model.py`)
```python
class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    is_done: bool = False
    user_id: UUID = Field(foreign_key="user.uid")
```

---

## 🧠 Extras

- The authentication system clearly separates `access_token` and `refresh_token`.
- Easily extendable to add Redis as cache or Celery for asynchronous tasks.
- All errors are handled and return clear responses to the client.
- Integrated Redis (via `redis.asyncio`) to manage token blacklisting for logout testing purposes.

---

## ✨ Future Improvements

- Add tests with `pytest`
- Customized Swagger documentation
- Role system (admin/user)
- Notifications or reminders

---

## 🧑‍💻 Author

Developed by Nico 🚀  
Learning and applying FastAPI, SQLModel, and PostgreSQL with JWT authentication.