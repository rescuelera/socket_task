import socket

my_socket = socket.socket()
address_and_port = ("127.0.0.1", 9999)
my_socket.bind(address_and_port)
print("Started socket on", address_and_port)
my_socket.listen()
while True:
    conn, addr = my_socket.accept()
    data = conn.recv(4096)
    print("Got data\n", data.decode("utf-8"))
    request_data = data.decode("utf-8")
    request_data_list = request_data.split("\r\n")
    first_row, *headers = request_data_list
    method, url, *_ = first_row.split()
    status = 200
    split_list = url.split("status=")
    if len(split_list) == 2:
        status_string = split_list[1]
        status = int(status_string) if status_string.isdigit() else 200
    response_body = f''' 
    <p>headers: {headers}</p>
    <p>method: {method}</p>
    <p>status: {status}</p>
    '''
    conn.send(
        f"HTTP/1.1 200 OK Content-Length:100\n Connection:close\n Content-Type:text/html\n\n {response_body}".encode())
    conn.close()
my_socket.close()
