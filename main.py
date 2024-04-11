import requests  # py -m pip install requests
# Used for scraping. We need to install bs4 and import BeautifulSoup: py -m pip install bs4.
from bs4 import BeautifulSoup
import pandas as pd  # used for cleaning data and converting it to csv file
import time  # used for pause scraping and not to be blocked by the server
import csv  # used for csv file
import json  # used for json file
import datetime  # used for date and time
from datetime import datetime  # used for date and time
import sqlite3  # used for database connection
import matplotlib.pyplot as plt  # used for plotting
import pygal  # used for plotting
from tkinter import *  # py -m pip install tkinter
from tkinter import messagebox  # used for message box
from turtle import Screen, heading  # used for turtle graphics
import tkinter as tk  # used for tkinter
# used for filedialog and messagebox
from tkinter import ttk, filedialog, messagebox
from tkinter.messagebox import showinfo  # used for showinfo
from PIL import ImageTk  # used for image
import numpy as np  # used for numpy
import customtkinter  # <- import the CustomTkinter module
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # used for plotting
import threading  # used for threading
import subprocess  # used for subprocess


class LoginWindow():
    # Establishes the database connection and initializes the cursor
    def __init__(self, db_file):
        self.conector = sqlite3.connect(db_file)
        self.c = self.conector.cursor()
        # Create the users table if it does not already exist
        self.createTable('users', ['id INTEGER PRIMARY KEY',
                                   'username TEXT NOT NULL', 'password TEXT NOT NULL'])
        # Create the locations table if it does not already exist
        self.createTable('locations', ['id INTEGER PRIMARY KEY',
                                       'location_name TEXT NOT NULL'])
        # Invokes the method to create the login form
        self.create_gui()

        # self.createTable('locations', ['id INTEGER PRIMARY KEY',
        #                                'location_name TEXT NOT NULL'])
        # self.createTable()
