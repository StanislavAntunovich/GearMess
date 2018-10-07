from server_src.server import Server


def run_server(host='', port=7777):
    server = Server(host, port)
    server.run()


if __name__ == '__main__':
    run_server('', 7777)
