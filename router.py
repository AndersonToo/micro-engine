# router.py  —  Phase 3: Routing Engine

class Router:
    def __init__(self):
        # { (path, method): handler_function }
        self.routes = {}

    def route(self, path: str, method: str = "GET"):
        """Decorator factory — @app.route('/users', method='GET')"""
        def decorator(func):
            self.routes[(path, method.upper())] = func
            print(f"[router] Registered {method.upper()} {path} -> {func.__name__}()")
            return func
        return decorator

    def resolve(self, request):
        """Find and call the right handler for this request."""
        key = (request.path, request.method)
        handler = self.routes.get(key)

        if handler is None:
            return self._not_found()

        # Call the handler and get its return value
        body = handler(request)
        return self._build_response(200, body)

    def _build_response(self, status_code: int, body: str) -> str:
        status_text = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}
        return (
            f"HTTP/1.1 {status_code} {status_text.get(status_code, '')}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{body}"
        )

    def _not_found(self) -> str:
        return self._build_response(404, "404 - Route not found")


# --- Create the app instance (like Flask's app = Flask(__name__)) ---
app = Router()


# --- Define your routes ---
@app.route("/", method="GET")
def index(request):
    return "Welcome to Micro-Engine!"

@app.route("/hello", method="GET")
def hello(request):
    name = "World"
    return f"Hello, {name}!"

@app.route("/users", method="GET")
def get_users(request):
    # Simulating what a DB call would return
    users = ["alice", "bob", "charlie"]
    return f"Users: {', '.join(users)}"

@app.route("/users", method="POST")
def create_user(request):
    return f"Created user! Body received: '{request.body}'"
# add these to the bottom of router.py

@app.route("/admin", method="GET")
def admin(request):
    return "Welcome to the admin panel!"

@app.route("/secret", method="GET")
def secret(request):
    return "Top secret data!"