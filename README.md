# Micro-Engine Web Framework

A functional, asynchronous web framework built from scratch using Python's standard library.
No Django. No Flask. No FastAPI. Just pure Python.

Built to understand the "under-the-hood" mechanics of modern backend development.

---

## Project Structure
```
micro-engine/
├── async_server.py     # Entry point — asyncio server
├── server.py           # Phase 1-3 sync reference server
├── request.py          # HTTP parser
├── router.py           # Routing engine with decorator syntax
├── middleware.py       # Middleware stack + context manager
├── orm.py              # Mini ORM with metaclasses + SQLite
├── test_orm.py         # ORM demo
├── test_concurrency.py # Concurrency demo
└── db.sqlite3          # Auto-created by ORM
```

---

## Phases & Concepts Covered

### Phase 1 — Raw Socket Server
- TCP socket server listening on `localhost:8080`
- Accepts raw byte streams and decodes them to strings
- **Concepts:** TCP handshakes, byte decoding, `socket` module

### Phase 2 — HTTP Protocol Parser
- `Request` class that parses raw HTTP strings
- Extracts method, path, HTTP version, headers, and body
- **Concepts:** HTTP anatomy, string manipulation, status codes

### Phase 3 — Routing Engine
- `Router` class with `@app.route(path, method)` decorator syntax
- Dictionary-based O(1) route lookup
- **Concepts:** Higher-order functions, first-class functions, decorators

### Phase 4 — Asyncio Concurrency
- Full async server using `asyncio.start_server`
- Handles multiple concurrent requests without blocking
- **Concepts:** Event loops, coroutines, `await`, WSGI vs ASGI

### Phase 5 — Mini ORM (Metaprogramming)
- `BaseModel` with a `ModelMeta` metaclass
- Field types: `TextField`, `IntegerField`, `RealField`
- `.save()` generates dynamic `INSERT INTO` SQL
- `.all()` and `.filter()` for querying
- **Concepts:** Metaclasses, `__new__`, reflection, SQLite

### Phase 6 — Middleware & Context Manager
- Chainable middleware stack: Timing → Logging → Auth → Router
- `RequestTimer` context manager measures request duration
- `AuthMiddleware` protects routes with Bearer token validation
- **Concepts:** Middleware pattern, `__enter__`/`__exit__`, context manager protocol

---

## How to Run

**Requirements:** Python 3.8+ — no external dependencies.

**Start the server:**
```bash
python async_server.py
```

**Test routes:**
```bash
curl http://localhost:8080/
curl http://localhost:8080/hello
curl http://localhost:8080/users
curl http://localhost:8080/nothing

# Protected route (401)
curl http://localhost:8080/admin

# Protected route (200)
curl http://localhost:8080/admin -H "Authorization: Bearer micro-engine-secret-token"

# POST request
curl -X POST http://localhost:8080/users -d "name=diana"
```

**Test the ORM:**
```bash
python test_orm.py
```

**Test concurrency (run while server is running):**
```bash
python test_concurrency.py
```

---

## Milestone Checklist

| Milestone | Deliverable | Status |
|-----------|-------------|--------|
| 1 | Raw socket server prints HTTP headers | ✅ |
| 2 | Async router with decorator syntax | ✅ |
| 3 | Python object saved to SQLite via `model.save()` | ✅ |
| 4 | 10 concurrent requests handled without blocking | ✅ |

---

## Key Insight

| This project | Real framework equivalent |
|---|---|
| `Router` + `@app.route` | Flask's `Blueprint`, FastAPI's `APIRouter` |
| `ModelMeta` metaclass | Django's `ModelBase` metaclass |
| `_fields` dictionary | Django's `_meta.fields` |
| `TimingMiddleware` | Django's `MIDDLEWARE` stack |
| `RequestTimer` | Python's `contextlib.contextmanager` |
| `asyncio.start_server` | Uvicorn's ASGI server core |

---

Built by Anderson Too — Micro-Engine Internship Project