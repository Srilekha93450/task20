# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Path to the msedgedriver executable
# EDGE_DRIVER_PATH = r'C:\Users\WELCOME\Downloads\edgedriver_win64\msedgedriver.exe'

# # Initialize Microsoft Edge WebDriver
# edge_service = EdgeService(executable_path=EDGE_DRIVER_PATH)
# edge_options = webdriver.EdgeOptions()
# driver = webdriver.Edge(service=edge_service, options=edge_options)

# try:
#     # Open the Cowin website
#     driver.get("https://www.cowin.gov.in")
#     driver.maximize_window()

#     # Wait for the "FAQ" link to be clickable and then click it
#     faq_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'FAQ')]"))
#     )
#     faq_link.click()

#     # Wait for the "Partners" link to be clickable and then click it
#     partners_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Partners')]"))
#     )
#     partners_link.click()

#     # Wait a bit for the new windows to open
#     time.sleep(2)

#     # Get all window handles
#     all_handles = driver.window_handles

#     # Display window handles
#     for handle in all_handles:
#         print("Window Handle:", handle)

#     # Close the new windows and switch back to the main window
#     main_window = driver.current_window_handle
#     for handle in all_handles:
#         if handle != main_window:
#             driver.switch_to.window(handle)
#             driver.close()

#     # Switch back to the main window (homepage)
#     driver.switch_to.window(main_window)
#     print("Back to the main window:", main_window)

# finally:
#     # Close the browser window
#     driver.quit()

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the msedgedriver executable
EDGE_DRIVER_PATH = r'C:\Users\WELCOME\Downloads\edgedriver_win64\msedgedriver.exe'

# Initialize Microsoft Edge WebDriver
edge_service = EdgeService(executable_path=EDGE_DRIVER_PATH)
edge_options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=edge_service, options=edge_options)

# Function to download a file
def download_file(url, folder_path, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_path, file_name), 'wb') as file:
            file.write(response.content)

try:
    # Open the URL
    driver.get("https://labour.gov.in/")
    driver.maximize_window()

    # Wait until the page is fully loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Task 1: Download the Monthly Progress Report from 'Documents' menu
    documents_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Documents"))
    )
    documents_menu.click()

    # Wait until the Monthly Progress Report link is clickable
    monthly_progress_report = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Monthly Progress Report"))
    )
    monthly_progress_report.click()

    # Find the download link and download the report
    download_link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'MonthlyProgressReport')]"))
    )
    report_url = download_link.get_attribute('href')
    print(f"Report URL: {report_url}")  # Debugging line
    download_file(report_url, '.', 'MonthlyProgressReport.pdf')

    print("Monthly Progress Report downloaded successfully.")

    # Task 2: Download 10 photos from 'Media' > 'Photo Gallery'
    media_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Media"))
    )
    media_menu.click()

    photo_gallery_submenu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Photo Gallery"))
    )
    photo_gallery_submenu.click()

    # Wait for photos to load and find the photo elements
    photo_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'view-content')]//img"))
    )

    # Create a folder to store the photos
    folder_path = 'PhotoGallery'
    os.makedirs(folder_path, exist_ok=True)

    # Download the first 10 photos
    for i, photo in enumerate(photo_elements[:10]):
        photo_url = photo.get_attribute('src')
        file_name = f"photo_{i + 1}.jpg"
        print(f"Downloading {photo_url} as {file_name}")  # Debugging line
        download_file(photo_url, folder_path, file_name)

    print("Downloaded 10 photos from the Photo Gallery.")

finally:
    # Close the browser window
    driver.quit()

