import socket
import select
import subprocess
import _c_hidden_c_ as scram

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = socket.gethostname()
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
CURRENTLY_CONNECTED_DEVICES = []
# SUCCESS_ALARM = []
FAIL_ALARM = []

###################################################
# raw_data = subprocess.check_output(["arp", "-a"]).decode(FORMAT).split("\n")

# for line in raw_data:
#     if "dynamic" in line:
#         place = 0
#         for _ in line:
#             if line[place] == "1":
#                 start_position = place
#                 break
#             place += 1
#         for _ in line:
#             if line[place] == " ":
#                 end_position = place
#                 break
#             place += 1

#         CURRENTLY_CONNECTED_DEVICES.append(line[start_position:end_position])

def current_gateway():
    ip_info = subprocess.check_output(["ipconfig"]).decode(FORMAT).split("\n")
    for i in range(len(ip_info)):
        current_line = ip_info[i]
        if "Default Gateway" in current_line:
            maybe_the_ip = ip_info[i + 1]
            if len(maybe_the_ip) == 1:
                maybe_the_ip = ip_info[i]

            for i2 in range(len(maybe_the_ip)):
                if maybe_the_ip[i2] == "1":
                    return (maybe_the_ip[i2:len(maybe_the_ip) - 1])

### NOTICE ME!!!!
# raw_data = subprocess.check_output(["nmap", "-sP", f"{current_gateway()}/24"]).decode(FORMAT).split("\n")

# for line in raw_data:
#     if "Nmap scan report for" in line:
#         ip_line = line[21:len(line) - 1] # -1 for strip
#         if ip_line != current_gateway() and ip_line != SERVER:
#             CURRENTLY_CONNECTED_DEVICES.append(ip_line)

def send(msg, client_socket):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)

def notify_new_server(SERVER):
    PORT = 15550
    ADDR = (SERVER, PORT)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(ADDR)

    not_sent = True

    while not_sent:
        send(socket.gethostbyname(socket.gethostname()), client_socket)
        recvd_msg = client_socket.recv(HEADER).decode(FORMAT)

        if recvd_msg == "Thank you for telling me!\n":
            not_sent = False
            client_socket.close()

print ("IP addresses successfully notified:") ### FOR DYNAMIC EFFECT, I DIDN'T PUT IT IN LIST

none = True
for server in CURRENTLY_CONNECTED_DEVICES:
    try:
        notify_new_server(server)
        print (server)
        none = False
    except (Exception, ConnectionError, ConnectionRefusedError):
        FAIL_ALARM.append(server)
if none:
    print ("None")

print ()

print ("IP addresses not notified:")

for server in FAIL_ALARM:
    print (server)

if len(FAIL_ALARM) == 0:
    print ("None")

print ()
######################################################

# COMMANDS
PRIVATE_MESSAGE = "/pmsg <"
SHOW_ALL_PEEPS_IN_SERVER = "/peeps"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print (f"[STARTING...] Server is starting on {SERVER}")

# SPECIAL #
server_socket.bind(ADDR)
# SPECIAL #

server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

clients = {}

### LATE CODED
clients_addr = {}
###

print(f"[LISTENING] Server is listening for connections on {SERVER}...")

def peer_update(peer, state, exception_client):
    if peer != scram.searcher_name:
        username_s = f"{scram.owner_tag}".encode(FORMAT)
        username_header_s = f"{len(username_s):<{HEADER}}".encode(FORMAT)

        msg = f"{peer} has {state}"
        message_s = msg.encode(FORMAT)
        message_header_s = f"{len(msg):<{HEADER}}".encode(FORMAT)

        for client_socket in clients:
            if client_socket != exception_client:
                client_socket.send(username_header_s + username_s + message_header_s + message_s)

def confirm_client():
    msg = scram.encrypt(scram.entry_pass)
    message_2 = msg.encode(FORMAT)
    message_header_2 = f"{len(msg):<{HEADER}}".encode(FORMAT)

    client_socket.send(message_header_2 + message_2)

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        message_length = int(message_header.decode(FORMAT).strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)} # data here = username

    except:
        return False

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            confirm_client()

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user
            clients_addr[user['data'].decode(FORMAT)] = client_address

            print (f"[NEW CONNECTION] [{client_address}] <{user['data'].decode(FORMAT)}>")
            peer_update(user['data'].decode(FORMAT), "joined", client_socket)
            print (f"[ACTIVE CONNECTIONS] {len(sockets_list) - 1}")

        else:
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print(f"{clients[notified_socket]['data'].decode(FORMAT)} has disconnected")
                peer_update(clients[notified_socket]['data'].decode(FORMAT), "disconnected", notified_socket)

                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                print (f"[ACTIVE CONNECTIONS] {len(sockets_list) - 1}")
                continue

            user = clients[notified_socket]

            print(f"[{clients_addr[user['data'].decode(FORMAT)]}] {user['data'].decode(FORMAT)}: {message['data'].decode(FORMAT)}")

            if message['data'].decode(FORMAT)[0:len(PRIVATE_MESSAGE)] == PRIVATE_MESSAGE:
                closer = -1
                name = ""
                place_holder = 7

                for letter in message['data'].decode(FORMAT)[7:len(message['data'].decode(FORMAT))]:
                    if letter == "<":
                        closer -= 1
                    elif letter == ":" and closer == 0:
                        place_holder += 2
                        break
                    elif letter == ">":
                        closer += 1
                        place_holder += 1
                    else:
                        name += letter
                        place_holder += 1

                exportable_msg = f"{scram.encrypt(scram.pm_code)}{message['data'].decode(FORMAT)[place_holder:len(message['data'].decode(FORMAT))]}"
                message_header = f"{len(exportable_msg):<{HEADER}}".encode(FORMAT)
                message_data = exportable_msg.encode(FORMAT)

                person_not_found = True
                for client_socket in clients:
                    if clients[client_socket]['data'].decode(FORMAT) == name:
                        client_socket.send(user['header'] + user['data'] + message_header + message_data)
                        person_not_found = False

                if person_not_found:
                    exportable_msg = f"{scram.encrypt(scram.pm_error_code)}{name}"
                    message_header = f"{len(exportable_msg):<{HEADER}}".encode(FORMAT)
                    message_data = exportable_msg.encode(FORMAT)

                    notified_socket.send(user['header'] + user['data'] + message_header + message_data)

            elif message['data'].decode(FORMAT)[0:len(SHOW_ALL_PEEPS_IN_SERVER)] == SHOW_ALL_PEEPS_IN_SERVER:
                to_be_sent = [scram.encrypt(scram.show_people_code)]
                
                for client_socket in clients:
                    temp_adder = f"{client_socket.getpeername()}: <{clients[client_socket]['data'].decode(FORMAT)}>"
                    to_be_sent.append(temp_adder)

                exportable_msg = "\n".join(to_be_sent)

                message_header = f"{len(exportable_msg):<{HEADER}}".encode(FORMAT)
                message_data = exportable_msg.encode(FORMAT)
                notified_socket.send(user['header'] + user['data'] + message_header + message_data)

            else:
                if user['data'].decode(FORMAT) == scram.searcher_name:
                    continue
                else:
                    for client_socket in clients:
                        # To all, except sender
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]


