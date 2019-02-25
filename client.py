#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from rsa import generate_keypair , is_prime ,encrypt ,decrypt


# send key on the first time when we send name :
keySent = False

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = str(client_socket.recv(BUFSIZ).decode("utf8"))
            # if "has joined the chat!" in msg:
            #     usrs_list.insert(tkinter.END,msg.split(" ")[0])
                # usrs_list.

            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global keySent
    inp = my_msg.get()
    msg = str(inp)

    if (not keySent):
        msg += " " + str(public)
        keySent = True

    my_msg.set("")  # Clears input field.

    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def generate_Keys():
    p = 2
    q = 4
    while(not (is_prime(p) and is_prime(q) and p != q)):
        p = int(input("enter first prim number : "))
        q = int(input("enter second prim number : "))

    return generate_keypair(p, q)


#----Now comes the sockets part----
HOST = input('Enter host "127.0.0.1 by default": ')
PORT = input('Enter port "33000 by default": ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

# generating keys :
public, private  = generate_Keys()
print("Your public key is ", public, " and your private key is ", private)




client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your Name first.")
# To navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30,
                           width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

#users online :
usrs_list = tkinter.Listbox(messages_frame, height=10,
                           width=30, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)



receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
