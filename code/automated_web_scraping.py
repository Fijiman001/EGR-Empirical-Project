from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

# Configure Chrome options for headless execution
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36"
    )

    # Set up the ChromeDriver service
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Function to extract bond data from the current page
def extract_bond_data(soup):
    bond_table = soup.find("div", {"class": "table-responsive"})
    bonds = []

    if bond_table:
        rows = bond_table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                bonds.append(
                    {
                        "Name": cols[0].text.strip(),
                        "WKN": cols[1].text.strip(),
                        "Last Price": cols[2].text.strip(),
                        "Date/Time Last Price": cols[3].text.strip(),
                        "Volume in Euro": cols[4].text.strip(),
                        "+/- %": cols[5].text.strip(),
                        "Coupon": cols[12].text.strip() if len(cols) > 12 else "",
                        "Currency": cols[13].text.strip() if len(cols) > 13 else "",
                        "YTM": cols[14].text.strip() if len(cols) > 14 else "",
                    }
                )
    return bonds

# Core scraping function
def scrape_bonds(url, output_file, page_limit=20):
    driver = configure_driver()
    all_bonds = []
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Click through Cookie Selection
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "cookie-hint-btn-decline"))
        )
        cookie_button.click()
        print("Cookie banner handled successfully (Declined).")

        # Wait for overlay to disapear
        WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".wrapper[_ngcontent-boerse-frankfurt-c97]"))
        )
        print("Overlay disappeared before 100 button")

        # Click the "100" button to show 100 rows per page
        hundred_button = wait.until(
            EC.element_to_be_clickable((By.XPATH,"//button[contains(@class, 'page-bar-type-button') and text()='100']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", hundred_button)
        hundred_button.click()
        time.sleep(10)

        # Wait for overlay to disapear
        WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".wrapper[_ngcontent-boerse-frankfurt-c97]"))
        )
        print("Overlay disappeared before Pages button")

        # Wait for the page to load
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'table-responsive')]")
            )
        )

        # Get total number of pages
        page_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'page-bar-type-button') and not(@disabled)]",
        )
        total_pages = min(
            int(page_buttons[-1].text.strip()), page_limit or float("inf")
        )
        print(f"Total pages: {total_pages}")

        # Loop through pages
        for page in range(1, total_pages + 1):
            try:
                if page != 1:
                    page_button = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                f"//button[contains(@class, 'page-bar-type-button') and text()='{page}']",
                            )
                        )
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", page_button
                    )
                    page_button.click()
                    wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'table-responsive')]")
                        )
                    )

                # Parse current page
                soup = BeautifulSoup(driver.page_source, "html.parser")
                bonds = extract_bond_data(soup)
                all_bonds.extend(bonds)
                print(f"Page {page} scraped successfully.")

            except Exception as page_error:
                print(f"Error on page {page}: {page_error}")
                driver.save_screenshot("error_page.png") # test
                break

        # Save results to CSV
        file_name = f"{output_file}_{timestamp}.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Name",
                "WKN",
                "Last Price",
                "Date/Time Last Price",
                "Volume in Euro",
                "+/- %",
                "Coupon",
                "Currency",
                "YTM",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_bonds)
        print(f"Data saved to {file_name}")

    except Exception as main_error:
        print(f"Critical error: {main_error}")
        driver.save_screenshot("error_main.png") # test

    finally:
        driver.quit()

# Main execution
if __name__ == "__main__":
    # Scrape green bonds
    scrape_bonds(
        url="https://www.boerse-frankfurt.de/anleihen/green-bonds",
        output_file="green_bonds_data",
    )
    # Scrape all bonds (limit to 20 pages)
    scrape_bonds(
        url="https://www.boerse-frankfurt.de/anleihen/most-traded",
        output_file="all_bonds_data",
        page_limit=20,
    )
