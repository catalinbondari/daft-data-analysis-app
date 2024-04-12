# Daft.ie Property Data Analysis App
This project aims to scrape property listing data from the popular Irish property website Daft.ie, clean and store the data, and provide a user-friendly graphical interface for analyzing and visualizing the data.

## Features
- Web scraping of property listings from Daft.ie using Python's BeautifulSoup and Requests libraries
- Handling of broken links during scraping process with try-except blocks
- Data cleaning and preprocessing
- Saving scraped data to CSV files
- User authentication system with login and registration functionality
- Storing scraped data in a database
- Graphical user interface (GUI) built with Tkinter for data visualization and analysis
- Interactive dashboard for generating customizable charts and graphs based on location, price range, and other filters
- Price range search functionality
- Parsing button to parse data in real-time
- CSV file cleaning functionality to remove zeros or other unwanted values

## Usage
Upon launching the application, you will be prompted to log in or register a new account.
After successful authentication, the main interface will be displayed.
Use the menu buttons on the left to navigate through different functionalities, such as downloading CSV files, cleaning data, uploading data to the database, and accessing the dashboard.
In the dashboard, select the desired location, y-axis, x-axis, and chart type, then click "Generate" to visualize the data.
The "Search Price" section allows you to filter property listings by location and price range.
Use the "Parsing" button to parse data in real-time from the Daft.ie website.
The "Clean CSV File" button allows you to remove zeros or other unwanted values from the CSV file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
The Daft.ie website for providing property listing data.
The Python community for the libraries and resources used in this project.
