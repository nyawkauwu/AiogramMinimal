import socketio
from aiohttp import web
import asyncio
from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
from os import environ


io = socketio.AsyncServer()
app = web.Application()
io.attach(app)


@io.on("message")
async def update(sid, data):
    init_data: WebAppInitData = None
    try:
        init_data = safe_parse_webapp_init_data(
            environ["BOT_TOKEN"], data["initData"])
        io.emit("message", f"Hello, {init_data.user.first_name}!")
    except ValueError:
        try:
            await io.disconnect(sid)
        except Exception:
            pass

app.router.add_static('/', './webapp')


def run(port=8080):
    # web.run_app(app, host="127.0.0.1", port=port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    handler = app.make_handler()
    server = loop.create_server(handler, host='127.0.0.1', port=port)
    loop.run_until_complete(server)
    loop.run_forever()
