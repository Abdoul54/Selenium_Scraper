import scraper

# Initialiser Chrome driver
driver = scraper.initialize_driver()
cities = [
    'Bouznika',
    'Settat',
    'El Jadida',
    'Mohammedia',
    'Tétouan',
    'Nador',
    'Safi',
    'Béni Mellal',
    'Khouribga',
    'Tanger',
    'Fès',
    'Salé',
    'Kénitra',
    'Meknès',
    'Oujda',
    'Temara',
    'Rabat',
    'Marrakech',
    'Agadir',
]

scraper.scrape(driver, *cities)
