import asyncio
from asyncio import transports


data = {}

class ClientServerPorotcol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def process_data(command):
    if command[:4] == 'get ' and command[-1:] == '\n':
        return get_data(command[4:-1])
    elif command[:4] == 'put ' and command[-1:] == '\n':
        return put_data(command[4:-1])
    else:
        return 'error\nwrong command\n\n'

def get_data(command):
    if command == '*':
        response = 'ok\n'
        for metric_name in data.keys():
            for record in data[metric_name]:
                timestamp = record[0]
                value = record[1]
                response += f'{metric_name} {value} {timestamp}\n'
        response += '\n'
        return response
    elif ' ' in command:
        response = 'error\nwrong command\n\n'
        return response
    else:
        response = 'ok\n'
        metric_name = command
        if metric_name in data.keys():
            for record in data[metric_name]:
                timestamp = record[0]
                value = record[1]
                response += f'{metric_name} {value} {timestamp}\n'
        response += '\n'
        return response

def put_data(command):
    try:
        metric, value, timestamp = command.split(' ')
        value = float(value)
        timestamp = int(timestamp)
    except ValueError:
        return 'error\nwrong command\n\n'
    
    if metric in data.keys():
        for item in data[metric]:
            if timestamp == item[0]:
                data[metric].remove(item)
        data[metric].append((timestamp, value))
    else:
        data[metric] = [(timestamp, value)]
    return 'ok\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerPorotcol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8181)