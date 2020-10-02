# refer https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# abc@abc.com 123

# imports for system
import tkinter as tk
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import re
import sqlite3
import pandas as pd
from tkcalendar import *
import numpy as np
import pickle
from pandastable import Table
import math
import random
import smtplib


# main class which renders different frames as per users actions
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.grid(sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Code to navigate between pages
        for F in (StartPage, SignUpPage, PredictionPage, ForgotPassword):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")  # strech window in all direction
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def update_frame(self, page_name):
        frame = self.frames[page_name]
        frame.update()

    def destroy_frame(self, page_name):
        frame = self.frames[page_name]
        frame.destroy()

    def des(self):
        self.destroy()


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', indicator=0):
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.put_placeholder()
        self['bd'] = 8
        self['relief'] = GROOVE
        self['font'] = ("", 15)
        self.indicator = indicator
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.insert(0, self.placeholder)

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
        if (self.indicator):
            self['show'] = "*"

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
        if (self.indicator):
            if (self.get().__contains__("Enter the ")):
                self['show'] = ""


# Homepage, which will display first to user
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        global lusername, lpassword
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="Start Page")
        # label.pack(pady=10,padx=10)

        self.lusername = StringVar()
        self.lpassword = StringVar()
        self.controller = controller
        self.bg_image = ImageTk.PhotoImage(file='images/background.jpg')
        self.loginimage_icon = ImageTk.PhotoImage(file='images/login.png')
        self.user_icon = ImageTk.PhotoImage(file='images/user.png')
        self.password_icon = ImageTk.PhotoImage(file='images/password.png')
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.grid(row=0, column=0, sticky="nsew")
        title = tk.Label(self, text="Vegetable Price Predictor ", font=("times new roman", 36, "bold"), fg="red",
                         bg="yellow", bd=8, relief=GROOVE)
        title.place(x=0, y=0, relwidth=1)

        LoginFrame = Frame(self, bg="white")
        LoginFrame.place(x=480, y=200)
        loginimage_label = Label(LoginFrame, image=self.loginimage_icon, bg="white").grid(row=0, columnspan=2)
        username_label = Label(LoginFrame, text="Username", bg="white", image=self.user_icon, compound=LEFT,
                               font=("times new roman", 20, "bold")).grid(row=1, column=0, padx=25, pady=10)
        password_label = Label(LoginFrame, text="Password", bg="white", image=self.password_icon, compound=LEFT,
                               font=("times new roman", 20, "bold")).grid(row=2, column=0, padx=25, pady=10)
        self.usernameText = EntryWithPlaceholder(LoginFrame, "Enter the username", 'grey',
                                                 0)  # Entry(LoginFrame, bd=8, textvariable=self.lusername, relief=GROOVE, font=("", 15))
        self.usernameText['textvariable'] = self.lusername
        self.usernameText['fg'] = "grey"
        self.usernameText.insert(0, "Enter the username")
        self.usernameText.grid(row=1, column=1, padx=25)
        self.passwordText = EntryWithPlaceholder(LoginFrame, "Enter the password", 'grey',
                                                 1)  # Entry(LoginFrame, bd=8, textvariable=self.lpassword, relief=GROOVE, show='*', font=("", 15)).grid(row=2,column=1,padx=25)
        self.passwordText['textvariable'] = self.lpassword
        self.passwordText['fg'] = "grey"
        self.passwordText.insert(0, "Enter the password")
        self.passwordText.grid(row=2, column=1, padx=25)
        loginButton = tk.Button(LoginFrame, text="Login", command=self.LoginWindow, width=15, bd=2, bg="Green",
                                fg="White", font=("times new roman", 14, "bold")).grid(row=4, columnspan=3, pady=8)
        signUpButton = Button(LoginFrame, text="Sign Up", command=lambda: controller.show_frame(SignUpPage), width=15,
                              bd=2, bg="Yellow", fg="Red", font=("times new roman", 14, "bold")).grid(row=5,
                                                                                                      columnspan=3,
                                                                                                      pady=8)
        ResetButton = Button(LoginFrame, text="Forgot Password", command=self.reset, width=15, bd=2, bg="Blue",
                             fg="White", font=("times new roman", 14, "bold")).grid(row=6, columnspan=3, pady=8)
        ExitButton = Button(LoginFrame, text="Exit", command=self.quit, width=15, bd=2, bg="Red", fg="White",
                            font=("times new roman", 14, "bold")).grid(row=7, columnspan=3, pady=8)

    def LoginWindow(self):
        conn = sqlite3.connect("UserDB.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER")
            rows = cursor.fetchall()
            flag = 0
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            if (self.lusername.get() == '' or self.lpassword.get() == ''):
                messagebox.showerror("Error", "Username Or Password Cannot Be Blank")
            elif (not (re.search(regex, self.lusername.get()))):
                messagebox.showerror("Error", "Please Enter a valid mail id")
            else:
                for usr, passw in rows:
                    if (usr == self.lusername.get() and passw == self.lpassword.get()):
                        flag = 1
                        conn.commit()
                        self.controller.show_frame(PredictionPage)
                if (flag == 0):
                    messagebox.showerror("Error", "Check Your Credentials")
        conn.commit()
        return 0;

    def signup(self):
        return 0;

    def reset(self):
        self.usernameText.delete('0', 'end')
        self.passwordText.delete('0', 'end')
        self.controller.show_frame(ForgotPassword)

    def quit(self):
        self.usernameText.delete('0', 'end')
        self.passwordText.delete('0', 'end')
        self.controller.des()

    # signup page Frame is created using this class


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.susername = StringVar()
        self.spassword = StringVar()
        self.cpassword = StringVar()
        # username_label = Label(self, text="Back To Home", bg="white", compound=LEFT,font=("times new roman", 20, "bold")).grid(row=1, column=0, padx=25, pady=10)
        # signUpButton = Button(self, text="Sign Up", command= lambda: controller.show_frame(StartPage), width=15, bd=2, bg="Yellow", fg="Red",font=("times new roman", 14, "bold")).grid(row=5, columnspan=3, pady=8)
        self.bg_image = ImageTk.PhotoImage(file='images/background.jpg')
        self.user_icon = ImageTk.PhotoImage(file='images/user.png')
        self.password_icon = ImageTk.PhotoImage(file='images/password.png')
        self.loginimage_icon = ImageTk.PhotoImage(file='images/login.png')
        self.controller = controller
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.grid(row=0, column=0)

        title = tk.Label(self, text="Vegetable Price Predictor ", font=("times new roman", 36, "bold"), fg="red",
                         bg="yellow", bd=8, relief=GROOVE)
        title.place(x=0, y=0, relwidth=1)

        signupFrame = Frame(self, bg="white")
        signupFrame.place(x=480, y=200)
        loginimage_label = Label(signupFrame, image=self.loginimage_icon, bg="white")
        loginimage_label.config(image=self.loginimage_icon)
        loginimage_label.image = self.loginimage_icon
        loginimage_label.grid(row=0, columnspan=2)
        username_label = Label(signupFrame, text="Username", bg="white", image=self.user_icon, compound=LEFT,
                               font=("times new roman", 19, "bold"))
        username_label.config(image=self.user_icon)
        username_label.image = self.user_icon
        username_label.grid(row=1, column=0, padx=15, pady=10)
        password_label = Label(signupFrame, text="Password", bg="white", image=self.password_icon, compound=LEFT,
                               font=("times new roman", 19, "bold"))
        password_label1 = Label(signupFrame, text="Confirm Password", bg="white", image=self.password_icon,
                                compound=LEFT, font=("times new roman", 16, "bold"))
        password_label.config(image=self.password_icon)
        password_label.image = self.password_icon
        password_label1.config(image=self.password_icon)
        password_label1.image = self.password_icon
        password_label.grid(row=2, column=0, padx=15, pady=10)
        password_label1.grid(row=3, column=0, padx=15, pady=10)
        susernameText = EntryWithPlaceholder(signupFrame, "Enter the username", 'grey',
                                             0)  # Entry(signupFrame, bd=8, textvariable=self.susername, relief=GROOVE, font=("", 15))
        susernameText['textvariable'] = self.susername
        susernameText['fg'] = "grey"
        susernameText.insert(0, "Enter the username")
        susernameText.grid(row=1, column=1, padx=15, pady=12)

        spasswordText = EntryWithPlaceholder(signupFrame, "Enter the password", 'grey',
                                             1)  # Entry(signupFrame, bd=8, textvariable=self.spassword, relief=GROOVE, show='*', font=("", 15)).grid(row=2,column=1,padx=15,pady=12)
        spasswordText['textvariable'] = self.spassword
        spasswordText['fg'] = "grey"
        spasswordText.insert(0, "Enter the password")
        spasswordText.grid(row=2, column=1, padx=15, pady=12)

        spasswordText1 = EntryWithPlaceholder(signupFrame, "Enter the confirm password", 'grey',
                                              1)  # Entry(signupFrame, bd=8, textvariable=self.cpassword, relief=GROOVE, show='*', font=("", 15)).grid(row=3, column=1, padx=15,pady=12)
        spasswordText1['textvariable'] = self.cpassword
        spasswordText1['fg'] = "grey"
        spasswordText1.insert(0, "Enter the confirm password")
        spasswordText1.grid(row=3, column=1, padx=15, pady=12)

        registerButton = Button(signupFrame, text="Register", command=self.validate, width=15, bd=2, bg="Yellow",
                                fg="Red", font=("times new roman", 14, "bold")).grid(row=6, columnspan=2, pady=15)
        sExit = Button(signupFrame, text="Exit", command=self.quit, width=15, bd=2, bg="Red", fg="White",
                       font=("times new roman", 14, "bold")).grid(row=8, columnspan=2, pady=15)

    def validate(self):
        Username = self.susername.get()
        Password = self.spassword.get()
        CPassword = self.cpassword.get()
        flag = 0
        # print(Username)
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if ((Username == '' or Password == '' or CPassword == '')):
            messagebox.showerror("Error", "Username Or Password Cannot Be Blank")
        elif (not (re.search(regex, Username))):
            messagebox.showerror("Error", "Please Enter a valid mail id")
        else:
            if (CPassword == Password):
                flag = 1
                conn = None
                conn = sqlite3.connect("UserDB.db")
                with conn:
                    try:
                        cursor = conn.cursor()
                        if (self.toggle == 0):
                            cursor.execute(
                                'CREATE TABLE IF NOT EXISTS USER(Username TEXT NOT NULL UNIQUE ,Password TEXT NOT NULL)')
                            cursor.execute('INSERT INTO USER(Username,Password) VALUES(?,?)', (Username, Password))
                            messagebox.showinfo("Registraion Successful",
                                                "Dear User You Have Registered With Our System ")
                            conn.commit()
                        else:
                            print("hi")
                    except:
                        messagebox.showerror("Error", "This Username is already exist")
                self.controller.show_frame(StartPage)
            else:
                messagebox.showerror("Error", "Please Check Password and Confirm Password field")
        return 0;

    def quit(self):
        self.controller.show_frame(StartPage)


