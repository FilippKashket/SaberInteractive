from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from functools import partial

file_name = "'test1.txt'"
lines_in_message = 1000

class LogFile:
    def __init__(self, path, count):
        def count_lines():
            my_buffer = 2 ** 16
            with open(path) as f:
                size = sum(x.count('\n') for x in iter(partial(f.read, my_buffer), ''))
            return size
        # with open(path) as f:
        #     self.size = len([0 for _ in f])
        self.size = count_lines()
        self.file = open(path, 'r')
        self.count = count

    def get_lines(self, start):
        lines = []
        next_offset = self.size if (start + self.count > self.size) else start + self.count
        for i in range(start, next_offset):
            lines.append(json.loads(self.file.readline()))
        result = {
            "ok": True,
            "next_offset": next_offset,
            "total_size": self.size,
            "messages": lines
        }
        return result

    def __del__(self):
        self.file.close()


class HelloHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write({'message': 'hello world'})


class ReadLog(RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        req = json.loads(self.request.body)
        position = req['offset']
        res = jf.get_lines(position)
        self.write({'message': res})


def make_app():
    urls = [
        ("/", HelloHandler),
        ("/read_log", ReadLog)
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    jf = LogFile(file_name, lines_in_message)
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
