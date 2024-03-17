from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import getsize
import json
JSON_FILE = "database.json"
HOST = 'localhost'
PORT = 8888

class RequestHandler(BaseHTTPRequestHandler):
    '''
    BaseHTTPRequestHandler DOC
    instance variables
        client_address
            Contains a tuple of the form (host, port) referring to the client’s address.
        server
            Contains the server instance.
        close_connection
            Boolean that should be set before handle_one_request() returns, indicating if another request may be expected, or if the connection should be shut down.
        requestline
            Contains the string representation of the HTTP request line. The terminating CRLF is stripped. This attribute should be set by handle_one_request(). If no valid request line was processed, it should be set to the empty string.
        command
            Contains the command (request type). For example, 'GET'.
        path
            Contains the request path.
        request_version
            Contains the version string from the request. For example, 'HTTP/1.0'.
        headers
            Holds an instance of the class specified by the MessageClass class variable. This instance parses and manages the headers in the HTTP request. The parse_headers() function from http.client is used to parse the headers and it requires that the HTTP request provide a valid RFC 2822 style header.
        rfile
            An io.BufferedIOBase input stream, ready to read from the start of the optional input data.
        wfile
            Contains the output stream for writing a response back to the client. Proper adherence to the HTTP protocol must be used when writing to this stream in order to achieve successful interoperation with HTTP clients.

    attributes
        server_version
            Specifies the server software version. You may want to override this. The format is multiple whitespace-separated strings, where each string is of the form name[/version]. For example, 'BaseHTTP/0.2'.
        sys_version
            Contains the Python system version, in a form usable by the version_string method and the server_version class variable. For example, 'Python/1.4'.
        error_message_format
            Specifies a format string that should be used by send_error() method for building an error response to the client. The string is filled by default with variables from responses based on the status code that passed to send_error().
        error_content_type
            Specifies the Content-Type HTTP header of error responses sent to the client. The default value is 'text/html'.
        protocol_version
            This specifies the HTTP protocol version used in responses. If set to 'HTTP/1.1', the server will permit HTTP persistent connections; however, your server must then include an accurate Content-Length header (using send_header()) in all of its responses to clients. For backwards compatibility, the setting defaults to 'HTTP/1.0'.
        MessageClass
            Specifies an email.message.Message-like class to parse HTTP headers. Typically, this is not overridden, and it defaults to http.client.HTTPMessage.
        responses
            This attribute contains a mapping of error code integers to two-element tuples containing a short and long message. For example, {code: (shortmessage, longmessage)}. The shortmessage is usually used as the message key in an error response, and longmessage as the explain key. It is used by send_response_only() and send_error() methods.

    mathods
        handle()
            Calls handle_one_request() once (or, if persistent connections are enabled, multiple times) to handle incoming HTTP requests. You should never need to override it; instead, implement appropriate do_*() methods.
        handle_one_request()
            This method will parse and dispatch the request to the appropriate do_*() method. You should never need to override it.
        handle_expect_100()
            When a HTTP/1.1 compliant server receives an Expect: 100-continue request header it responds back with a 100 Continue followed by 200 OK headers. This method can be overridden to raise an error if the server does not want the client to continue. For e.g. server can chose to send 417 Expectation Failed as a response header and return False.
        send_error(code, message=None, explain=None)
            Sends and logs a complete error reply to the client. The numeric code specifies the HTTP error code, with message as an optional, short, human readable description of the error. The explain argument can be used to provide more detailed information about the error; it will be formatted using the error_message_format attribute and emitted, after a complete set of headers, as the response body. The responses attribute holds the default values for message and explain that will be used if no value is provided; for unknown codes the default value for both is the string ???. The body will be empty if the method is HEAD or the response code is one of the following: 1xx, 204 No Content, 205 Reset Content, 304 Not Modified.
        send_response(code, message=None)
            Adds a response header to the headers buffer and logs the accepted request. The HTTP response line is written to the internal buffer, followed by Server and Date headers. The values for these two headers are picked up from the version_string() and date_time_string() methods, respectively. If the server does not intend to send any other headers using the send_header() method, then send_response() should be followed by an end_headers() call.
        send_header(keyword, value)
            Adds the HTTP header to an internal buffer which will be written to the output stream when either end_headers() or flush_headers() is invoked. keyword should specify the header keyword, with value specifying its value. Note that, after the send_header calls are done, end_headers() MUST BE called in order to complete the operation.
        send_response_only(code, message=None)
            Sends the response header only, used for the purposes when 100 Continue response is sent by the server to the client. The headers not buffered and sent directly the output stream.If the message is not specified, the HTTP message corresponding the response code is sent.
        end_headers()
            Adds a blank line (indicating the end of the HTTP headers in the response) to the headers buffer and calls flush_headers().
        flush_headers()
            Finally send the headers to the output stream and flush the internal headers buffer.
        log_request(code='-', size='-')
            Logs an accepted (successful) request. code should specify the numeric HTTP code associated with the response. If a size of the response is available, then it should be passed as the size parameter.
        log_error(...)
            Logs an error when a request cannot be fulfilled. By default, it passes the message to log_message(), so it takes the same arguments (format and additional values).
        log_message(format, ...)
            Logs an arbitrary message to sys.stderr. This is typically overridden to create custom error logging mechanisms. The format argument is a standard printf-style format string, where the additional arguments to log_message() are applied as inputs to the formatting. The client ip address and current date and time are prefixed to every message logged.
        version_string()
            Returns the server software’s version string. This is a combination of the server_version and sys_version attributes.
        date_time_string(timestamp=None)
            Returns the date and time given by timestamp (which must be None or in the format returned by time.time()), formatted for a message header. If timestamp is omitted, it uses the current date and time.
        log_date_time_string()
            Returns the current date and time, formatted for logging.
        address_string()
            Returns the client address.
    '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', getsize("index.html"))
        self.end_headers()       
        
    def do_GET(self):
        print(self.path)
        if self.path == '/data':
            self.get_data()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', getsize("index.html"))
        self.end_headers()
        file = open("index.html", 'r')
        response_data = file.read().encode('utf-8')
        file.close()
        self.wfile.write(response_data)

    def get_data(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', getsize("database.json"))
        self.end_headers()
        file = open("database.json", 'r')
        response_data = file.read().encode('utf-8')
        file.close()
        print(response_data)
        self.wfile.write(response_data)

    def do_POST(self):
        '''limit post_data length, limit database size'''
        # Read the POST data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Decode the received JSON data
        try:
            new_data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON data')
            return

        # Load existing data from JSON file
        try:
            with open(JSON_FILE, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}
            
        # Update existing data with new data
        print(existing_data)
        existing_data.update(new_data)
        print(existing_data)
        
        # Write updated data back to JSON file
        with open(JSON_FILE, 'w') as f:
            json.dump(existing_data, f)

        # Send a response indicating success
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Data stored successfully')




def main(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, RequestHandler)
    print(f"Server started on {HOST}:{PORT}")
    httpd.serve_forever()
    

main()
