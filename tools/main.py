from tkinter import *
from tkinter import ttk
from hashlib import sha1
from tkinter.messagebox import showerror, showinfo
from config.config import endpoint
import requests


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Password-Checker")
        self.geometry("500x500")
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="Black", background="grey", font=('San Francisco', '10', 'bold'))
        self.endpoint = endpoint
        self.configure(background='black')
        self.input_label_frame = LabelFrame(text="Input", font=('San Francisco', '10', 'bold'))
        self.input_label_frame.configure(background='grey')
        self.input_label_frame.pack(fill="x", padx="20", pady="20")
        self.output_label_frame = LabelFrame(text="Output", font=('San Francisco', '10', 'bold'))
        self.output_label_frame.configure(background='grey')
        self.output_label_frame.pack(fill="both", padx="20", pady="5", expand=True)
        self.output_label = ttk.Label(self.output_label_frame, text="You will see output here ... ", style="BW.TLabel")
        self.output_label.configure(background='Grey')
        self.output_label.pack(anchor=CENTER)
        self.button_frame = Frame()
        self.button_frame.configure(background='Black')
        self.button_frame.pack(padx="20", pady="5")
        self.password_label = ttk.Label(self.input_label_frame, text="Password:", style="BW.TLabel")
        self.password_label.pack(anchor=NW, side="left")
        self.password_entry = ttk.Entry(self.input_label_frame, show="#")
        self.password_entry.pack(anchor=NW, side="left", fill="x", expand=True, padx="20")
        self.check_button = ttk.Button(self.button_frame, text="Check", command=self.check_password)
        self.check_button.pack(side="left")
        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.destroy)
        self.exit_button.pack(side="left", padx="5")
        self.notice_label = Label(text="**Important**: API & data comes from https://haveibeenpwned.com",
                                  background="Black",
                                  foreground="white")
        self.notice_label.pack(side="bottom", anchor=CENTER)

    def check_password(self):
        self.output_label.destroy()
        data = sha1(self.password_entry.get().encode()).hexdigest().upper()
        req = requests.get(f'{self.endpoint}/{data[:5]}')
        if req.status_code != 200:
            showerror(title="Error!",
                      message=f"The status code of GET request is {req.status_code}.\nResponse headers:\n{req.headers}")
        else:
            showinfo(title="Info",
                     message=f"The status code of GET request is {req.status_code}.\nResponse headers:\n{req.headers}")
            hash_tuple = (item.split(":") for item in req.text.splitlines())
            match = False
            for h, count in hash_tuple:
                if h == data[5:]:
                    if int(count) > 0:
                        self.output_label = ttk.Label(self.output_label_frame,
                                                      text=f"Please change your password ...\nthis "
                                                           f"password has been in {count} security breaches.",
                                                      style="BW.TLabel")
                        self.output_label.configure(background='Grey')
                        self.output_label.pack(anchor=CENTER)
                        match = True
            if not match:
                self.output_label = ttk.Label(self.output_label_frame,
                                              text=f"Awesome! your password did not appear in any security breach.",
                                              style="BW.TLabel")
                self.output_label.configure(background='Grey')
                self.output_label.pack(anchor=CENTER)


if __name__ == "__main__":
    password_checker = App()
    password_checker.mainloop()
