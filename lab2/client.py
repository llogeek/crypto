import tkinter.messagebox
from bitarray import bitarray
from cfb import _cfb_decrypt
import random
import socket
import sys
sys.set_int_max_str_digits(6000)
import tkinter as tk
from tkinter import messagebox
import time
import threading
from hashlib import sha256
import os

from flask import app
from gm import generate_key, decrypt, encrypt


class GUI:

    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))
        self.folder_files = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\files\\"
        self.folder_users = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\clients\\"
        self.folder_keys = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\keys\\"
        self.folder_decr = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\decryptes\\"
        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = tk.Label(self.login,
                            text="Login page",
                            justify=tk.CENTER,
                            font="Tahoma 15 bold")

        self.pls.place(relheight=0.15, relx=0.4, rely=0.07)
        self.userLabelName = tk.Label(self.login, text="Username: ", font="Tahoma 12")
        self.userLabelName.place(relheight=0.15, relx=0.1, rely=0.26)

        self.userEntryName = tk.Entry(self.login, font="Tahoma 12")
        self.userEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.29)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Password: ", font="Tahoma 12")
        self.roomLabelName.place(relheight=0.15, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Tahoma 12", show="*")
        self.roomEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.43)
        self.reg = tk.Button(self.login,
                             text="Register",
                             font="Tahoma 12 bold",
                             command=lambda: self.registerr())
        self.go = tk.Button(self.login,
                            text="Log In",
                            font="Tahoma 12 bold",
                            command=lambda: self.login_verify())  # self.goAhead()) #self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))
        self.reg.place(relx=0.45, rely=0.75)
        self.go.place(relx=0.47, rely=0.62)

        self.Window.mainloop()

    def registerr(self):
        self.register_screen = tk.Toplevel()
        self.register_screen.title("Register")
        self.register_screen.geometry("300x220")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.email = tk.StringVar()

        tk.Label(self.register_screen, text="Please enter details below", bg="light green", font=("Tahoma", 10)).pack()
        tk.Label(self.register_screen, text="").pack()
        username_lable = tk.Label(self.register_screen, text="Username * ", font=("Tahoma", 10))
        username_lable.pack()
        self.username_entry = tk.Entry(self.register_screen, textvariable=self.username)
        self.username_entry.pack()
        password_lable = tk.Label(self.register_screen, text="Password * ", font=("Tahoma", 10))
        password_lable.pack()
        self.password_entry = tk.Entry(self.register_screen, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self.register_screen, text="").pack()
        self.confirm_registration = tk.Button(self.register_screen,
                                              text="Confirm Register",
                                              font="Tahoma 12 bold",
                                              command=lambda: self.register_user())
        self.confirm_registration.place(relx=0.245, rely=0.70)

    def register_user(self):
        temp_txt = ''
        username_info = self.username_entry.get()
        password_info = self.password_entry.get()
        list_of_files = os.listdir(self.folder_users)
        if username_info != '' and password_info != '':
            if username_info in list_of_files:
                messagebox.showerror('User Error', 'Error: Such user already exists!')
                temp_txt = "Failed registration"
            else:
                file = open(self.folder_users + username_info, "w")
                file.write(username_info + "\n")
                file.write(sha256(bytes(password_info, 'utf-8')).hexdigest())
                file.close()
                temp_txt = "Registration success"
        else:
            messagebox.showerror('User Error', 'Error: Empty information!')
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if temp_txt == "Registration success":
            tk.Label(self.register_screen, text=temp_txt, fg="green", font=("calibri", 11)).pack()
        else:
            tk.Label(self.register_screen, text=temp_txt, fg="red", font=("calibri", 11)).pack()
        self.register_screen.destroy()

    def login_verify(self):
        username1 = self.userEntryName.get()
        password1 = sha256(bytes(self.roomEntryName.get(), 'utf-8')).hexdigest()
        self.userEntryName.delete(0, tk.END)
        self.roomEntryName.delete(0, tk.END)
        list_of_files = os.listdir(self.folder_users)
        if username1 in list_of_files:
            with open(self.folder_users + username1, "r") as file1:
                verify = file1.read().splitlines()
            if password1 in verify:
                self.username = username1
                self.login_sucess()
            else:
                self.password_not_recognised()

        else:
            self.user_not_found()

    def login_sucess(self):
        self.login_success = tk.Toplevel()
        self.login_success.title("Profile")
        self.login_success.geometry("250x200")
        self.user_label = tk.Label(self.login_success, text="Name: {}".format(self.username), font=("Tahoma", 11))
        self.user_label.pack()
        self.generate_session_key = tk.Button(self.login_success,
                                              text="Generate GM key",
                                              font="Tahoma 11 bold",
                                              command=lambda: self.generate_gm_key())
        self.set_file_name = tk.Button(self.login_success,
                                       text="Input filename",
                                       font="Tahoma 11 bold",
                                       command=lambda: self.file_name_window())
        self.generate_session_key.place(relx=0.21, rely=0.21)
        self.set_file_name.place(relx=0.26, rely=0.41)

    def generate_gm_key(self):
        self.key = generate_key()
        with open(self.folder_keys + "priv_key_" + str(self.username) + '.txt', 'w') as f:
            f.write(str(self.key['priv'][0]))
            f.write(str(self.key['priv'][1]))
        with open(self.folder_keys + "pub_key_" + str(self.username) + '.txt', 'w') as f:
            f.write(str(self.key['pub'][0]))
            f.write(str(self.key['pub'][1]))
        print("Generated keys: ")
        print("Personal key: ", self.key['priv'])
        print("Public key: ", self.key['pub'])

    def file_name_window(self):
        self.login_success.destroy()
        self.get_file = tk.Toplevel()
        self.get_file.title("Filename")
        self.get_file.geometry("250x150")
        frame = tk.Frame(self.get_file)
        self.listbox = tk.Listbox(frame)
        file_items = os.listdir(self.folder_files)
        for item in range(len(file_items)):
            self.listbox.insert(item, file_items[item])

        def dialog():
            self.files = self.listbox.get(self.listbox.curselection())

        btn = tk.Button(frame, text='Set info', command=dialog)
        btn.pack(side=tk.RIGHT, padx=5, pady=2)
        btn2 = tk.Button(frame, text='OK', command=self.goAhead)
        btn2.pack(side=tk.RIGHT, padx=5, pady=5)
        self.listbox.pack(side=tk.LEFT)
        frame.pack(padx=30, pady=30)

    def code_not_recognised(self):
        self.code_not_recog_screen = tk.Toplevel()
        self.code_not_recog_screen.title("Failed")
        self.code_not_recog_screen.geometry("150x100")
        tk.Label(self.code_not_recog_screen, text="Invalid Code ").pack()
        tk.Button(self.code_not_recog_screen,
                  text="OK",
                  font="Helvetica 12 bold",
                  command=lambda: self.delete_code_not_recognised()).pack()

    def user_not_found(self):
        self.user_not_found_screen = tk.Toplevel()
        self.user_not_found_screen.title("Success")
        self.user_not_found_screen.geometry("150x100")
        tk.Label(self.user_not_found_screen, text="User Not Found").pack()
        tk.Button(self.user_not_found_screen,
                  text="OK",
                  font="Helvetica 12 bold",
                  command=lambda: self.delete_user_not_found_screen()).pack()

    def password_not_recognised(self):
        self.password_not_recog_screen = tk.Toplevel()
        self.password_not_recog_screen.title("Failed")
        self.password_not_recog_screen.geometry("150x100")
        tk.Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        tk.Button(self.password_not_recog_screen,
                  text="OK",
                  font="Helvetica 12 bold",
                  command=lambda: self.delete_password_not_recognised()).pack()

    def delete_password_not_recognised(self):
        self.password_not_recog_screen.destroy()

    def delete_code_not_recognised(self):
        self.code_not_recog_screen.destroy()

    def delete_user_not_found_screen(self):
        self.user_not_found_screen.destroy()

    def goAhead(self):
        filename = self.files
        self.get_file.destroy()
        self.key_used = generate_key()
        print("Filename: ", filename.encode())
        print("Public key: ", (str(self.key_used['pub'][0]) + ' ' + str(self.key_used['pub'][1])))
        self.server.send(filename.encode())
        time.sleep(0.1)
        self.server.send(str(self.key_used['pub'][0]).encode())
        self.server.send(str(self.key_used['pub'][1]).encode())
        self.login.destroy()
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            #try:
            message = ""
            while '\n' not in message:
                message += self.server.recv(1024).decode()
            message = message.split('\n')
            key = message[1]
            message = message[0]
            while '\n' not in key:
                key += self.server.recv(1024).decode()
            key_mas = key.split('\n')
            find_in = key_mas[0].split(' ')
            key_encrypted = [int(i) for i in find_in]
            print("Len session key encrypted: ", len(key_encrypted))
            res = decrypt(key_encrypted, self.key_used['priv'])
            print("Key: ", res)
            decrypted_text = _cfb_decrypt(message, res)
            print("Decrypted: ", decrypted_text)

            def BinaryToDecimal(binary):
                string = int(binary, 2)
                return string
            pt_got = ' '.join(decrypted_text[i:i+8] for i in range(0, len(decrypted_text), 8))
            print(pt_got)
            bts = bitarray(pt_got)
            ascs = bts.tobytes().decode('ascii')
            ascs = ascs.replace(chr(0), "")
            with open(self.folder_decr + str(self.username) + "_" + str(self.files), 'w') as f:
                f.write(ascs)
            break
            #except:
            print("User disconnected!")
            self.server.close()
            break
        self.Window.destroy()



if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
    sys.exit(0)
    app.exec()
