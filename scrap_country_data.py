import requests
from bs4 import BeautifulSoup

def scrape_country_codes():
    url = 'https://gadm.org/download_country.html'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    select_element = soup.find('select', {'id': 'countrySelect'})
    country_codes = {}
    if select_element:
        options = select_element.find_all('option')
        for option in options:
            value = option['value']
            if value:
                code = value.split('_')[0]
                country_name = option.text
                country_codes[code] = country_name
    return country_codes

def download_geographic_data(country_codes):
    base_url = 'https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_{}.gpkg'
    for code in country_codes:
        url = base_url.format(code)
        filename = f'gadm41_{code}.gpkg'
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'File {filename} is downloaded successfully!')
        else:
            print(f'Failed to download {filename}.')

codes = scrape_country_codes()
download_geographic_data(codes)