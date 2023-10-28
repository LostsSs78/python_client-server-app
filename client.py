from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from functions import text_update
import socket
import threading

DATA = ()
username = ''


def thread_connection(username, text_field, ip, port):
    thread = threading.Thread(target=connection, args=(username, text_field, ip, port))
    thread.daemon = True
    thread.start()


def connection(username, text_field, ip,  port=2000):
    global client

    try:
        connection_btn.configure(state='disabled')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(username.encode('utf-8'))

        if client.recv(1024).decode() == '001':
            messagebox.showwarning('Warning', 'Username already taken, write something else, please')
            connection_btn.configure(state='normal')
            return False
    except:
        connection_btn.configure(state='normal')
        messagebox.showerror('Error', 'Connection Failed')
        return False

    send_btn.configure(state='normal')
    ip_address_entry.configure(state='disabled')
    username_entry.configure(state='disabled')

    chat_log = client.recv(1024).decode('utf-8').split('/')

    if len(chat_log) > 0:
        users = [chat_log[_] for _ in range(0, len(chat_log), 2)]
        texts = [chat_log[_] for _ in range(1, len(chat_log), 2)]
        for i in range(len(texts)):
            text_update(users[i] , text_field , texts[i])

    while True:
        try:
            response = client.recv(1024).decode('utf-8').split('/')
            user = response[0]
            text = response[1]

            if response:
                text_update(user, text_field, text)
        except ConnectionResetError:
            client.close()
            connection_btn.configure(state='normal')
            send_btn.configure(state='disabled')
            ip_address_entry.configure(state='normal')
            username_entry.configure(state='normal')


def send_message(entry):
    text = entry.get()
    entry.delete(0, END)
    global username
    if not text:
        messagebox.showwarning('Warning', 'Cant send empty message')
        return False
    client.send(username.encode('utf-8'))
    client.send(text.encode('utf-8'))


def validation(data: tuple):
    if len(data[0]) == 0 or not data[0].isalnum() or data[0].isdigit() or data[0].isdigit():
        messagebox.showwarning('Warning', 'Incorrect username, enter something else, please')
        return False, None
    if len(data[1].split('.')) == 4:
        ip_address = data[1].split('.')
        for i in range(len(ip_address)):
            if not 0 <= int(ip_address[i]) < 255 and int(ip_address[0]) != 0:
                messagebox.showwarning('Warning', 'Incorrect IP-address')
                return False, None
    else:
        messagebox.showwarning('Warning', 'Incorrect IP-address')
        return False, None
    return True, data


def send_data(entry1: Entry, entry2: Entry, text_field):
    flag, data = validation((entry1.get(), entry2.get()))
    if flag:
        global username
        DATA = data
        username = DATA[0]
        thread_connection(DATA[0], text_field, DATA[1], 2000)
        return True

# Initialising main window of application
chat_window = Tk()
chat_window.geometry('800x400')
chat_window.resizable(False, False)
chat_window.title('Messanger client app')

# Title label for application
app_title = ttk.Label(chat_window, text='Messanger Client App', font='Arial 18').pack(anchor=N)

# Entry for entering message text and button for send message
chat_entry = ttk.Entry(chat_window, font='Arial 13')
send_btn = ttk.Button(chat_window, state='disabled', text='Send', command=lambda:send_message(chat_entry))
send_btn.place(x=400, y=350, height=30)
chat_entry.place(x=20, y=350, width=360, height=30)

# Main text field, where displays all messages in app
text_field = ScrolledText(chat_window, state='disabled', relief='ridge', bd=2, wrap='word',
                          height=20, width=68, font='Arial 9')
text_field.pack()
text_field.place(x=1, y=35)

# Label and text field for connected users
#connected_users_label = ttk.Label(text='Connected users:', font='Arial 11')
#connected_users_label.place(x=585, y=210)
#connected_users = ScrolledText(chat_window , state='disabled' , relief='ridge' , bd=2 , wrap='word' , font='Arial 9',
#                               height=9, width=40)
#connected_users.place(x=500, y=240)

# Label, hint for user to input username and servers ip
ip_port_label = ttk.Label(text='Enter your username and Server IP Address', font='Arial 11')
ip_port_label.pack(anchor=N)
ip_port_label.place(x=500, y=65)

# Label and Entry for input username
username_label = ttk.Label(text='Username:', font='Arial 12')
username_entry = ttk.Entry(font='Arial 12')

# Label and Entry for input servers IP Address
ip_address_label = ttk.Label(text='IP-Address:', font='Arial 12')
ip_address_entry = ttk.Entry(font='Arial 12')

# Placing username and IP in application window
ip_address_entry.place(x=595, y=130, height=25, width=180)
username_entry.place(x=595, y=100, height=25, width=180)
username_label.place(x=514, y=100)
ip_address_label.place(x=508, y=130)

# Button for connect to messangers server
connection_btn = ttk.Button(text="CONNECT", width=25, command=lambda:send_data(username_entry, ip_address_entry, text_field))
connection_btn.place(x=600, y=170)

chat_window.mainloop()
