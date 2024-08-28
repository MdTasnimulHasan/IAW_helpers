import os
import sys
import requests
import json
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


# Suppress unnecessary logging
os.environ['WDM_LOG_LEVEL'] = '0'

# Create downloads directory
download_dir = 'downloaded-files'
os.makedirs(download_dir, exist_ok=True)



import json
import os
import shutil

# Specify the path to your JSON file
file_path = 'E:/Tasnim/PhD_Project/IAW_3D_CAD_file_retrieval/IKEAAssemblyInTheWildDataset.json'
DATASET_DIR = os.path.join(os.getcwd(),'dataset') # D:\IKEAAssemblyInTheWildDataset\dataset

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')  # Only show fatal errors
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        service = Service(ChromeDriverManager(log_level=0).install())
    except TypeError:
        service = Service(ChromeDriverManager().install())
    
    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    sys.stderr = original_stderr
    
    return driver

def get_product_details(url):
    driver = get_chrome_driver()
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'title'))
        )
        
        title = driver.title
        if title:
            full_title = title.strip()
            name_color = full_title.split(' - IKEA')[0]
            match = re.match(r'(.*?),\s*(.*)', name_color)
            if match:
                name, color = match.groups()
            else:
                name = name_color
                color = "Default"
        else:
            name = "Unknown"
            color = "Unknown"
        
        try:
            script = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'pip-xr-viewer-model'))
            )
            if script:
                try:
                    data = json.loads(script.get_attribute('innerHTML'))
                    glb_url = data.get('url')
                    return name, color, glb_url
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for {url}")
        except TimeoutException:
            print(f"GLB model script not found for {url}")
        
    except TimeoutException:
        print(f"Timeout while loading page: {url}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
    finally:
        driver.quit()
    
    return name, color, None

def download_glb(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            progress_bar.update(size)

def main():

    if os.path.exists(DATASET_DIR):
            shutil.rmtree(DATASET_DIR)
            print(f"Removed existing directory: {DATASET_DIR}")

    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)


    # Now 'data' contains the content of the JSON file as a Python dictionary
    print(len(data)) # 420

    success_count = 0
    failure_count = 0

    for c in range (0, len(data), 1):
        print(f'Processing: {c} out of: {len(data)}')
        # print(data[0].keys())
        '''
        "id": "s79011430",
        "name": "KIVIK",
        "category": "Furniture",
        "subCategory": "Sofas",
        "pipUrl": "https://www.ikea.com/au/en/p/glostad-2-seat-sofa-knisa-medium-blue-00488821/"
        '''

        cad_link = data[c]['pipUrl']
        print(cad_link)
       
        cad_path = os.path.join(DATASET_DIR, data[c]['category'], data[c]['subCategory'], data[c]['id'], '3D_model')
        print(cad_path)
        # print(video_path) # D:\IKEAAssemblyInTheWildDataset\dataset\Furniture\Sofas\s79011430\video\eJcsxzPKO-U.mp4

        os.makedirs(cad_path, exist_ok=True)


        
        url = cad_link
        
        name, color, glb_url = get_product_details(url)
        if glb_url:
            filename = f"{name} - {color}.glb"
            filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid characters
            full_path = os.path.join(cad_path, filename)
            download_glb(glb_url, full_path)
            print(f"Downloaded {filename} successfully.")
            success_count += 1
        else:
            print("No GLB file found for the provided URL.")
            failure_count += 1
        
    print("total downloaded: ", success_count)
    print("total failed to downloaded: ", failure_count)

if __name__ == "__main__":
    main()