###############################################################################################
# Invokes the method to create the login form

    def createTable(self, table_name, columns):
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} ({','.join(columns)});'''
        # Execute the SQL query
        self.c.execute(query)
        # Commit the changes to the database
        self.conector.commit()
##############################################################################################
    # Method to create the graphical user interface for the login form

    def create_gui(self):
        self.rootlog = tk.Tk()  # Initialize the window

        self.rootlog.title("Login")  # Set the window title
        # Define the window size and position
        self.rootlog.geometry("900x500+300+100")

        self.rootlog.configure(bg='#264848')  # Set the window background color
        self.rootlog.resizable(False, False)  # Make the window non-resizable


        # Load and place the image for the login form
        self.img = PhotoImage(file="login_img.png")
        Label(self.rootlog, image=self.img, bg='#264848').place(x=50, y=120)

        # Create and place a frame for the login form
        self.frame = Frame(self.rootlog, width=450, height=400, bg="white")
        self.frame.place(x=350, y=50)

        # Create and place a heading for the login form
        self.heading = Label(self.frame, text="Sign in", fg="#575757",
                             bg="white", font=("Tahoma", 30, "bold"))
        self.heading.place(x=150, y=5)

        # Labels for the username entry field will be created later
        # on_enter: The field will be cleared when it gains focus
        # on_leave: The default text will be restored if the field is empty when it looses focus
        def on_enter(e):
            self.username_entry.delete(0, "end")

        def on_leave(e):
            username_entry = self.username_entry.get()
            if username_entry == "":
                self.username_entry.insert(0, "Username")

        # entry for username
        self.username_entry = Entry(self.frame, width=30, fg="black", border=0,
                                    bg="white", font=("Tahoma", 12))
        self.username_entry.place(x=100, y=100)
        self.username_entry.insert(0, "Username")

        self.username_entry.bind("<FocusIn>", on_enter)
        self.username_entry.bind("<FocusOut>", on_leave)
        # line for bottom username
        Frame(self.frame, width=275, height=2,
              bg="#575757").place(x=100, y=125)

        # password entry text labels
        # the same 2 functions on_enter (when user click text Password desapear,
        # and on_leave if not was entered any text - Username text will be back
        def on_enter(e):
            self.password_entry.delete(0, "end")

        def on_leave(e):
            name = self.password_entry.get()
            if name == "":
                self.password_entry.insert(0, "Password")

        # Create a password entry field with specified properties
        self.password_entry = Entry(self.frame, width=30, fg="black", border=0,
                                    bg="white", font=("Tahoma", 12))
        self.password_entry.place(x=100, y=150)
        self.password_entry.insert(0, "Password")
        # Create a line under the password entry field
        Frame(self.frame, width=275, height=2,
              bg="#575757").place(x=100, y=175)
        # Bind the on_enter and on_leave functions to the password entry field
        # These functions will be called when the field gains and looses focus
        self.password_entry.bind("<FocusIn>", on_enter)
        self.password_entry.bind("<FocusOut>", on_leave)

        # Create a "Sign in" button, which triggers the login method when clicked
        Button(self.frame, width=30, pady=7, text="Sign in", bg="#244F68",
               font=("Tahoma", 12), fg="azure", border=0, command=self.login).place(x=100, y=230)

        # Create a label indicating the option to create a new account
        self.label = Label(self.frame, text="Don't have an account?",
                           fg="black", bg="white", font=("Tahoma", 10))
        self.label.place(x=100, y=310)

        # Method to close the login form when the "Register" button is clicked
        def reg():
            self.rootlog.destroy()

        # The button triggers the signup method when clicked
        self.reg_user = Button(self.frame, width=6, text="Register", command=self.signup, border=0,
                               bg="white", font=("Tahoma", 12), cursor="hand2", fg="#11B4BB",)
        self.reg_user.place(x=250, y=305)

        # Display the login window
        self.rootlog.mainloop()


#########################################################################################################

##############################################################################################

    def signup(self):
        signup_window = tk.Toplevel(self.rootlog)
        signup_window.title("Register")
        signup_window.geometry("900x500+300+100")
        signup_window.configure(bg='#264848')
        signup_window.resizable(False, False)

        # Load and place the image for the signup form
        img = PhotoImage(file="register_img1.png")
        Label(signup_window, image=img, bg='#264848').place(x=70, y=130)

        # Create and place a frame for the signup form
        frame = Frame(signup_window, width=450, height=400, bg="white")
        frame.place(x=350, y=50)

        # Create and place a heading for the signup form
        heading = Label(frame, text="Register", fg="#575757",
                        bg="white", font=("Tahoma", 30, "bold"))
        heading.place(x=150, y=5)

        # Define the behavior when the username entry field gains focus
        def on_enter(e):
            username_entry.delete(0, "end")

        def on_leave(e):
            name = self.username_entry.get()
            if name == "":
                username_entry.insert(0, "Username")
        # Create a username entry field with specified properties
        username_entry = Entry(frame, width=30, fg="black", border=0,
                               bg="white", font=("Tahoma", 12))
        username_entry.place(x=100, y=100)
        username_entry.insert(0, "Username")

        # Bind the on_enter and on_leave functions to the username entry field
        # These functions will be triggered when the field gains and loses focus, respectively
        username_entry.bind("<FocusIn>", on_enter)
        username_entry.bind("<FocusOut>", on_leave)

        # Create a line under the username entry field
        Frame(frame, width=275, height=2, bg="#575757").place(x=100, y=125)

        # Define the behavior when the password entry field gains focus
        def on_enter(e):
            password_entry.delete(0, "end")
        # Define the behavior when the password entry field loses focus

        def on_leave(e):
            name = password_entry.get()
            if name == "":
                password_entry.insert(0, "Password")

        # Create a password entry field with specified properties
        password_entry = Entry(frame, width=30, fg="black", border=0,
                               bg="white", font=("Tahoma", 12))
        password_entry.place(x=100, y=150)
        password_entry.insert(0, "Password")

        # Create a line under the password entry field
        Frame(frame, width=275, height=2, bg="#575757").place(x=100, y=175)

        # Bind the on_enter and on_leave functions to the password entry field
        # These functions will be triggered when the field gains and loses focus, respectively
        password_entry.bind("<FocusIn>", on_enter)
        password_entry.bind("<FocusOut>", on_leave)

        # Define the behavior when the confirm password entry field gains focus
        def on_enter(e):
            confirm_password_entry.delete(0, "end")
        # Define the behavior when the confirm password entry field loses focus

        def on_leave(e):
            confirm_password_entry = confirm_password_entry.get()
            if confirm_password_entry == "":
                confirm_password_entry.insert(0, "Confirm password")

        confirm_password_entry = Entry(frame, width=30, fg="black", border=0,
                                       bg="white", font=("Tahoma", 12))
        confirm_password_entry.place(x=100, y=200)
        confirm_password_entry.insert(0, "Confirm password")

        # Create a line under the confirm password entry field
        Frame(frame, width=275, height=2, bg="#575757").place(x=100, y=225)
        # Bind the on_enter and on_leave functions to the confirm password entry field
        confirm_password_entry.bind("<FocusIn>", on_enter)
        confirm_password_entry.bind("<FocusOut>", on_leave)

        # Create a "Sign up" button, which triggers the create_user method when clicked
        Button(frame, width=30, pady=7, text="Sign up", bg="#244F68",
               font=("Tahoma", 12), fg="white", border=0, command=lambda: self.create_user(username_entry.get(), password_entry.get(), confirm_password_entry.get(), signup_window)).place(x=100, y=260)

        # Create a label indicating the option to sign in if the user already has an account
        label = Label(frame, text="I have an account!",
                      fg="black", bg="white", font=("Tahoma", 10))
        label.place(x=100, y=330)

        # Method to close the signup form when the "Sign in" button is clicked
        def sign():
            signup_window.destroy()
        # sign up button
        reg_user = Button(frame, width=6, text="Sign in", border=0,
                          bg="white", font=("Tahoma", 12), cursor="hand2", fg="#11B4BB", command=sign)
        reg_user.place(x=250, y=325)
        signup_window.mainloop()
#############################################################################################
    # Method to validate the user's credentials and grant access to the application

    def create_user(self, username, password, confirm_password, signup_window):
        # Check if the password and confirm password fields match
        if password != confirm_password:
            messagebox.showerror("Sign up", "Passwords do not match!")
        else:
            query = "SELECT * FROM users WHERE username=?"
            self.c.execute(query, (username,))
            result = self.c.fetchone()
            if result is not None:
                messagebox.showerror(
                    "Sign up", "This Username already exists!\nChose another one!")

            else:
                query = "INSERT INTO users (username, password) VALUES (?, ?)"
                self.c.execute(query, (username, password))
                self.conector.commit()
                messagebox.showinfo("Sign up", "Successfully signed up!")
                signup_window.destroy()

    def __del__(self):
        self.conector.close()  # Close the database connection


########################## CREATE MY APP ################################

    def main(self):
        # Set the appearance mode and default color theme
        # Modes: system (default), light, dark
        customtkinter.set_appearance_mode("Dark")
        # Themes: blue (default), dark-blue, green
        customtkinter.set_default_color_theme("green")

        # Initialize the main window
        root = customtkinter.CTk()
        root.eval('tk::PlaceWindow . center')
        root.geometry('1150x550+300+100')

        # Set the window title and prevent resizing
        root.title('Daft.ie HOUSES')
        root.pack_propagate(False)

        # Define a function to the download_db_to_csv_page

        def download_db_to_csv_page():
            download_csv_page_frame = tk.Frame(main_frame)
            download_csv_page_frame.pack(pady=5)

    # Begin the process of displaying the required data on the page

            # Define a function to open the CSV file

            def open_csv():
                # use the filedialog.askopenfilename method to open the file
                my_file = filedialog.askopenfilename(title="Open File",
                                                     filetypes=(("Csv Files", ".csv"), ("All Files", ".*")))
                # attempt to read the file and display the data in a table
                try:
                    df = pd.read_csv(my_file)
                    print(df)
                except Exception as e:
                    messagebox.showerror("Ups!", f'Some errors! {e}')

                # Clear the existing data in the treeview
                my_treeview.delete(*my_treeview.get_children())

                # Set the treeview columns
                my_treeview['column'] = list(df.columns[1:])
                my_treeview['show'] = 'headings'
                # Set the headings for each column in the treeview widget to match the column names in the CSV file
                for colums in my_treeview['column']:
                    my_treeview.heading(colums, text=colums)
                # convert the dataframe to a list of lists
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    my_treeview.insert("", "end", values=row[1:])

            # Create a Treeview widget to display the CSV file data

            # Add a scrollbar to the treeview widget
            my_treeview_scroll = Scrollbar(download_csv_page_frame)
            my_treeview_scroll.pack(side=RIGHT, fill=Y)
            # Initialize the treeview widget with the specified properties
            my_treeview = ttk.Treeview(
                download_csv_page_frame, height=15, yscrollcommand=my_treeview_scroll.set)
            my_treeview.pack()

            # Configure the scrollbar to scroll the treeview widget
            my_treeview_scroll.config(command=my_treeview.yview)

            ######### set treevew styles ########################
            style = ttk.Style()
            style.theme_use("default")
            # change colors for style
            style.configure("Treeview", background="azure", foreground="black", font=(
                'Bold', 12), rowheight=25, fieldbackground="azure")
            # change colors of headers
            style.configure("Treeview.Heading", background="#545454",
                            foreground="white", font=('Bold', 16), padding=(5, 10, 5, 10))
            # column heading height
            my_treeview.heading('#0', text="\n")

            my_treeview.heading(
                "# 0", text="Treeview for csv file", anchor=CENTER)
        # column width
            my_treeview.column("# 0", anchor=CENTER, stretch=NO, width=1200)
            # change color of selected row
            style.map('Treeview', background=[('selected', "green")])

            ################################################################################################
            # Define a function to clean the CSV file before uploading it to the database

            def clean_csv():

                # Open a file dialog to select the CSV file
                my_file = filedialog.askopenfilename(title="Open File",
                                                     filetypes=(("Csv Files", ".csv"), ("All Files", ".*")))
                # Attempt to read the selected file as a CSV file and clean the data
                try:
                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(my_file)
                    # Remove all rows with missing values
                    df = df[df.bed != "(0,)"]
                    # Write the cleaned data to a new CSV file
                    df.to_csv('out_clean_csv.csv', index=False)

                except Exception as e:
                    messagebox.showerror("Ups!", f'Some errors! {e}')

             ###############################################################################################################
            # Create a frame for the "View CSV File" button, which triggers the open_csv function when clicked
            frame_btn = customtkinter.CTkFrame(
                download_csv_page_frame, fg_color='#545454')
            frame_btn.pack(padx=50, pady=(20, 5), fill="x")
            # Create a button to open the CSV file
            download_btn = customtkinter.CTkButton(
                frame_btn, text="1.View CSV File", fg_color='#343638', font=customtkinter.CTkFont(size=18, weight='bold'), command=open_csv)
            download_btn.pack(fill="x", padx=50, pady=10, side=tk.LEFT)
            #############################################################################################################################

            # Create a frame for the "Clean CSV File" button that triggers the clean_csv function when clicked

            clean_btn = customtkinter.CTkButton(
                frame_btn, text="2.Clean CSV File", fg_color='#343638', font=customtkinter.CTkFont(size=18, weight='bold'), command=clean_csv)
            clean_btn.pack(fill="x", padx=50, pady=10, side=tk.LEFT)

            #######################################################################################################################

            # Create a frame for the "Choose location data" label for combobox
            # This frame will contain the label and combobox for selecting the location data

            frame_location = customtkinter.CTkFrame(
                download_csv_page_frame, fg_color='#545454')
            frame_location.pack(padx=50, pady=(5, 20), fill="both")
            # Create a label for the "Choose location data" section
            label_location = customtkinter.CTkLabel(
                frame_location, text="Choose location data", font=customtkinter.CTkFont(weight="bold"))
            label_location.pack()

            #############################################################################################################################
            # Create the 'locations' table if it does not already exist
            query = f'''CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY,
                    location_name TEXT)'''
            # Execute the SQL query
            self.c.execute(query)
            self.conector.commit()

            # Retrieve the options from the 'locations' table to populate the combobox
            self.c.execute("SELECT location_name FROM locations")
            locations = [row[0] for row in self.c.fetchall()]

            # Create a Combobox widget for location selection
            # The options for the combobox are retrieved from the 'locations' table
            combo_box = customtkinter.CTkComboBox(
                frame_location,  values=locations)
            # Pack the combobox widget to the frame
            combo_box.pack(fill="x", padx=50, pady=5, side=tk.LEFT)

            # Define a function to add a new location to the 'locations' table
            def add_location():
                new_location = tk.simpledialog.askstring(
                    "New Location", "Enter a new location name:")
                if new_location:
                    self.c.execute(
                        "INSERT INTO locations (location_name) VALUES (?)", (new_location,))
                    self.conector.commit()
                    # Commit the changes to the database
                    combo_box.configure(values=get_options())

            # Define a function to delete a selected location from the 'locations' table
            def delete_location():
                selected_location = combo_box.get()
                if selected_location:
                    self.c.execute(
                        "DELETE FROM locations WHERE location_name=?", (selected_location,))
                    self.conector.commit()
                    combo_box.configure(values=get_options())

            # Define a function to retrieve the options from the 'locations' table
            def get_options():
                self.c.execute("SELECT location_name FROM locations")
                options = [row[0] for row in self.c.fetchall()]
                return options

            ##########################################################

####################################################################################################

            # Section to upload the cleaned CSV file to the database

            def upload_to_db():
                selected_location = combo_box.get()
                # Create the table with the selected name if it does not already exist and exclude m2,bed,bath to be just integer value and float
                self.c.execute(
                    f"CREATE TABLE IF NOT EXISTS {selected_location} (address TEXT, price REAL, beds INTEGER, baths INTEGER, floor_area REAL, property_type TEXT)")

                # Open the cleaned CSV file and read the data
                with open('out_clean_csv.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader)  # Skip the header row
                    for row in csv_reader:
                        address = row[1]
                        price = float(row[2])
                        # integer value split and take just first value
                        beds = int(row[3].split()[0])
                        baths = int(row[4].split()[0])
                        # float value split and take just first value
                        floor_area = float(row[5].split()[0])
                        property_type = row[6]

                        # Check if the record already exists in the database
                        self.c.execute(
                            f"SELECT * FROM {selected_location} WHERE address=?", (address,))
                        existing_record = self.c.fetchone()

                        if existing_record:
                            # Update the existing record
                            self.c.execute(f"UPDATE {selected_location} SET price=?, beds=?, baths=?, floor_area=?, property_type=? WHERE address=?", (
                                price, beds, baths, floor_area, property_type, address))
                        else:
                            # Insert the new record into the database
                            self.c.execute(f"INSERT INTO {selected_location} VALUES (?, ?, ?, ?, ?, ?)", (
                                address, price, beds, baths, floor_area, property_type))
                messagebox.showinfo("Success", "Data uploaded to database!")

                # Commit the changes to the database
                self.conector.commit()

            ################################################################################################

            # Create a button which uploads the cleaned CSV file to the database

            upload__DB_btn = customtkinter.CTkButton(
                frame_location, text="3.Upload to DB", fg_color='#343638', font=customtkinter.CTkFont(size=18, weight='bold'), command=upload_to_db)
            upload__DB_btn.pack(fill="x", padx=50, pady=10, side=tk.LEFT)
            #####################################################################################################
            # Create a frame for the "Download CSV File" button, which triggers the download_csv function when clicked
            add_button = tk.Button(
                frame_location, text="Add Location", font=('Times New Roman Bold', 12), fg="azure", bg="#343638", command=add_location)
            add_button.pack(fill="x", padx=50, pady=10, side=tk.LEFT)
            # Create a frame for the "Delete Location" button, which triggers the delete_location function when clicked
            delete_button = tk.Button(
                frame_location, text="Delete Location", font=('Times New Roman Bold', 12), fg="azure", bg="#343638", command=delete_location)
            delete_button.pack(fill="x", padx=50, pady=10, side=tk.LEFT)
    #########################################################################################
    #########################################################################################
    ####################### D A S H B O A R D  P A G E ######################################
        # Define a function to display the dashboard page
        def dashboard_page():
            frame_main_dashboard = tk.Frame(main_frame)
            frame_main_dashboard.pack(pady=10)
            # Create a frame for the dashboard page
            frame_up_main = customtkinter.CTkFrame(
                frame_main_dashboard, fg_color='#454545')
            frame_up_main.pack(fill="both", padx=50, pady=(20, 10))

            lb_title = tk.Label(frame_up_main, text='Choose data to create your chart',
                                font=('Bold', 15))
            lb_title.pack(padx=10, pady=10)

            # Create a frame for the data chart
            frame_data_chart = customtkinter.CTkFrame(
                frame_up_main, fg_color='#545454')
            frame_data_chart.pack(fill="x", padx=50)

            #######################################################
            # Create a frame table name up to frame_data_chart
            frame_table_name = customtkinter.CTkFrame(
                frame_data_chart, fg_color='azure')
            frame_table_name.pack(fill="both", padx=50, pady=50, side=tk.LEFT)
            # label for table name
            lb_table_name = tk.Label(frame_table_name, text='Choose location', bg='azure',
                                     font=('Bold', 15))
            lb_table_name.pack(padx=5)

            # Create a combobox to select the table name-location
            # retrieve the options from all tables exclude some
            self.c.execute(
                f'''SELECT name FROM sqlite_master WHERE type='table'AND name NOT IN ('locations', 'users', 'sqlite_sequence')''')
            table_names = [table[0] for table in self.c.fetchall()]

            table_combobox = customtkinter.CTkComboBox(
                frame_table_name, values=table_names)
            table_combobox.pack(fill="both", padx=10, pady=10, side=tk.LEFT)

            selected_table_names = table_combobox.get()

            ###############################################################
            # Query the column names of the selected table

            self.c.execute(f"PRAGMA table_info('{selected_table_names}')")
            column_names = [row[1] for row in self.c.fetchall()]

            # Create a frame x-axis up to frame_data_chart
            frame_x_axis = customtkinter.CTkFrame(
                frame_data_chart, fg_color='azure')
            frame_x_axis.pack(fill="both", padx=50, pady=50, side=tk.LEFT)
            # label for x-axis
            lb_x_axis = tk.Label(frame_x_axis, text='Choose x-axis', bg='azure',
                                 font=('Bold', 15))
            lb_x_axis.pack(padx=5)

            # Create a combobox to select the x-axis column
            x_column_combobox = customtkinter.CTkComboBox(
                frame_x_axis, values=column_names)
            x_column_combobox.pack(fill="both", padx=10, pady=10, side=tk.LEFT)

            # x value for chart
            x_column_name = x_column_combobox.get()

            # Create a frame y-axis up to frame_data_chart
            frame_y_axis = customtkinter.CTkFrame(
                frame_data_chart, fg_color='azure')
            frame_y_axis.pack(fill="both", padx=50, pady=50, side=tk.LEFT)
            # label for y-axis
            lb__y_axis = tk.Label(frame_y_axis, text='Choose y-axis', bg='azure',
                                  font=('Bold', 15))
            lb__y_axis.pack(padx=5)

            # Create a combobox to select the y-axis column
            y_column_combobox = customtkinter.CTkComboBox(
                frame_y_axis, values=column_names)
            y_column_combobox.pack(fill="both", padx=10, pady=10, side=tk.LEFT)

            # y value for chart
            y_column_name = y_column_combobox.get()

            # Define a function to update the column comboboxes when the table combobox is changed
            def update_column_comboboxes(event):
                # Get the selected table name
                selected_table_names = table_combobox.get()

                # Update the column comboboxes with the column names for the selected table
                x_column_combobox['values'] = get_column_names(
                    selected_table_names)
                y_column_combobox['values'] = get_column_names(
                    selected_table_names)

            # Bind the update_column_comboboxes function to the table_combobox event
            table_combobox.bind("<<ComboboxSelected>>",
                                update_column_comboboxes)

            # Define a function to create a chart when the create chart button is clicked
            def generate_chart():
                # Get the selected table name and column names
                selected_table_names = table_combobox.get()
                x_column_name = x_column_combobox.get()
                y_column_name = y_column_combobox.get()

                # Get the data for the selected columns
                x_data = get_column_data(selected_table_names, x_column_name)
                y_data = get_column_data(selected_table_names, y_column_name)

                # Create the chart
                if check_box2.get():
                    check_box1.deselect()  # Deselect the first checkbox
                    create_chart(x_data, y_data)
                elif check_box1.get():

                    create_chart1(x_data, y_data)

                def my_search(self):
                    # Get the selected table name and price value
                    selected_table_name = self.table_combobox.get()
                    selected_price_value = self.price_combobox.get()

                    # Get the data for the selected table and price value
                    table_data = get_table(selected_table_name)
                    price_data = get_price(
                        selected_table_name, selected_price_value)

                    # Perform the search operation
                    search_result = self.perform_search(
                        table_data, price_data)

                    # Display the search result
                    self.display_search_result(search_result)
#####################################################################################################
# check box
            # frame
            frame_check_box = customtkinter.CTkFrame(
                frame_up_main, fg_color='#575757')
            frame_check_box.pack(fill="x", padx=50, pady=(15, 15))

            check_box1 = customtkinter.CTkCheckBox(
                frame_check_box, text='Plot chart')
            check_box1.pack(padx=50, pady=(15, 15), side=tk.LEFT)

            check_box2 = customtkinter.CTkCheckBox(
                frame_check_box, text='Bar chart')
            check_box2.pack(padx=50, pady=(15, 15), side=tk.LEFT)

####################################################################################################
            # Create a button which creates the chart

            # frame for create chart button
            frame_create_chart_button = customtkinter.CTkFrame(
                frame_up_main, fg_color='#575757')
            frame_create_chart_button.pack(fill="x", padx=50, pady=(20, 10))

            create_chart_button = tk.Button(
                frame_create_chart_button, text="GENERATE", font=('Times New Roman Bold', 16),  command=generate_chart)
            create_chart_button.pack(fill="x", padx=50, pady=(35, 35))


###########################################################################################
        # function to retrieve the column names for a table


        def get_column_names(table_name):
            self.c.execute(f"PRAGMA table_info({table_name})")
            rows = self.c.fetchall()
            return [row[1] for row in rows]

        # function to retrieve the data for a column in a table
        def get_column_data(table_name, column_name):
            self.c.execute(f"SELECT {column_name} FROM {table_name}")
            rows = self.c.fetchall()
            return [row[0] for row in rows]

        # OK function to create a chart using matplotlib

        def create_chart1(x_data, y_data):
            plt.plot(x_data, y_data)
            plt.show()

        def create_chart(x_data, y_data):
            fig, ax = plt.subplots()
            ax.bar(x_data, y_data)
            plt.show()
##########################################################################################################


############################         search price page                ########################################

        # function to switch to search page


        def search_page():
            frame_search_price = tk.Frame(main_frame)
            frame_search_price.pack(pady=25)
            #############################################################
            # Create treeview csv file

            # add a scrollbar
            my_tree_scroll = Scrollbar(frame_search_price)
            my_tree_scroll.pack(side=RIGHT, fill=Y)

            my_treeview = ttk.Treeview(
                frame_search_price, height=15, yscrollcommand=my_tree_scroll.set)
            my_treeview.pack()

            # configure scrollbar
            my_tree_scroll.config(command=my_treeview.yview)

            ####### set treevew styles ########################
            style = ttk.Style()
            style.theme_use("default")
            # change colors for style
            style.configure("Treeview", background="azure", foreground="black", font=(
                'Bold', 12), rowheight=25, fieldbackground="azure")
            # change color of heders
            style.configure("Treeview.Heading", background="#545454",
                            foreground="white", font=('Bold', 16), padding=(5, 10, 5, 10))
            # column heading heght
            my_treeview.heading('#0', text="\n")

            my_treeview.heading(
                "# 0", text="Search about price", anchor=CENTER)
            # column width
            my_treeview.column("# 0", anchor=CENTER, stretch=NO, width=1200)
            # change color of selected row
            style.map('Treeview', background=[('selected', "green")])

            ################################################################
            ##############################################################

            lb_title_search = tk.Label(frame_search_price, text='Choose your price',
                                       font=('Bold', 15))
            lb_title_search.pack(padx=10, pady=10)

            # Create a select data main_frame
            frame_search = customtkinter.CTkFrame(
                frame_search_price, fg_color='#545454')
            frame_search.pack(fill="x", padx=100)

            #######################################################
            # Create a frame frame_table_name_search up to frame_search
            frame_table_name_search = customtkinter.CTkFrame(
                frame_search, fg_color='azure')
            frame_table_name_search.pack(
                fill="both", padx=20, pady=20, side=tk.LEFT)

            # label for table_name_search
            lb_table_name_search = tk.Label(frame_table_name_search, text='Choose location', bg='azure',
                                            font=('Bold', 15))
            lb_table_name_search.pack(padx=5)

            # Create a combobox to select the table name-location

            # retrieve the options from all tables exclude some
            self.c.execute(
                f'''SELECT name FROM sqlite_master WHERE type='table'AND name NOT IN ('locations', 'users', 'sqlite_sequence')''')
            table_names = [table[0] for table in self.c.fetchall()]

            # 2.combobox
            table_combobox = customtkinter.CTkComboBox(
                frame_table_name_search, values=table_names)
            table_combobox.pack(
                fill="both", padx=5, pady=5, side=tk.LEFT)

            selected_table_names = table_combobox.get()

            # 3.frame
            frame_price_search = customtkinter.CTkFrame(
                frame_search, fg_color='azure')
            frame_price_search.pack(
                fill="both", padx=20, pady=20, side=tk.LEFT)

            # labels
            lb_price_search = tk.Label(frame_price_search, text='Choose price', bg='azure',
                                       font=('Bold', 15))
            lb_price_search.pack(padx=5)

            # 1.query price
            self.c.execute(
                f'''SELECT DISTINCT price FROM {selected_table_names}''')
            prices = [str(row[0]).ljust(10)
                      for row in self.c.fetchall()]

            # 2.combobox price
            price_combobox = customtkinter.CTkComboBox(
                frame_price_search, values=prices)
            price_combobox.pack(
                fill="both", padx=5, pady=5, side=tk.LEFT)

            selected_price = price_combobox.get()

            # Define a function to update the column comboboxes when the table combobox is changed
            def update_column_comboboxes(event):
                # Get the selected table name
                selected_table_names = self.table_combobox.get()
                selected_price = self.price_combobox.get()

                # Update the column comboboxes with the column names for the selected table
                self.price_combobox['values'] = get_price(
                    selected_table_names, selected_price)
                # Update the column comboboxes with the column names for the selected table
                self.table_combobox['values'] = get_table(selected_table_names)

            # Bind the update_column_comboboxes function to the table_combobox event
            table_combobox.bind(
                "<<ComboboxSelected>>", update_column_comboboxes)

        # function to update the table comboboxes with price, when the table combobox is changed

            def my_search(self):
                # Retrieve the selected table name and price value
                selected_table_name = self.table_combobox.get()
                selected_price_value = self.price_combobox.get()

                # Execute the SQL query to fetch the search results
                self.c.execute(
                    f'''SELECT * FROM {selected_table_name} WHERE price=?''', (selected_price_value,))
                rows = self.c.fetchall()

                # Clear the existing items in the my_treeview
                for item in self.my_treeview.get_children():
                    self.my_treeview.delete(item)

                # Insert the search results into the my_treeview
                for row in rows:
                    self.my_treeview.insert("", "end", values=row)

            # frame for create chart button
            frame_search_button = customtkinter.CTkFrame(
                frame_search, fg_color='#575757')
            frame_search_button.pack(fill="x", padx=50, pady=(20, 10))

            search_button = customtkinter.CTkButton(
                frame_search_button, text="Search", font=('Times New Roman Bold', 18), command=my_search)
            search_button.pack(fill="both", padx=50, pady=(20, 10))

        def get_table(selected_table_name):
            self.c.execute(
                f'''SELECT name FROM sqlite_master WHERE type='table'AND name NOT IN ('locations', 'users', 'sqlite_sequence')''')
            selected_table_name = self.c.fetchall()
            return [row[0] for row in selected_table_name]

        # function to retrieve the data for a column in a table
        def get_price(selected_table_name, selected_price_value):
            self.c.execute(f'''SELECT price FROM {selected_table_name}''')
            selected_price_value = self.c.fetchall()
            return [row[0] for row in selected_price_value]

###########################                                 ####################################################
        def parsing_page():
            frame_parsing = tk.Frame(main_frame)
            frame_parsing.pack(pady=25)

            # Create a threading event object to signal when to stop parsing
            stop_event = threading.Event()

            def stop_parsing():
                global stop_event
                stop_event.set()

            def parsing_daft():
                global stop_event

                messagebox.showinfo("Parsing", "Running...")

                # Step 1: Sending a HTTP request to a URL
                baseurl = "https://www.daft.ie/property-for-sale/ireland"

                # do not be banned change proxies
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0.'
                }

                list = []

                # because pages its move increasing to 20, i decide to make range pages to be parsed and calculate page values(nr)
                for num in range(1, 8):
                    page = num*20
                    # for page in range(0, 60):
                    url = f'https://www.daft.ie/property-for-sale/waterford-city?pageSize={page}'
                # Make a GET request to fetch the raw HTML content
                    response = requests.get(url, headers=headers)

                    # Simple check to check if page was blocked (Usually 503)
                    if response.status_code > 500:
                        if "To discuss automated access to web data please contact" in response.text:
                            print(
                                "Page %s was blocked by web admin. Please try using better proxies\n" % url)
                        else:
                            print("Page %s must have been blocked by web admin as the status code was %d" % (
                                url, response.status_code))
                    time.sleep(20)
                    # print(response)
                    # if code response[200] we have acces, we can scraping
                # Step 2: Parse the html content
                    soup = BeautifulSoup(response.content, 'html.parser')
                # found all house list webpage
                    time.sleep(10)
                    houselist = soup.find_all(
                        'li', class_='SearchPage__Result-gg133s-2 djuMQD')
                    # print(len(productlist))
                # Step 3: Analyze the HTML tag, where content lives

                # Create a data dictionary to store the data.
                    for item in houselist:
                        # address 'NoneType'

                        # for product in products:
                        # description_element = product.find('p', class_='sc-kAzzGY kZncUf')
                        # description = description_element.get_text() if description_element else "No Description"

                        address_element = item.find(
                            'p', class_='TitleBlock__Address-sc-1avkvav-8 dzihyY')
                        address = address_element.getText(', ').strip(
                        ) if address_element is not None else 'No Address Found'

                        # price
                        try:
                            price_element = item.find(
                                'span', class_='TitleBlock__StyledSpan-sc-1avkvav-5 fKAzIL')
                            price = price_element.getText(', ').strip(
                            ) if price_element is not None else 'No price Found'

                        except ValueError:
                            price = 0
                        # remove e before price to get clean nr and string to numbers
                        price = price[1:]
                        # pandas to change coma and convert to float, if no price will use try except method
                        try:
                            price = float(price.replace(',', ''))
                        except ValueError:
                            price = 0
                        ####################################################################################################
                        time.sleep(10)
                        # i got all but in one variable
                        bed_bath_floorArea_propertyType = (
                            item.find('div', class_='TitleBlock__CardInfo-sc-1avkvav-10 iCjViR')).getText(', ').strip()

                        try:
                            bed, bath, floorArea, propertyType = bed_bath_floorArea_propertyType.split(
                                ',')
                        except ValueError:
                            bed = 0,
                            bath = 0,
                            floorArea = 0,
                            propertyType = 0,

                        list.append([address, price, bed, bath,
                                    floorArea, propertyType])

                ###################################################################################################
                        # # csv file
                        df = pd.DataFrame(
                            list, columns=['address', 'price', 'bed', 'bath', 'floorArea', 'propertyType'])
                        df.to_csv('Waterford_house.csv')
                    # pause do not be banned
                    time.sleep(20)
                    # print(list)

                    ##############################################################################################
            parsing_btn = customtkinter.CTkButton(
                frame_parsing, text="START", command=run_parsing_file)
            parsing_btn.pack(
                fill="both", padx=10, pady=(100, 50))

        def run_parsing_file():
            try:
                # Run the Python script using subprocess module
                subprocess.Popen(["python", "parsing_file.py"])
            except FileNotFoundError:
                print(
                    "Error: Could not find ult.py. Make sure the file exists in the current directory.")
        #####################################################################################################

            # to switch that pages we need to add a argument page to function indicate and call function page and to buton add download_db_to_csv_page
            #####################################################################################################

        ################# function hide non activate indicators #############################################################################

        def hide_indicate():
            download_db_to_csv_indicate.config(bg='#264848')
            dashboard_indicate.config(bg='#264848')
            search_page_indicate.config(bg='#264848')
            parsing_indicate.config(bg='#264848')

        ############ function to clean pages when take another one using winfo_children method and in indicate function will clean pages###############
        def clean_pages():
            for frame in main_frame.winfo_children():
                frame.destroy()

    ################# function show indicators #############################################################################
        def indicate(lb, page):
            hide_indicate()
            lb.config(bg='azure')
            clean_pages()
            page()
        ##########################        frame options-text left side       ################################################
        ######### frame left options ##################################################################
        # bg color
        options_frame = tk.Frame(root, bg='#264848')
        # alighn left
        options_frame.pack(side=tk.LEFT)
        # pack_propagate(False) to be available for width and hight parameters
        options_frame.pack_propagate(False)
        options_frame.configure(width=250, height=650)
    ########## logo img #########################################################
        logo_img = ImageTk.PhotoImage(file="house_logo3.png")
        logo_widget = tk.Label(options_frame, image=logo_img, bg='#264848')
        logo_widget.image = logo_img
        logo_widget.pack(padx=25, pady=25)

        ######################## text buttons #####################################

        # to hiding indicate label wil change bg for the same color frame
        #  and after will make a function to change another color when its activate

        ############################################ Button download_db_to_csv ##########################################
        # Donwload dataset for csv file
        download_db_to_csv = tk.Button(options_frame, text='Download_CSV', font=('Times New Roman Bold',
                                                                                 18), fg='azure', bd=0, bg='#264848',
                                       command=lambda: indicate(download_db_to_csv_indicate, download_db_to_csv_page))
        download_db_to_csv.place(x=25, y=200)

    # indicate label for download_db_to_csv button and empty text
        download_db_to_csv_indicate = tk.Label(
            options_frame, text='', bg='#264848')
        download_db_to_csv_indicate.place(x=15, y=200, width=5, height=35)

    ############################################ Button Dashboard page #########################################################

        # Generate page_dashboard
        dashboard = tk.Button(options_frame, text='Dashboard', font=('Times New Roman Bold',
                                                                     18), fg='azure', bd=0, bg='#264848',
                              command=lambda: indicate(dashboard_indicate, dashboard_page))
        dashboard.place(x=25, y=250)

        # indicate label for Generate grafic1 button and empty text
        dashboard_indicate = tk.Label(options_frame, text='', bg='#264848')
        dashboard_indicate.place(x=15, y=250, width=5, height=35)

    ############################################ Left Button search_page #########################################################
        # Generate search_page
        search = tk.Button(options_frame, text='Search price', font=('Times New Roman Bold',
                                                                     18), fg='azure', bd=0, bg='#264848',
                           command=lambda: indicate(search_page_indicate, search_page))
        search.place(x=25, y=300)

        # indicate label for Generate grafic1 button and empty text
        search_page_indicate = tk.Label(options_frame, text='', bg='#264848')
        search_page_indicate.place(x=15, y=300, width=5, height=35)
        ########################################################################################################################
        ######################## parsing buton left page ######################################################################
        # Generate page_parsing
        parsing = tk.Button(options_frame, text='Parsing', font=('Times New Roman Bold',
                                                                 18), fg='azure', bd=0, bg='#264848',
                            command=lambda: indicate(parsing_indicate, parsing_page))
        parsing.place(x=25, y=350)

        # indicate label for Generate grafic1 button and empty text
        parsing_indicate = tk.Label(options_frame, text='', bg='#264848')
        parsing_indicate.place(x=15, y=350, width=5, height=35)

        ################################ main_frame- right side grafics display #########################################
        main_frame = tk.Frame(
            root, highlightbackground='#264848', highlightthickness=3)
        # alighn right
        main_frame.pack(side=tk.LEFT)
        # pack_propagate(False) to be available for width and hight parameters
        main_frame.pack_propagate(False)
        main_frame.configure(width=1200, height=650)

        # Looping window
        root. mainloop()


#############################################################################################


    def login(self):
        #  enter and take entry username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # check if username and password no empty
        if username == "" or password == "":
            messagebox.showerror(
                "Login", "Please enter a valid username and password.")
            return
        # query to db and take result
        query = f'''SELECT id, login_count, last_login FROM users WHERE username = ? AND password = ?'''
        result = self.c.execute(query, (username, password)).fetchone()

        # check if not user and password
        if result is None:
            messagebox.showerror("Login", "Invalid username or password.")
        else:

            # call the function main to open app and destroy login form

            self.rootlog.destroy()

            self.main()

#############################################################################################

    def change_password(self, username, password):
        #  enter a username and password
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        new_password = input("Enter your new password: ")

        query = f'''SELECT * FROM users WHERE username = ? AND password = ?'''
        result = self.c.execute(query, (username, password)).fetchone()
        if result is None:
            print("Username not found. Please signup.")
            self.signup()
        else:
            query = f'''UPDATE users SET password = ? WHERE username = ?'''
            result = self.c.execute(query, (new_password, username))
            self.conector.commit()
            print("Password changed successfully.")
##################################################################################
##################################################################################

    def remove_account(self, username, password):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        query = f'''DELETE FROM users WHERE username = ? AND password = ?'''
        result = self.c.execute(query, (username, password))
        self.conector.commit()
        if result.rowcount == 0:
            print("Username or password is incorrect")
        else:
            print("Account removed successfully")

############################################################################################################################
###########################################################################################################################

# close database connection
        self.conector.close()
#############################################################################################################


##########################################################################################################################
db_file = 'daft_db.db'
table_name = 'users'
columns = ["username", "password",  "login_count", "last_login"]

#############################################################################################################################
if __name__ == "__main__":

    # create object with class Database and parameter name db

    login_window = LoginWindow("daft_db.db")


# call method createTable and give data to be created our table
    login_window.createTable('users', [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'username TEXT UNIQUE',
        'password TEXT',
        'login_count INTEGER DEFAULT 0',
        'last_login DATETIME'])
