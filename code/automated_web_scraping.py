"""# Packages & Function to Get Data"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
import shutil

# Function to extract bond data from the current page
def extract_bond_data(soup):
    bond_table = soup.find("div", {"class": "table-responsive"})
    bonds = []

    if bond_table:
        rows = bond_table.find_all("tr")  # Get all rows in the table

        # Iterate over each row (skip the header row)
        for row in rows[1:]:
            cols = row.find_all("td")  # Get all columns in the row
            if len(cols) >= 6:  # Ensure there are enough columns
                bond_info = {
                    "Name": cols[0].text.strip(),
                    "WKN": cols[1].text.strip(),
                    "Last Price": cols[2].text.strip(),
                    "Date/Time Last Price": cols[3].text.strip(),
                    "Volume in Euro": cols[4].text.strip(),
                    "+/- %": cols[5].text.strip(),
                    "Coupon": cols[12].text.strip(),
                    "Currency": cols[13].text.strip(),
                    "YTM": cols[14].text.strip()
                }
                bonds.append(bond_info)
    return bonds

"""# Green bond data"""

# Check if Chromedriver is available on system path
shutil.which("chromedriver")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Fallback: Try common locations for Chrome
possible_paths = ["/usr/bin/google-chrome", "/snap/bin/chromium", "/usr/local/bin/google-chrome"]
for path in possible_paths:
    try:
        with open(path) as f:
            chrome_options.binary_location = path
            break
    except FileNotFoundError:
        pass

if not chrome_options.binary_location:
    raise FileNotFoundError("No valid Chrome binary found on the system.")

# Set up the ChromeDriver service
service = Service("/usr/bin/chromedriver")

# Initialize the driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.boerse-frankfurt.de/anleihen/green-bonds"

# Initialize an empty list to store all bonds
all_bonds = []

try:
    # Open the website
    driver.get(url)

    # Wait for the button to be visible
    wait = WebDriverWait(driver, 5)
    hundred_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'page-bar-type-button btn btn-lg ng-star-inserted') and text()='100']"))
    )

    # Click the "100" button
    hundred_button.click()
    time.sleep(5)

    # Find the number of pages
    page_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'page-bar-type-button page-bar-type-button-width-auto btn btn-lg ng-star-inserted') and not(@disabled)]")
    total_pages = int(page_buttons[-1].text.strip())  # Extract the number from the last button, this button should always be showing the maximum amount of pages
    print(f"Total pages: {total_pages}")

    # Loop through all pages, skipping the first one
    for page in range(1, total_pages + 1):
      try:

        # Wait for the page button to be clickable and click it
        if page != 1:
          page_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'page-bar-type-button page-bar-type-button-width-auto btn btn-lg ng-star-inserted') and text()='{page}']"))
          )
          # click next page button
          page_button.click()
          time.sleep(5)  # Allow time for the page to load, check how long is optimal, 2 seconds to be safe

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract data from the current page
        bonds = extract_bond_data(soup)
        all_bonds.extend(bonds)

        # Loop count
        print(f"Loop {page}")

      except Exception as e:
        print(f"An error occurred on page {page}: {e}")
        break  # Exit the loop if there is an error

    # Get the current date and time for the file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"green_bonds_data_{timestamp}.csv"

    # Save all the extracted data to a CSV file
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "WKN", "Last Price", "Date/Time Last Price", "Volume in Euro", "+/- %", "Coupon", "Currency", "YTM"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(all_bonds)  # Write all bond data rows

    print("Bond data has been saved to 'green_bonds_data.csv'")

except Exception as e:
    print(f"Critical error: {e}")

    # Get the current date and time for the file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"green_bonds_partial_data_{timestamp}.csv"

    # Save the collected data so far
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "WKN", "Last Price", "Date/Time Last Price", "Volume in Euro", "+/- %", "Coupon", "Currency", "YTM"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(all_bonds)  # Write collected bond data rows so far

    print("Partial bond data has been saved to 'green_bonds_partial_data.csv'")

finally:
    # Close the browser
    driver.quit()

"""# All Bonds"""

# Check if Chromedriver is available on system path
shutil.which("chromedriver")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Fallback: Try common locations for Chrome
possible_paths = ["/usr/bin/google-chrome", "/snap/bin/chromium", "/usr/local/bin/google-chrome"]
for path in possible_paths:
    try:
        with open(path) as f:
            chrome_options.binary_location = path
            break
    except FileNotFoundError:
        pass

if not chrome_options.binary_location:
    raise FileNotFoundError("No valid Chrome binary found on the system.")

# Set up the ChromeDriver service
service = Service("/usr/bin/chromedriver")

# Initialize the driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.boerse-frankfurt.de/anleihen/most-traded"

# Initialize an empty list to store all bonds
all_bonds = []

try:
    # Open the website
    driver.get(url)
    
    # Wait for the button to be visible
    wait = WebDriverWait(driver, 10)
    hundred_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'page-bar-type-button btn btn-lg ng-star-inserted') and text()='100']"))
    )

    # Click the "100" button
    hundred_button.click()
    time.sleep(5)

    # Find the number of pages
    page_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'page-bar-type-button page-bar-type-button-width-auto btn btn-lg ng-star-inserted') and not(@disabled)]")
    total_pages = int(page_buttons[-1].text.strip())  # Extract the number from the last button, this button should always be showing the maximum amount of pages
    print(f"Total pages: {total_pages}")

    # Loop through all pages, skipping the first one, limiting to 20 pages, so the 2000 most traded bonds
    for page in range(1, min(total_pages + 1, 21)):
      try:

        # Wait for the page button to be clickable and click it
        if page != 1:
          page_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'page-bar-type-button page-bar-type-button-width-auto btn btn-lg ng-star-inserted') and text()='{page}']"))
          )
          # Allow time for scroll to complete
          page_button.click()
          time.sleep(5)  # Allow time for the page to load, check how long is optimal

        # Extract page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract data from the current page
        bonds = extract_bond_data(soup)
        all_bonds.extend(bonds)

        # Loop count
        print(f"Loop {page}")

      except Exception as e:
        print(f"An error occurred on page {page}: {e}")
        break  # Exit the loop if there is an error

    # Get the current date and time for the file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"all_bonds_data_{timestamp}.csv"

    # Save all the extracted data to a CSV file
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "WKN", "Last Price", "Date/Time Last Price", "Volume in Euro", "+/- %", "Coupon", "Currency", "YTM"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(all_bonds)  # Write all bond data rows

    print("Bond data has been saved to 'all_bonds_data.csv'")

except Exception as e:
    print(f"Critical error: {e}")

    # Get the current date and time for the file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"all_bonds_partial_data_{timestamp}.csv"

    # Save the collected data so far
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "WKN", "Last Price", "Date/Time Last Price", "Volume in Euro", "+/- %", "Coupon", "Currency", "YTM"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(all_bonds)  # Write collected bond data rows so far

    print("Partial bond data has been saved to 'all_bonds_partial_data.csv'")

finally:
    # Close the browser
    driver.quit()