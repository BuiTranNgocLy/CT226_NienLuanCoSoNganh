from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

#Hàm nhận 
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: #Thông báo client đã rời phòng chat
            break

#sự kiện được thông qua
def send(event=None):  
    msg = my_msg.get()
    my_msg.set("")  #xóa trường nhập liệu.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

#Giao diện khi khởi động client.py
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  #Gửi tin nhắn từ client.
my_msg.set("Nhập tên của bạn!.")
scrollbar = tkinter.Scrollbar(messages_frame)  #Chuyển hướng tin nhắn sang các tin nhắn khác.
#chứa các tin nhắn từ client.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gửi", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#Ket noi toi server
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Bắt đầu GUI.