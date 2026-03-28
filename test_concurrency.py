# test_concurrency.py  —  sends 5 concurrent requests using asyncio
import asyncio
import time

async def fetch(session_id: int, path: str):
    """Simulates one client making a request."""
    reader, writer = await asyncio.open_connection("localhost", 8080)

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:8080\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    writer.write(request.encode())
    await writer.drain()

    response = await reader.read(4096)
    first_line = response.decode().split("\r\n")[0]

    print(f"  [client {session_id}] {path} -> {first_line}")
    writer.close()
    await writer.wait_closed()

async def main():
    print("=== Sending 10 concurrent requests ===\n")
    start = time.time()

    # Mix of fast and slow requests — all fired at the same time
    tasks = [
        fetch(1,  "/slow"),     # 2 second DB simulation
        fetch(2,  "/"),         # instant
        fetch(3,  "/users"),    # instant
        fetch(4,  "/slow"),     # 2 second DB simulation
        fetch(5,  "/hello"),    # instant
        fetch(6,  "/"),         # instant
        fetch(7,  "/slow"),     # 2 second DB simulation
        fetch(8,  "/users"),    # instant
        fetch(9,  "/hello"),    # instant
        fetch(10, "/"),         # instant
    ]

    # asyncio.gather fires ALL tasks simultaneously
    await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"\n=== Done in {elapsed:.2f}s ===")
    print(f"(A sync server would have taken ~{3 * 2}s+ — one slow request blocks all others)")

if __name__ == "__main__":
    asyncio.run(main())