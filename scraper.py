import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import JavascriptException
from pymongo import MongoClient

# Charger la configuration à partir d'un fichier JSON
with open('config.json') as config_file:
    config = json.load(config_file)

# Configurer les journaux
logging.basicConfig(filename='scraping.log', level=logging.INFO)


def initialize_driver():
    # Configurer les options de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter Chrome en mode headless

    # Définir le chemin du pilote Chrome en fonction de la configuration
    chrome_driver_path = config['chrome_driver_path']

    # Initialiser Chrome Driver
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options)
    return driver


def scrape_jobs(driver, *cities):
    data = []
    try:
        for city in cities:
            driver.get(
                f'https://www.avito.ma/fr/{city}/emploi_et_services-%C3%A0_vendre')

            for i in range(1, 31):
                try:
                    title_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > h3 > span');")
                    link_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a')")
                    localisation_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > div > div:nth-child(2) > span');")
                    type_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > p')")
                    if title_element is not None:
                        title = title_element.text
                        link = link_element.get_attribute('href')
                        localisation = localisation_element.text
                        typeV = type_element.text
                        price_element = driver.execute_script(
                            f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > div > span > div > span:nth-child(1)');")

                        data.append(
                            {
                                "Category": "Job",
                                "Title": title,
                                "Price": price_element.text.replace(',', '') if price_element is not None else 0,
                                "link": link,
                                "localisation": localisation,
                                "type": typeV,
                                "platform": "www.avito.ma"
                            })
                    else:
                        continue
                except JavascriptException:
                    break
            print(f'Scraping jobs in {city}: DONE !')
        save_data_to_database(data)
        driver.quit() # Fermer Chrome Driver
    except Exception as e:
        logging.error("An error occurred while scraping jobs: %s", str(e))


def scrape_properties(driver, *cities):
    data = []
    try:
        for city in cities:
            driver.get(
                f'https://www.avito.ma/fr/{city}/immobilier-%C3%A0_vendre')

            for i in range(1, 31):
                try:
                    title_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > h3 > span');")
                    link_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a')")
                    localisation_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > div > div:nth-child(2) > span');")
                    image_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-jejop8-4.gLljJq > div > div > img')")
                    type_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > p')")

                    if title_element is not None:
                        title = title_element.text
                        link = link_element.get_attribute('href')
                        image = image_element.get_attribute('src')
                        localisation = localisation_element.text
                        typeV = type_element.text
                        price_element = driver.execute_script(
                            f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > div > span > div > span:nth-child(1)');")

                        data.append(
                            {
                                "Category": "Property",
                                "Title": title,
                                "Price": price_element.text.replace(',', '') if price_element is not None else 0,
                                "link": link,
                                "localisation": localisation,
                                "image": image,
                                "type": typeV,
                                "platform": "www.avito.ma"
                            })
                    else:
                        continue
                except JavascriptException:
                    break
            print(f'Scraping properties in {city}: DONE !')
        save_data_to_database(data)
        driver.quit() # Fermer Chrome Driver
    except Exception as e:
        logging.error(
            "An error occurred while scraping properties: %s", str(e))


def scrape_vehicles(driver, *cities):
    data = []
    try:
        for city in cities:
            driver.get(
                f'https://www.avito.ma/fr/{city}/v%C3%A9hicules-%C3%A0_vendre')

            for i in range(1, 31):
                try:
                    title_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > h3 > span');")
                    link_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a')")
                    localisation_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > div > div:nth-child(2) > span');")
                    image_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-jejop8-4.gLljJq > div > div > img')")
                    type_element = driver.execute_script(
                        f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(2) > p')")

                    if title_element is not None:
                        title = title_element.text
                        link = link_element.get_attribute('href')
                        image = image_element.get_attribute('src')
                        localisation = localisation_element.text
                        typeV = type_element.text
                        price_element = driver.execute_script(
                            f"return document.querySelector('#__next > div > main > div > div:nth-child(6) > div.sc-1lz4h6h-0.gzFzOo > div > div.sc-1nre5ec-1.fzpnun.listing > div:nth-child({i}) > a > div.sc-ibbrkc-0.sc-jejop8-9.feyxCM.hjXlHz > div:nth-child(1) > div > span > div > span:nth-child(1)');")

                        data.append(
                            {
                                "Category": "Vehicle",
                                "Title": title,
                                "Price": price_element.text.replace(',', '') if price_element is not None else 0,
                                "link": link,
                                "localisation": localisation,
                                "image": image,
                                "type": typeV,
                                "platform": "www.avito.ma"
                            })
                    else:
                        continue
                except JavascriptException:
                    break
            print(f'Scraping vehicles in {city}: DONE !')
        save_data_to_database(data)
        driver.quit() # Fermer Chrome Driver
    except Exception as e:
        logging.error("An error occurred while scraping vehicles: %s", str(e))


def save_data_to_database(data):
    try:
        # Se connecter à la base de données MongoDB
        client = MongoClient(config['mongodb_connection_string'])
        db = client[config['mongodb_database_name']]

        # Insérer les données dans la collection
        db.Posts.insert_many(data)
        print("Data inserted successfully")
        
        # Fermer la connexion à la base de données
        client.close()
    except Exception as e:
        logging.error(
            "An error occurred while saving data to the database: %s", str(e))
