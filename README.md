# Async Task API

A minimal yet **production-grade** demonstration of **FastAPI** featuring fully-typed
asynchronous endpoints, a clean *hexagonal* (ports & adapters) architecture and
an on-disk **SQLite** database that is wiped automatically between runs.

---

## ✨ Features

* **Modern stack** – FastAPI, SQLAlchemy, Pydantic, Python 3.11 (type-checked & linted)
* **Hexagonal architecture** – clear separation of *domain*, *ports*, *adapters* and *use-cases*
* **Async HTTP layer** – non-blocking endpoints while re-using a synchronous SQLAlchemy repository
* **Ephemeral database** – data stored in a local `tasks.db` file that is *emptied on shutdown*
* **CRUD for `Task`** – create • list • retrieve • delete
* **Comprehensive tests** – written with `pytest` & `httpx` in AAA-style
* **Self-contained demo client** – see `examples/async_client_demo.py`

---

## 🚀 Quick Start

```bash
# 1. (Optional) create & activate a virtual environment
python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate                           # Windows PowerShell

# 2. Install the dependencies
pip install -r requirements.txt

# 3. Run the development server (auto-reload enabled)
uvicorn app.main:app --reload
```

Navigate to <http://localhost:8000/docs> for the interactive Swagger UI 🚀

---

## 🗂 Project Structure

```
app/
    domain/        # Pure business entities (no frameworks!)
    ports/         # Abstract interfaces (e.g. `TaskRepository`)
    adapters/      # Infrastructure implementations (SQLite repository)
    usecases/      # Application services orchestrating the domain
    api/           # FastAPI routers, Pydantic schemas & dependencies
    main.py        # Application factory / bootstrap
examples/          # Async demo client
tests/             # AAA-style test-suite
```

---

## 🔌 HTTP API Overview

| Method | Path          | Description              | Status |
|--------|---------------|--------------------------|--------|
| POST   | `/tasks/`     | Create a new task        | 201    |
| GET    | `/tasks/`     | List all tasks           | 200    |
| GET    | `/tasks/{id}` | Retrieve a task by `id`  | 200/404|
| DELETE | `/tasks/{id}` | Delete a task by `id`    | 204/404|

> OpenAPI documentation is served automatically at `/docs` (Swagger UI) and `/redoc`.

---

## 🧱 Architecture in a Nutshell

```text
          ┌────────────┐        HTTP         ┌────────────────────┐
          │  FastAPI   │◀──────────────────▶│  async client / UI │
          └────────────┘                     └────────────────────┘
                │
                │  calls (async)                  Ports (abstract)
                ▼
          ┌────────────────┐         ┌──────────────────────────┐
          │  Use-cases     │◀──────▶│  TaskRepository (port)   │
          └────────────────┘         └──────────────────────────┘
                │                              ▲
                │ (sync)                       │ implements
                ▼                              │
          ┌────────────────┐                   │
          │    Domain      │                   │
          │   (Task)       │                   │
          └────────────────┘                   │
                │                              │
                │ (sync)                       │
                ▼                              │
          ┌──────────────────────────┐         │
          │  SQLiteTaskRepository    │─────────┘
          └──────────────────────────┘
```

*The outer world depends on the inner – never the other way round.*  This keeps
business logic framework-agnostic and trivially testable.

---

## 🧪 Running Tests

```bash
pytest -q
```

All tests should pass green ✅

---

## 🤖 Example: Concurrent Client

Before running the client, **start the API server in another terminal**:

```bash
uvicorn app.main:app --reload
```

A small script in `examples/async_client_demo.py` then spawns several concurrent
requests using `httpx` and the native `asyncio` event-loop:

```bash
python examples/async_client_demo.py
```

Feel free to play around and inspect the log output.

---

## 🙋 FAQ

**Why keep the DB synchronous?**  Simplicity.  SQLite lacks a mature async
driver.  A file-based database shared by threads combined with FastAPI’s
high-performance async layer is often plenty for demos, quick prototypes or
low-traffic apps.

**Is the project production-ready?**  Not entirely – consider migrations,
proper error handling, and containerisation.  Yet the foundation is solid and
serves as an excellent learning resource.

---

Made with ❤️  &  FastAPI 