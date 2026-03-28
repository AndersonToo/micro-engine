# middleware.py  —  Phase 6: Middleware Stack + Context Manager
import time


# ─────────────────────────────────────────────
# Context Manager — measures request duration
# ─────────────────────────────────────────────

class RequestTimer:
    """
    Used with the 'with' statement:
        with RequestTimer() as timer:
            ... process request ...
        print(timer.elapsed)
    """
    def __enter__(self):
        self.start = time.perf_counter()
        return self                         # 'as timer' binds to this

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        # returning False means: don't suppress exceptions
        return False


# ─────────────────────────────────────────────
# Base Middleware class
# ─────────────────────────────────────────────

class BaseMiddleware:
    def __init__(self, next_handler):
        self.next = next_handler            # the next layer in the stack

    def process(self, request, resolve_fn):
        raise NotImplementedError


# ─────────────────────────────────────────────
# Timing Middleware
# ─────────────────────────────────────────────

class TimingMiddleware(BaseMiddleware):
    def process(self, request, resolve_fn):
        with RequestTimer() as timer:
            response = self.next.process(request, resolve_fn)
        print(f"  [timing] {request.method} {request.path} completed in {timer.elapsed * 1000:.2f}ms")
        return response


# ─────────────────────────────────────────────
# Logging Middleware
# ─────────────────────────────────────────────

class LoggingMiddleware(BaseMiddleware):
    def process(self, request, resolve_fn):
        print(f"  [logger] Incoming: {request.method} {request.path}")
        print(f"  [logger] User-Agent: {request.headers.get('User-Agent', 'unknown')[:40]}")
        response = self.next.process(request, resolve_fn)
        status = response.split(" ", 2)[1]  # pull status code from response string
        print(f"  [logger] Outgoing: HTTP {status}")
        return response


# ─────────────────────────────────────────────
# Auth Middleware
# ─────────────────────────────────────────────

class AuthMiddleware(BaseMiddleware):
    PROTECTED_PATHS = ["/admin", "/secret"]
    VALID_TOKEN = "micro-engine-secret-token"

    def process(self, request, resolve_fn):
        if request.path in self.PROTECTED_PATHS:
            token = request.headers.get("Authorization", "")
            if token != f"Bearer {self.VALID_TOKEN}":
                print(f"  [auth] BLOCKED {request.path} — invalid token")
                return (
                    "HTTP/1.1 401 Unauthorized\r\n"
                    "Content-Type: text/plain\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "401 - Unauthorized. Provide a valid Bearer token."
                )
            print(f"  [auth] PASSED {request.path}")
        return self.next.process(request, resolve_fn)


# ─────────────────────────────────────────────
# Final handler — calls the actual router
# ─────────────────────────────────────────────

class RouterHandler:
    def process(self, request, resolve_fn):
        return resolve_fn(request)          # calls app.resolve(request)


# ─────────────────────────────────────────────
# Middleware Stack builder
# ─────────────────────────────────────────────

def build_stack():
    """
    Builds the chain:
    TimingMiddleware → LoggingMiddleware → AuthMiddleware → RouterHandler

    Each layer wraps the next — like an onion.
    Request travels inward, response travels outward.
    """
    handler = RouterHandler()
    handler = AuthMiddleware(handler)
    handler = LoggingMiddleware(handler)
    handler = TimingMiddleware(handler)     # outermost — runs first
    return handler