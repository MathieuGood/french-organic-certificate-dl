import csv
import requests
import httplib2
from bs4 import BeautifulSoup
import wget
import sys
import os


oc_data = {
    'Ecocert France': ['https://certificat.ecocert.com/', 'download-pdf', ''],
    'Certipaq Bio': ['https://www.certipaq.solutions', '', 'download="" ']
    }


def api_request(siret):
    api_response = requests.get("https://opendata.agencebio.org/api/gouv/operateurs?siret=" + siret)
    json_response = api_response.json()

    # Pretty print the json response
    # import json
    # print(json.dumps(json_response, indent=2))

    return json_response


def dl_page_url(response):
    for result in response['items']:
        oc = result['certificats'][0]['organisme']
        url = result['certificats'][0]['url']
        name = result['raisonSociale']
        return (url, name, oc)


def scrape_page(dl_page):
    http = httplib2.Http()
    content = http.request(dl_page)[1]
    soup = BeautifulSoup(content, features='html.parser')
    # For debugging purpose
    # print(soup)
    return soup


def get_pdf_url(soup, oc):

    class_tag = oc_data[oc][1]
    base_url = oc_data[oc][0]
    prefix = oc_data[oc][2] + 'href="'

    pdf_links = soup.find_all(class_=class_tag)[0]
    pdf_links = str(pdf_links.prettify(formatter=None))
    dl_link = pdf_links.split(prefix)[1].split('"')[0]
    url = base_url + dl_link
    # For debugging purpose
    # print(url)
    return url


def create_file_name(name):
    return name.replace(' ', '_') + '.pdf'


def download_pdf(url, name):
    file = create_file_name(name)
    wget.download(url, file)


def get_certificate(siret):

    response = api_request(siret)

    try:
        if response['nbTotal'] != 0:
            dl_page, name, oc  = dl_page_url(response)
            print(f'{name} certified by {oc}')

            if oc not in oc_data:
                print(f'>>> The Certification company {oc} is not supported on this software')
                print('Follow this link to manually download the certificate :', dl_page, '\n')
            else:
                page = scrape_page(dl_page)
                url = get_pdf_url(page, oc)
                # For debugging purpose
                # print(dl_page)
                # print(page)
                # print(url)
                try:
                    download_pdf(url, './certificates/' + name)
                    print('\n')
                except:
                    print("Can't download file")
    except:
        print('Wrong SIRET value or company not existing in database')
        menu()


def import_csv(csv_name):
    if os.path.isfile(csv_name):
        with open(csv_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            for company in csv_reader:
                get_certificate(company[1])
    else:
        print('File not found')
        return menu()


def menu():
    menu_content = [
        '🌿🌿📜📜 Organic certificate downloader 📜📜🌿🌿',
        'Please choose an option :',
        '(1) Enter SIREN number',
        '(2) Batch download with csv import',
        '(3) Exit program']

    print('\n')

    for line in menu_content:
        print(line)

    menu_choice()


def menu_choice():
    choice = input('Your choice: ')
    if choice == '1':
        get_certificate(input('Enter SIREN number: '))
        menu()
    elif choice == '2':
        import_csv(input('Please enter name of csv file: '))
        menu()
    elif choice == '3':
        print('Bye!')
        sys.exit()
    else:
        print('Wrong value')
        menu_choice()


def main():

    menu()



if __name__ == '__main__':
    main()
