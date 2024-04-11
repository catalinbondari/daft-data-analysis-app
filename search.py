def my_search(selected_table_name, selected_price_value, my_treeview, c):
    # Execute the SQL query to fetch the search results
    c.execute(
        f'''SELECT * FROM {selected_table_name} WHERE price=?''', (selected_price_value,))
    rows = c.fetchall()

    # Clear the existing items in the my_treeview
    for item in my_treeview.get_children():
        my_treeview.delete(item)

    # Insert the search results into the my_treeview
    for row in rows:
        my_treeview.insert("", "end", values=row)


def update_column_comboboxes(event, table_combobox, price_combobox, get_price, get_table):
    # Get the selected table name
    selected_table_name = table_combobox.get()

    # Update the column comboboxes with the column names for the selected table
    price_combobox['values'] = get_price(selected_table_name)
    table_combobox['values'] = get_table(selected_table_name)


def search_page(self):
    frame_search_price = tk.Frame(self.main_frame)
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

    # Define a function to update the column comboboxes when the table combobox is changed
    table_combobox.bind("<<ComboboxSelected>>", lambda event: update_column_comboboxes(
        event, table_combobox, price_combobox, get_price, get_table))

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

    # frame for create chart button
    frame_search_button = customtkinter.CTkFrame(
        frame_search, fg_color='#575757')
    frame_search_button.pack(fill="x", padx=50, pady=(20, 10))

    search_button = customtkinter.CTkButton(
        frame_search_button, text="Search", font=('Times New Roman Bold', 18), command=lambda: my_search(selected_table_names, selected_price, my_treeview, self.c))
    search_button.pack(fill="both", padx=50, pady=(20, 10))


def get_table(selected_table_name, c):
    c.execute(
        f'''SELECT name FROM sqlite_master WHERE type='table'AND name NOT IN ('locations', 'users', 'sqlite_sequence')''')
    selected_table_name = c.fetchall()
    return [row[0] for row in selected_table_name]

# function to retrieve the data for a column in a table


def get_price(selected_table_name, c):
    c.execute(f'''SELECT price FROM {selected_table_name}''')
    selected_price_value = c.fetchall()
    return [row[0] for row in selected_price_value]
