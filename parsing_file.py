import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sqlite3
import threading
import subprocess
import customtkinter  # <- import the CustomTkinter module

# Global variable to control fetching process
stop_event = threading.Event()


def show_loading_window():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_label = tk.Label(
        loading_window, text="Fetching data, please wait...")
    loading_label.pack(padx=20, pady=10)
    return loading_window


def hide_loading_window(window):
    window.destroy()


def fetch_data():
    stop_event.clear()  # Reset stop event flag

    # Function to run in a separate thread
    def fetch_in_background():
        loading_window = show_loading_window()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0.'
        }

        # Get the selected country and convert to lowercase
        country = country_var.get().lower()
        data = []  # list to store the fetched data
        seen_addresses = set()  # Set to store unique addresses encountered

        for num in range(1, 12):  # Adjusted range for 11 pages
            if stop_event.is_set():  # Check if stop button is pressed
                break

            page = num * 11
            # Adjusted URL
            url = f'https://www.daft.ie/property-for-sale/{country}?from={page}&pageSize=20'
            response = requests.get(url, headers=headers)

            result_text.insert(
                tk.END, f"Page {num} Response Status: {response.status_code}\n")

            if response.status_code > 500:
                if "To discuss automated access to web data please contact" in response.text:
                    result_text.insert(
                        tk.END, f"Page {num} was blocked by web admin. Please try using better proxies\n")
                else:
                    result_text.insert(
                        tk.END, f"Page {num} must have been blocked by web admin as the status code was {response.status_code}\n")
                continue  # Skip processing this page

            soup = BeautifulSoup(response.content, 'html.parser')
            houselist = soup.find_all(
                'li', class_='SearchPagestyled__Result-v8jvjf-2 iWPGnb')

            for item in houselist:
                address_element = item.find(
                    'h2', class_='TitleBlock__Address-sc-1avkvav-8 dzihyY')
                address = address_element.getText(
                    ', ').strip() if address_element else 'No Description'

                # Check if the address is repeating, if so, skip parsing for this address
                if address in seen_addresses:
                    continue
                seen_addresses.add(address)

                price_element = item.find(
                    'h3', class_='TitleBlock__StyledCustomHeading-sc-1avkvav-5 blbeVq')
                price_text = price_element.getText(', ').strip()[1:].replace(
                    ',', '') if price_element else 'Price on Application'

                # Handle 'Price on Application' or other non-numeric values
                if price_text == 'Price on Application' or not price_text.replace('.', '').isdigit():
                    price = None  # Set price to None if it's not a numeric value
                else:
                    # Convert to float if it's a numeric value
                    price = float(price_text)

                bed_bath_floorArea_propertyType_element = item.find(
                    'div', class_='TitleBlock__CardInfo-sc-1avkvav-10 iCjViR')

                if bed_bath_floorArea_propertyType_element:
                    bed_bath_floorArea_propertyType = bed_bath_floorArea_propertyType_element.getText(
                        ', ').strip()
                    split_result = bed_bath_floorArea_propertyType.split(',')
                    if len(split_result) >= 4:
                        bed, bath, floorArea, propertyType = split_result
                    else:
                        bed, bath, floorArea, propertyType = 0, 0, 0, 0
                else:
                    bed, bath, floorArea, propertyType = 0, 0, 0, 0

                data.append([country, address, price, bed,
                             bath, floorArea, propertyType])

                result_text.insert(tk.END, f"Address: {address}\n")
                result_text.insert(tk.END, f"Price: {price}\n")
                result_text.insert(tk.END, f"Bedrooms: {bed}\n")
                result_text.insert(tk.END, f"Bathrooms: {bath}\n")
                result_text.insert(tk.END, f"Floor Area: {floorArea}\n")
                result_text.insert(
                    tk.END, f"Property Type: {propertyType}\n\n")

                time.sleep(10)  # Sleep after each page fetch

        hide_loading_window(loading_window)

        if not stop_event.is_set():
            # Write to CSV file inside the loop
            df = pd.DataFrame(data, columns=[
                'country', 'address', 'price', 'bed', 'bath', 'floorArea', 'propertyType'])
            # Include country name in CSV file name
            df.to_csv(f'parsing_house_{country}.csv', index=False)

            result_text.insert(tk.END, "All done!\n")

    # Start the thread
    threading.Thread(target=fetch_in_background).start()


def stop_fetching_data():
    global stop_event
    stop_event.set()  # Set stop event flag
    result_text.insert(tk.END, "Parsing was stopped by the user\n")
    root.quit()
    # root.destroy()


# Function to fetch country names from the database


def get_countries():
    conn = sqlite3.connect('daft_db.db')
    c = conn.cursor()
    c.execute("SELECT location_name FROM locations")
    countries = c.fetchall()
    conn.close()
    return [country[0] for country in countries]


# Create a Tkinter window
# customize
# Modes: system (default), light, dark
customtkinter.set_appearance_mode("Dark")

# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

# main window - root
# root = tk.Tk()
root = customtkinter.CTk()
root.eval('tk::PlaceWindow . center')
root.geometry('1150x550+300+100')

root.title("Web Data Fetcher")
root.pack_propagate(False)

# Set background color for main page
root.configure(bg="#575757")


# Country Selector
country_label = ttk.Label(root, text="Choose Country:",
                          font=("Arial", 12, "bold"))
country_label.pack(fill="both", pady=5)
country_var = tk.StringVar()
country_var.set("sligo")  # Default value

country_selector = ttk.Combobox(
    root, textvariable=country_var, values=get_countries(), font=("Arial", 12, "bold"))
country_selector.pack(
    padx=10, pady=(10, 5))

# Fetch Button
fetch_button = customtkinter.CTkButton(
    root, text="Fetch Data", command=fetch_data)
fetch_button.pack(padx=5, pady=(5, 5))

# Stop Button
stop_button = customtkinter.CTkButton(
    root, text="Stop", command=stop_fetching_data)
stop_button.pack(padx=5, pady=(5, 5))

##############################################################################################

#####################################################################################################


# Result Text
result_label = ttk.Label(
    root, text="Results:",  font=("Arial", 12, "bold"))
result_label.pack(padx=5, pady=5, ipadx=15, ipady=15,
                  anchor="center")


result_text = tk.Text(root, height=20, width=100,
                      bg="azure", fg="black", font=("Arial", 12, "bold"))
result_text.pack(padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
