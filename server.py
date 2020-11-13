from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from functools import partial

# Customization
file_name = "test2.txt"
lines_in_message = 1000


# Base class for our service
class LogFile:
    def __init__(self, path, count):
        # Function for counting lines in file.
        # With partial and buffer it should be faster
        def count_lines():
            my_buffer = 2 ** 16
            try:
                with open(path) as f:
                    size = sum(x.count('\n') for x in iter(partial(f.read, my_buffer), ''))
            except IOError:
                size = 0
            return size
        # with open(path) as f:
        #     self.size = len([0 for _ in f])
        self.size = count_lines()
        # Let's open file and keep it as opened until service works
        try:
            self.file = open(path, 'r')
        except IOError:
            self.file = None
        self.count = count

    def get_lines(self, start):
        # if there isn't file
        if (self.size == 0) or (self.file is None):
            result = {
                "ok": False,
                "reason": "file was not found"
            }
        # if there is incorrect offset
        elif start > self.count or start < 0:
            result = {
                "ok": False,
                "reason": "incorrect offset"
            }
        else:
            lines = []
            # Count next offset in file
            next_offset = self.size if (start + self.count > self.size) else start + self.count
            # Read lines from file and add these to list
            for i in range(start, next_offset):
                lines.append(json.loads(self.file.readline()))
            # make correct message
            result = {
                "ok": True,
                "next_offset": next_offset,
                "total_size": self.size,
                "messages": lines
            }
        return result

    def __del__(self):
        # let's close file
        self.file.close()


# test class for tornado server
class HelloHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    # send message if we got simple request
    def get(self):
        self.write({'message': 'hello world'})


# class for post service
class ReadLog(RequestHandler):
    def data_received(self, chunk):
        pass

    # if post let's process
    def post(self):
        # read request from string to json
        req = json.loads(self.request.body)
        # get offset
        position = req['offset']
        # get lines from file
        res = jf.get_lines(position)
        # send
        self.write(res)


def make_app():
    urls = [
        ("/", HelloHandler),
        ("/read_log", ReadLog)
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    print("Please, waite a little. Server is starting")
    jf = LogFile(file_name, lines_in_message)
    app = make_app()
    app.listen(3000)
    print("Server started")
    IOLoop.instance().start()
