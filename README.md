# Daft Property Data Parsing and Analysis

This repository contains a Python application designed to fetch and analyze property data from the Daft website, a popular Irish property listing site. The application uses web scraping techniques to extract property data, which is then stored in a SQLite database for further analysis.

## Features

- Fetch property data from the Daft website based on selected county.
- Store fetched data in a SQLite database.
- Analyze the fetched data.
- Display the results in a user-friendly GUI.

## Technologies Used

- Python
- SQLite
- Tkinter for GUI
- BeautifulSoup for web scraping
- Pandas for data manipulation
- Requests for HTTP requests

## How to Run

1. Clone the repository.
2. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the main Python script:
    ```bash
    python main.py
    ```
4. Select a county from the dropdown menu in the GUI.
5. Click the "Fetch Data" button to start fetching data.
6. Click the "Stop" button to stop fetching data.
7. The results will be displayed in the text box in the GUI.

## Note

The fetching process may take a while depending on the number of pages to fetch. Please be patient and do not close the application while fetching is in progress.

## Future Improvements

- Add more analysis features.
- Improve the GUI design.
- Handle potential errors and exceptions more gracefully.

## Disclaimer

This project is for educational purposes only. Please respect the Daft website's terms of use and do not use this project to overload or disrupt their services.
