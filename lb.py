import asyncio

from aiohttp import ClientSession, web


async def handle(request):
    path = request.path
    print(f"Received request at path: {path}")
    print(request.method, request.path, "HTTP/1.1")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    target_server_url = "http://localhost:1000"
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

    print("Server is listening on port 999")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
