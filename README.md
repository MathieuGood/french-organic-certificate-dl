# French Organic Certificate Downloader

### Download official certificates of French companies that produce/market organic products

This program is intended for companies that work with other companies producing/selling organic food products. It automatically retrieves the Organic Certificate of the different suppliers and partners that are needed when the company is audites. The key used to identify the company is the SIREN or SIRET number (French national company unique identification number).

## Features
* Download a single certificate entering manually the company's SIREN/SIRET number
* Batch download multiple certificates using a csv formatted list

## Starting the application
* Download the whole GitHub repository to your computer using `git clone https://github.com/MathieuGood/french-organic-certificate-dl.git`
* Install the required libraries with `pip install -r requirements.txt`
* Launch the app typing `python project.py` in your terminal


## Download single certificate from SIREN/SIRET number
* Enter `1` at menu prompt.
* Enter the company's either SIREN or SIRET number.
* Certificate is downloaded in the `certificates` directory

## Batch download multiple certificates using a csv formatted list
* Each line of the csv file should contain the company name and SIREN/SIRET number in the following format : `"Company name", 123456789`
* Place the csv file in the app folder (for testing purpose, the example file `suppliers.csv` is provided with the program)
* Enter `2` at menu prompt
* Enter the name of the csv file to use (do not forget the extension)
* All certificates are downloaded in the `certificates` directory


## Supported Certification Companies
This software only supports Ecocert France and Certipaq France as Certification Companies for automatic download. If a different operator is detected, the program will provide the user with the link to the download page so the PDF file can be retrieved manually.

**Feature coming in next version**: The possibility to retrieve certificates from Bureau Veritas is currently under development and will be shortly added to this program