import asyncio

from server_src.async_server import ServerHandlerProtocol


def server_run(host='', port=7777):
    connections = {}
    authorised = []
    online = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ServerHandlerProtocol(connections, authorised, online), host, port)
    server = loop.run_until_complete(coro)
    loop.run_forever()


if __name__ == '__main__':
    server_run()
