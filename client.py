import socket
import threading
import tkinter
from tkinter import messagebox
import tkinter.scrolledtext

HOST = 'localhost'
PORT = 33000
nicknames = []


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        msg = tkinter.Tk()
        msg.withdraw()

        self.gui_done = False
        self.running = True

        self.login = tkinter.Tk()
        self.input_Label = tkinter.Label(self.login, text="login: ")
        self.input_Label.grid(row=0, column=0)
        self.input_login = tkinter.Text(self.login, pady=5, padx=5, width=25, height=1)
        self.input_login.grid(row=0, column=1)
        self.login_button = tkinter.Button(self.login, text="Confirm chosen nickname", command=self.confirm_login)
        self.login_button.grid(row=1, column=1, pady=5, padx=5)
        self.login.mainloop()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.title("nazwa aplikacji")
        self.win.resizable(width=False, height=False)

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.grid(row=0, column=0, padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.grid(row=1, column=0, padx=20, pady=5)
        self.text_area.config(state='disabled')

        scroll = tkinter.Scrollbar(self.win)
        self.online_list = tkinter.Listbox(self.win, width=25, height=20, yscrollcommand=scroll.set)
        self.online_list.bind('<Double-Button>', self.open_chat)
        self.online_list.config(font=("Arial", 12))
        self.online_list.grid(row=1, column=1, padx=8, pady=5)
        self.online_list.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.grid(row=2, column=0, padx=20, pady=5)

        self.online_label = tkinter.Label(self.win, text="Users online:", bg="lightgray")
        self.online_label.config(font=("Arial", 12))
        self.online_label.grid(row=0, column=1, padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.grid(row=3, column=0, padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.bind("<Return>", self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.grid(row=4, column=0, padx=20, pady=5)

        self.gui_done = True
        self.updateUsers(nicknames)

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.win.mainloop()

    def open_chat(self, *args):
        print("essa")

    def updateUsers(self, nicknames):
        if self.gui_done:
            self.online_list.config(state='normal')
            self.online_list.delete(0, self.online_list.size())
            for nickname in nicknames:
                self.online_list.insert('end', nickname)
            self.online_list.yview('end')
            self.online_list.config(state='disabled')

    def confirm_login(self):
        login = self.input_login.get('1.0', 'end')
        login = login[0:str(login).find("\n")]
        if login == "":
            messagebox.showerror("Error", "Invalid username, input field cannot be empty")
        else:
            self.nickname = login
            nicknames.append(self.nickname)
            self.sock.connect((HOST, PORT))

            gui_thread = threading.Thread(target=self.gui_loop)
            receive_thread = threading.Thread(target=self.receive)

            gui_thread.start()
            receive_thread.start()

            self.login.destroy()

    def receive(self):
        """Handles receiving of messages."""
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NICK":
                    print(self.nickname)
                    self.sock.send(self.nickname.encode('utf-8'))
                elif message.startswith('UPDATE'):
                    if message[len('UPDATE '):].startswith("JOIN"):
                        nicknames.append(message[len('UPDATE JOIN '):])
                    elif message[len('UPDATE '):].startswith("LEFT"):
                        nicknames.remove(message[len('UPDATE LEFT '):])
                    self.updateUsers(nicknames)
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break

    def write(self):
        """Handles sending of messages."""
        if self.input_area.get('1.0', 'end') != "\n":
            message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def on_closing(self):
        """This function is to be called when the window is closed."""
        self.running = False
        self.win.destroy()
        self.sock.close()


client = Client(HOST, PORT)
