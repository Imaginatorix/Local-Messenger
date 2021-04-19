from tkinter import *
from tkinter import messagebox
from math import *
from os import path
import socket
import threading
import time
import winsound

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 15550
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)

class pop_up():        
    def __init__(self, server_found):
        winsound.PlaySound("alarm.wav", winsound.SND_ASYNC)
        
        self.root = Tk()

        var_x = self.root.winfo_screenwidth()
        var_y = self.root.winfo_screenheight()
        def_w = floor(var_x / 2)
        def_h = floor(var_y / 2)
        screendimx2 = floor(var_x / 2)
        screendimy2 = floor(var_y / 2)
        screenw2 = floor(def_w / 2)
        screenh2 = floor(def_h / 2)

        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        self.root.geometry(f"{screenw2}x{screenh2}+{(screendimx2) - floor(screenw2 / 2)}+{(screendimy2) - floor(screenh2 / 2)}")
        ##### ##### PIN!!! FUTURE ME! This is equal to exact center ---------------------------------
        pop_up_msg = Text(self.root, relief = RAISED, font = ("Helvetica", 12), bg = "black", fg = "white", wrap = WORD)
        okay = Button(self.root, text = "Okay", relief = RAISED, font = ("Helvetica", 9), bg = "black", fg = "white", command = self.destroy_pop_up)
        ###
        pop_up_msg.place(relwidth = 1, relheight = 0.9)
        okay.place(relwidth = 1, relheight = 0.1, rely = 0.9)
        
        color_theme = (0, 158, 96)

        pop_up_msg.tag_configure("italic_font", font = ("Helvetica", 12, "italic"))
        pop_up_msg.tag_configure("gray", foreground = "gray")
        pop_up_msg.tag_configure("bold_font", font = (("Helvetica", 12, "bold")))
        pop_up_msg.tag_configure("smoller", font = (("Helvetica", 8)))
        pop_up_msg.tag_configure("colored", foreground = "#%02x%02x%02x" % color_theme)

        pop_up_msg.insert(END, f"New Server Located!\n\n", ("bold_font", "colored"))
        pop_up_msg.insert(END, f"Server Found:\n")
        pop_up_msg.insert(END, f"{server_found}")    
        pop_up_msg.insert(END, f"\n\nThe server is added to 'Available Servers Today.txt'", ("italic_font", "gray", "smoller"))
        
        pop_up_msg.config(state = DISABLED)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', 1)
        self.root.mainloop()

    def destroy_pop_up(self):
        self.root.destroy()

def add_available_server(server_IP):
    if path.exists("Available Servers Today.txt") == True:
        f = open("Available Servers Today.txt", "r")
        lines = f.readlines()
        f.close()

        try:
            if lines[0] != f"{time.strftime('%m, %d, %Y', time.localtime(time.time()))}:\n":
                f = open("Available Servers Today.txt", "w")
                f.write(f"{time.strftime('%m, %d, %Y', time.localtime(time.time()))}:\n")
                pop_up(server_IP)
                f.write(f"{server_IP}\n")
                f.close()
            else:
                allowable = True
                for line in lines:
                    if line.strip() == server_IP:
                        allowable = False
                if allowable:
                    f = open("Available Servers Today.txt", "a")
                    f.write(f"{server_IP}\n")
                    pop_up(server_IP)
                    f.close()
        except IndexError:
            f = open("Available Servers Today.txt", "w")
            f.write(f"{time.strftime('%m, %d, %Y', time.localtime(time.time()))}:\n")
            f.write(f"{server_IP}\n")
            pop_up(server_IP)
            f.close()

    else:
        f = open("Available Servers Today.txt", "w")
        f.write(f"{time.strftime('%m, %d, %Y', time.localtime(time.time()))}:\n")
        f.write(f"{server_IP}\n")
        pop_up(server_IP)
        f.close()

def handle_client(conn, addr):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            # print (msg)

            if msg[0:8] == "192.168.":
                conn.send(("Thank you for telling me!\n").encode(FORMAT))
                add_available_server(msg)
                break
            else:
                conn.send(("INVALID!!!\n").encode(FORMAT))
        else:
            conn.send(("Nothing...\n").encode(FORMAT))
    
    conn.close()

server_socket.listen()
while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=[conn, addr])
    thread.start()
