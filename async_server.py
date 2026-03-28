# async_server.py  —  Final: All phases integrated
import asyncio
from request import Request
from router import app
from middleware import build_stack

HOST = "localhost"
PORT = 8080

# Build the middleware stack once at startup
stack = build_stack()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")

    try:
        raw_data = await reader.read(4096)
        http_text = raw_data.decode("utf-8")
        req = Request(http_text)

        if req.method:
            print(f"\n[request] {req.method} {req.path} from {addr[0]}")
            # Request passes through the full middleware stack
            response = stack.process(req, app.resolve)
        else:
            response = "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n"

        writer.write(response.encode("utf-8"))
        await writer.drain()

    except Exception as e:
        print(f"  [error] {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"[*] Micro-Engine running on http://{addr[0]}:{addr[1]}")
    print(f"[*] Middleware stack: Timing → Logging → Auth → Router\n")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())