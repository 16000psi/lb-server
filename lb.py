import asyncio

from aiohttp import ClientSession, web

PORT_LIST = [2000, 2001, 2002, 2003]
LAST_PORT = 3


def get_port():
    global PORT_LIST, LAST_PORT
    if LAST_PORT == 3:
        LAST_PORT = 0

    else:
        LAST_PORT = LAST_PORT + 1

    return PORT_LIST[LAST_PORT]


async def handle(request):
    path = request.path
    print(f"Received request at path: {path}")
    print(request.method, request.path, "HTTP/1.1")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    target_server_url = f"http://localhost:{get_port()}"
    target_url = f"{target_server_url}{path}"

    async with ClientSession() as session:
        async with session.get(target_url) as response:
            return web.Response(
                text=f"Received request at path: {path}\n{await response.text()}",
                status=response.status,
                headers=response.headers,
            )


async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 1999)
    await site.start()

    print("Server is listening on port 1999")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
