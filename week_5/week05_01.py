from os import CLD_EXITED
import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        if timeout is None:
            pass
        else:
            self.timeout = timeout

    def get(self, metric_name):
        data = ''
        request = 'get ' + metric_name + '\n'
        with socket.create_connection((self.host, self.port)) as sock:
            sock.send(request.encode('utf8'))
            data = sock.recv(1024).decode('utf8')
        if data == 'ok\n\n':
            return {}
        elif data == 'error\nwrong command\n\n':
            raise ClientError
        elif data[0:3] == 'ok\n' and data[-2:] == '\n\n':
            data = data[3:-2]
            lines = data.split('\n')
            answer_dict = {}
            for line in lines:
                try:
                    metric_name, value, timestamp = line.split(' ')
                    value = float(value)
                    timestamp = int(timestamp)
                except ValueError:
                    raise ClientError
                if metric_name in answer_dict.keys():
                    answer_dict[metric_name].append(tuple((timestamp, value)))
                else:
                    answer_dict[metric_name] = [tuple((timestamp, value))]
            for dict_key in answer_dict.keys():
                answer_dict[dict_key] = sorted(answer_dict[dict_key], 
                                               key=lambda x: x[0])
            return answer_dict
        else:
            raise ClientError

    def put(self, metric_name, value, timestamp=None):
        if timestamp == None:
            timestamp = int(time.time())
        request = 'put {metric_name} {value} {timestamp}\n'
        with socket.create_connection((self.host, self.port)) as sock:
            sent = sock.send(request.encode('utf8'))
            answer = sock.recv(1024).decode('utf8')
            if sent == 0 or answer != 'ok\n\n':
                raise ClientError    


class ClientError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClientError'