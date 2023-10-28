from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from functions import text_update
from server_config import *
import socket
import threading


def ip_validate(base_config) -> None:
    ip = ip_port_entry.get()

    if ip:
        ip, *port = ip.split(':')
        if not port:
            port = 2000
        else:
            if int(port[0]) not in range(1024, 65556):
                messagebox.showwarning('Warning', 'Incorrect port')
                return None
            port = int(port[0])
        ip = [el for el in ip.split('.')]
        print(ip)
        if len(ip) != 4:
            messagebox.showwarning('Warning', 'Incorrect IP-address')
            return None
        for i in ip:
            if i.isdigit() and int(i) in range(1, 256):
                continue
            else:
                messagebox.showwarning('Warning', 'Incorrect IP-address')
                break
        else:
            try:
                thread_server({'IP': '.'.join(ip), 'Port': port}, text_field)
            except:
                messagebox.showerror('Error', 'Can`t create server on this ip-port')
    elif ip == '':
        thread_server(base_config, text_field)
    else:
        messagebox.showerror('Error', 'Some error occurred')
        return None


def thread_server(config, text_field):
    ip_port_entry.configure(state='disabled')
    thread = threading.Thread(target=start_server, args=(config, text_field))
    thread.daemon = True
    thread.start()


def start_server(config: dict, text_field: ScrolledText):
    global chat_log
    start_server_button.config(state='disabled')
    stop_server_button.config(state='normal')

    try:
        global server_sock, users_log
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((config['IP'], config['Port']))
        server_sock.listen(10)

        text_update(server_username, text_field, 'Server started on IP-address and port: {}:{}'.format(config['IP'],
                                                                                                       config['Port']))

        while True:
            client, address = server_sock.accept()
            if address not in users:
                new_username = client.recv(1024).decode('utf-8')

                if new_username in users.keys():
                    client.send('001'.encode('utf-8'))
                    client.close()
                else:
                    client.send('000'.encode('utf-8'))
                    users[new_username] = client
                    text_update(server_username, text_field, 'User "{}" connected to chat!'.format(new_username))
                    client.send(chat_log.encode('utf-8'))
                    message_user = new_username + '/'
                    message_text = f'User {new_username} connected to chat'
                    chat_log += message_user + message_text + '/'
                    for user in users.keys() :
                        users[user].sendall((message_user + message_text).encode('utf-8'))
            if len(users) != 0:
                thread = threading.Thread(target=messanger, args=(client,))
                thread.daemon = True
                thread.start()
    except OSError as _ex:
        error = str(_ex).split()[1][:-1]
        if error == '10049':
            messagebox.showerror('Server start error', 'Unable to start server on given ip-port')
        elif error == '10038':
            pass
        else:
            messagebox.showerror('Server start error', 'Unable to start server with code ' + error)


def messanger(client: socket.socket):
    global users, chat_log
    try:
        while True:
            message_user = client.recv(1024).decode('utf-8')
            message_text = client.recv(1024).decode('utf-8')
            response = message_user + '/' + message_text
            chat_log += response + '/'
            for user in users.keys():
                users[user].sendall(response.encode('utf-8'))
    except ConnectionResetError as _ex:
        for username, user_client in users.items():
            if user_client == client:
                del users[username]
                text_update(server_username, text_field, f'User {username} disconnected from chat')
                disconnected_user = username + '/'
                disconnected__text = f'User {username} disconnected from chat'
                chat_log += disconnected_user + '/' + disconnected__text + '/'
                for user in users.keys():
                    users[user].sendall((disconnected_user + disconnected__text).encode('utf-8'))
        # except RuntimeError:
        #    for user in users.keys():
        #        users[user].sendall((server_username + '/' + f'Connection was closed').encode('utf-8'))


def end_server(text_field):
    global users, chat_log
    start_server_button.config(state='normal')
    stop_server_button.config(state='disabled')
    ip_port_entry.configure(state='normal')

    chat_log = ''

    for user, connection in users.items():
        users[user].sendall((server_username + '/' + f'Connection was closed').encode('utf-8'))
        connection.close()
    text_update(server_username, text_field, 'Server closed')
    server_sock.close()


server_window = Tk()
server_window.geometry('500x360')
server_window.title('Server app')
server_window.resizable(False, False)

app_title = ttk.Label(text='Server App', font='Arial 18').pack(anchor=N)
ip_port_label = ttk.Label(text='Servers IP-address and port: (standart port is 2000)', font='Arial 9').place(x=185,
                                                                                                             y=285)

start_server_button = ttk.Button(text='START', command=lambda: ip_validate(config))
stop_server_button = ttk.Button(text='STOP', state='disabled', command=lambda: end_server(text_field))

start_server_button.place(x=20, y=305, height=30)
stop_server_button.place(x=100, y=305, height=30)

ip_port_entry = ttk.Entry(font='Arial 13')
ip_port_entry.place(x=185, y=305, width=250, height=30)

text_field = ScrolledText(state='disabled', relief='ridge', bd=2, wrap='word',
                          height=16, width=68, font='Arial 9')
text_field.pack()
text_field.place(x=1, y=35)

text_update(server_username, text_field, 'Welcome to Server App!')

server_window.mainloop()
