from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from functools import partial

# Customization
file_name = "test1.txt"
lines_in_message = 1000
lines_in_file = 0
total_size = 0


def get_lines(offset, size, path):

    lines = []
    try:
        # Open file
        with open(path) as f:
            # set position in file
            f.seek(offset)
            # read lines
            for i in range(lines_in_message):
                line = f.readline()
                # if we read last line we must interrupt loop
                if line:
                    # try to read line as a json
                    try:
                        json_line = json.loads(line)
                    except ValueError:
                        # if not, we have bad data in file or we got wrong offset
                        result = {
                            "ok": False,
                            "reason": "Incorrect data in file or offset"
                        }
                        return result
                    # add correct line to list
                    lines.append(json_line)
                else:
                    break
            # got current position as a new offset
            next_offset = f.tell()
            # make correct message
            result = {
                "ok": True,
                "next_offset": next_offset,
                "total_size": size,
                "messages": lines
            }
    except IOError:
        # incorrect name or path for file
        result = {
            "ok": False,
            "reason": "file was not found"
        }
    return result


# Function for counting size of file.
def get_total_size(path):
    try:
        with open(path) as f:
            # set position to end of file
            f.seek(0, 2)
            # get current position, it is size of file in bytes
            size = f.tell()
    except IOError:
        size = 0
    return size


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
        res = get_lines(position, total_size, file_name)
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
    # jf = LogFile(file_name, lines_in_message)
    total_size = get_total_size(file_name)
    app = make_app()
    app.listen(3000)
    print("Server started")
    IOLoop.instance().start()