# Prediction code is inside this class
class PredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cvariable = StringVar()
        self.vvariable = StringVar()
        self.controller = controller
        self.parent = parent
        self.bg_image = ImageTk.PhotoImage(file='images/background.jpg')
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.grid(row=0, column=0)
        title = tk.Label(self, text="Vegetable Price Predictor ", font=("times new roman", 36, "bold"), fg="red",
                         bg="yellow", bd=8, relief=GROOVE)
        title.place(x=0, y=0, relwidth=1)

        self.PredictionFrame = Frame(self, bg="white")
        self.PredictionFrame.place(x=180, y=140)
        self.PredictedFrame = Frame(self, bg="white")
        self.PredictedFrame.place(x=670, y=140)

        df = pd.read_csv("Potato_2019.csv")
        # cal = DateEntry(self.PredictionFrame, width=12, background='darkblue', foreground='white', borderwidth=2)

        # def print_sel():
        #    global current_date
        #    current_date = cal.get_date()

        metadata = pd.read_csv("Metadata.csv")
        self.storage = metadata
        self.commodity_list = metadata["Commodity"]
        # cvariable.trace('w', change_dropdown_commodity)
        self.cvariable.set(self.commodity_list[0])
        self.cvariable.trace('w', self.change_dropdown_commodity)
        self.commodity_label = Label(self.PredictionFrame, text="Commodity", bg="white", compound=LEFT,
                                     font=("times new roman", 15, "bold")).grid(row=0, column=0, padx=20, pady=18)
        self.commoityOption = OptionMenu(self.PredictionFrame, self.cvariable, *self.commodity_list).grid(row=0,
                                                                                                          column=1,
                                                                                                          padx=20,
                                                                                                          pady=18)

        # date_label = Label(self.PredictionFrame, text="Date", bg="white", compound=LEFT,font=("times new roman", 15, "bold")).grid(row=5, column=0, padx=20, pady=18)
        # cal.grid(row=5, column=1,pady=18)
        # startDateButton = Button(self.PredictionFrame, text="Select Start Date", width=12, bd=2, bg="navyblue",fg="white", font=("times new roman", 12, "bold"), command=print_sel).grid(row=5, column=2,pady=18)
        predictButton = Button(self.PredictionFrame, text="Predict", command=self.predict, width=15, bd=2, bg="Yellow",
                               fg="Red", font=("times new roman", 14, "bold")).grid(row=8, columnspan=3, pady=18)
        logoutButton = Button(self.PredictionFrame, text="Signout", command=self.logout, width=15, bd=2, bg="blue",
                              fg="white", font=("times new roman", 14, "bold")).grid(row=9, columnspan=3, pady=18)

    def logout(self):
        # self.controller.destroy_frame(PredictionPage)
        self.controller.update_frame(PredictionPage)
        self.controller.show_frame(StartPage)

    def change_dropdown_commodity(self, *args):
        self.city_list = self.adapt_changes(self.cvariable.get())
        self.vvariable.set(self.city_list[0])
        self.City_label = Label(self.PredictionFrame, text="City", bg="white", compound=LEFT,
                                font=("times new roman", 15, "bold")).grid(row=1, column=0, padx=20, pady=18)
        self.CityOption = OptionMenu(self.PredictionFrame, self.vvariable, *self.city_list).grid(row=1, column=1,
                                                                                                 padx=20, pady=18)

    def adapt_changes(self, var):
        self.change = self.storage[self.storage["Commodity"] == var]["Cities"]
        self.change = str(np.array(self.change)[0]).split(",")
        return self.change

    def predict(self):
        self.city = self.vvariable.get()
        self.vegetable = self.cvariable.get()
        try:
            # features dataset path
            training = pd.read_csv("Vegetables_10//" + self.city + "//" + self.city + "_" + self.vegetable + "_X.csv")
            # Labels datset file path
            testing = pd.read_csv("Vegetables_10//" + self.city + "//" + self.city + "_" + self.vegetable + "_y.csv")
            # Date file path
            Date = pd.read_csv("Vegetables_10//" + self.city + "//" + self.city + "_" + self.vegetable + "_Date.csv")

            # trained file path(pickle file)
            filename = "Vegetables_10//" + self.city + "//" + self.city + "_" + self.vegetable
        except:
            messagebox.showerror("Error", "City Not Selected")

        with open(filename, "rb") as f:
            rf = pickle.load(f)

        # Unncessary columns are droped
        training = training.drop(['index'], axis=1)
        testing = testing.drop(['index'], axis=1)
        Date = Date.drop(['index'], axis=1)

        predicted = rf.predict(training)
        actual = np.reshape(np.array(testing), (len(testing),))
        Date = np.reshape(np.array(Date), (len(Date),))
        data = []

        for i in range(len(actual)):
            data.append([Date[i], actual[i], predicted[i]])

        sum = 0
        for i in range(len(predicted)):
            # print(str(actual[i]) + "->" + str(predicted[i]))
            sum = sum + abs(actual[i] - predicted[i])
        print(sum / len(predicted))

        PredictedFrame = Frame(self, bg="white")
        PredictedFrame.place(x=670, y=140)
        # print(data)
        self.dataframe = pd.DataFrame(data, columns=['Date', 'Actual_Price/Quintal', 'Predicted_Price/Quintal'])
        print(self.dataframe)
        pt = Table(PredictedFrame, dataframe=self.dataframe, showtoolbar=True, showstatusbar=True)
        pt.show()


class ForgotPassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_icon = ImageTk.PhotoImage(file='images/Icon_4.jpg')
        self.lusername = StringVar()
        self.otp = StringVar()
        self.email = StringVar()
        self.random = 0
        self.bg_image = ImageTk.PhotoImage(file='images/background.jpg')
        self.loginimage_icon = ImageTk.PhotoImage(file='images/login.png')
        self.user_icon = ImageTk.PhotoImage(file='images/user.png')
        self.password_icon = ImageTk.PhotoImage(file='images/password.png')
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.grid(row=0, column=0, sticky="nsew")
        title = tk.Label(self, text="Vegetable Price Predictor ", font=("times new roman", 36, "bold"), fg="red",
                         bg="yellow", bd=8, relief=GROOVE)
        title.place(x=0, y=0, relwidth=1)

        ResetFrame = Frame(self, bg="white")
        ResetFrame.place(x=480, y=200)
        self.toggle = 0
        username_label = Label(ResetFrame, text="Username", bg="white", compound=LEFT,
                               font=("times new roman", 20, "bold")).grid(row=0, column=0, padx=25, pady=10)
        self.usernameText = EntryWithPlaceholder(ResetFrame, "Enter your registered email", 'grey', 0)
        self.usernameText['textvariable'] = self.email
        self.usernameText['fg'] = "grey"
        self.usernameText.insert(0, "Enter the username")
        self.usernameText.grid(row=0, column=1, padx=25)
        reset = Button(ResetFrame, text="send", command=self.check_email, width=15, bd=2, bg="Yellow", fg="Red",
                       font=("times new roman", 14, "bold")).grid(row=0, column=2, columnspan=3, pady=8)
        otpLabel = Label(ResetFrame, text="OTP", bg="white", compound=LEFT, font=("times new roman", 20, "bold")).grid(
            row=1, column=0, padx=25, pady=10)
        self.otpText = EntryWithPlaceholder(ResetFrame, "otp", 'grey', 0)
        self.otpText['textvariable'] = self.otp
        self.otpText['fg'] = "grey"
        self.otpText.insert(0, "otp")
        self.otpText.grid(row=1, column=1, padx=25)
        verify = Button(ResetFrame, text="verify", command=self.verify, width=15, bd=2, bg="Yellow", fg="Red",
                        font=("times new roman", 14, "bold")).grid(row=2, column=1)
        logoutButton = Button(ResetFrame, text="Home", command=self.logout, width=15, bd=2, bg="blue", fg="white",
                              font=("times new roman", 14, "bold")).grid(row=3, column=1, pady=18)

    def check_email(self):
        def fpassword():
            # Declare a digits variable
            # which stores all digits
            digits = "0123456789"
            OTP = ""

            # length of password can be changed
            # by changing value in range
            for i in range(4):
                OTP += digits[math.floor(random.random() * 10)]

            return OTP

        # Function ends here

        receipent_email = self.email.get()
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (receipent_email == ''):
            messagebox.showerror("Error", "Email Cannot Be Blank")
        elif (not (re.search(regex, receipent_email))):
            messagebox.showerror("Error", "Please Enter a valid mail id")
        else:
            content = fpassword()
            self.random = content
            print(self.random)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()  # identify computer
            mail.starttls()  # transport layer security
            # admin mail-id and password (check that the account should off the less secure app in settings)
            mail.login('beprojectvpp@gmail.com', '20192020')
            # first mail-id for recipients second is for admin
            header = 'To:' + receipent_email + '\n' + 'From: ' \
                     + 'BE-Project Password Reset' + '\n' + 'Subject : Your OTP For Resetting Password \n'

            content = header + content
            mail.sendmail('beprojectvpp@gmail.com', receipent_email, content)
            mail.close()
        return

    def verify(self):
        if (self.random == self.otp.get()):
            print("Success")
            self.controller.show_frame(SignUpPage)
            self.toggle = 1
        return

    def logout(self):
        self.controller.show_frame(StartPage)


# actual code will be executing from here
gui = GUI()
gui.mainloop()