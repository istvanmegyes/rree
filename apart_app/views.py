from contextlib import nullcontext
from operator import contains
from pprint import pprint
from unicodedata import decimal
from django.shortcuts import render
import pandas as pd
import numpy as np
from sqlalchemy import column
from apart_app.models import Apartment
from apart_app.models import Vertical
from django.http import HttpResponse
from datetime import datetime
from apart_app import conversion as cv

now = str(datetime.now())[0:19]


def get_html_content(url):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(url).text
    return html_content
# Create your views here.


def searchform(request):

    apartments = None
    apartments_vertical = []

    header = ['id', 'price', 'floorspace', 'numberOfRooms', 'conditionOfTheRealEstate', 'yearOfConsttruction',
              'conveniences', 'energyPerformanceCertificate', 'floor', 'buildingLevels', 'lift', 'interiorHeight',
              'heating', 'airCondittioner', 'overhead', 'accessibility', 'bathroomAndToilet', 'orientation', 'view',
              'balconySize', 'gardenConnection', 'attic', 'parking', 'parkingSpacePrice', ]
    measure = ['', 'forint', 'm2', 'szoba', '', 'év',
               '', '', 'emelet', 'szintek', '', 'm',
               '', '', 'forint', '', '', '', '',
               'm2', '', 'm2', '', 'forint', ]

    column_names = ['id', 'date', 'attribute', 'value', 'measure']

    verticals = []
    #header_vertical = ['id', 'key', 'value', 'measure', 'date']

    if 'vertical' in request.GET:

        vertical_matrix = []
        vertical_line = []

        with open(f'verticals_{now}.txt', 'r') as f:
            for line in f.readlines():
                vertical_line = line.split(';')
                vertical_matrix.append(vertical_line)

        verticals = {idx + 1: vertical_matrix[idx]
                     for idx in range(len(vertical_matrix))}

        # print(verticals)

        return render(request, 'templates/verticals.html', {'verticals': verticals})

    elif 'url' in request.GET:
        url_base = request.GET.get('url')
        html_content = get_html_content(url_base)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        apartments = dict()
        apartment_url_list = []

        result_count = soup.find(
            'span', attrs={'class': 'results__number__count'}).text
        result_count = result_count.replace(' ', '')
        page_count = (int(result_count) - (int(result_count) % 20)) / 20 + 1

        # ----------------

        for page in range(1, int(page_count) + 1):
            url_actual = url_base + "?page=" + str(page)
            # print(url_actual+'\n')
            html_content = get_html_content(url_actual)
            soup = BeautifulSoup(html_content, 'html.parser')

            for item in soup.find_all("a", href=True):
                if "/elado+lakas/" in item["href"]:
                    if item["href"] not in apartment_url_list:
                        apartment_url_list.append(item["href"])
                        # print(item["href"])
            # print('\n')

        # ----------------

        for apartment in apartment_url_list:
            html_content = get_html_content("https://ingatlan.com" + apartment)
            soup = BeautifulSoup(html_content, 'html.parser')

            apartment_data = dict()
            apartment_data_vertical = []

            apartment_data[header[0]] = apartment[-8:]  # ID

            price_span = soup.find(
                'span', attrs={'class': 'fw-bold fs-5 text-nowrap'})
            price = price_span.find('span').text
            apartment_data[header[1]] = price  # PRICE

            # ----< VERTICALS >----
            apartment_data_vertical.append(apartment[-8:])  # id
            apartment_data_vertical.append(str(datetime.now())[0:19]) # date
            apartment_data_vertical.append(header[1])  # key
            apartment_data_vertical.append(str(int(float((price.split(' ')[0]).replace(',', '.')) * 1000000)))
            apartment_data_vertical.append(measure[1])  # measure

            verticals.append(apartment_data_vertical)
            apartment_data_vertical = []
            # ----< VERTICALS >----

            area_datas = soup.find_all('span', attrs={'fw-bold fs-5'})

            index = 2
            for area_data in area_datas:
                apartment_data[header[index]] = ((area_data.text).strip().replace(
                    '\n', ''))  # FLOORSPACE, NUMBEROF ROOMS
                # ----< VERTICALS >----

                apartment_data_vertical.append(apartment[-8:])  # id
                apartment_data_vertical.append(str(datetime.now())[0:19])  # date
                apartment_data_vertical.append(header[index])  # key
                apartment_data_vertical.append(apartment_data[header[index]].split(' ')[0])
                apartment_data_vertical.append(measure[index])  # measure

                verticals.append(apartment_data_vertical)
                apartment_data_vertical = []
                # ----< VERTICALS >----
                index += 1

            table = soup.find(
                'table', attrs={'class': 'd-md-none table table-borderless d-print-none'})
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                tds = row.find_all('td', attrs={'class': 'fw-bold'})
                for td in tds:
                    apartment_data[header[index]] = (
                        (td.text).strip().replace('\n', '').replace("   ", ''))
                    # ----< VERTICALS >----

                    apartment_data_vertical.append(apartment[-8:])  # id
                    apartment_data_vertical.append(str(datetime.now())[0:19])  # date
                    apartment_data_vertical.append(header[index])  # key
                    apartment_data_vertical.append(apartment_data[header[index]])  # value
                    apartment_data_vertical.append(measure[index])  # measure


                    verticals.append(apartment_data_vertical)
                    apartment_data_vertical = []
                    # ----< VERTICALS >----
                    index += 1

            # print(apartment_data,'\n')

            apartments[apartment_data[header[0]]] = apartment_data


            # with open(f'verticals_{now}.txt', 'a') as f:
            #     for data in apartment_data_vertical:
            #         f.writelines(data)
        # ----------------
        pass
        for item in verticals:
            print(item)
            

        apartment_data_vertical_dataFrame = pd.DataFrame(
            verticals, index=range(len(verticals)), columns=column_names)
        ranked_apartment_data = cv.start_conversion(
            apartment_data_vertical_dataFrame)

        print(ranked_apartment_data)

    return render(request, 'templates/searchform.html', {'apartments': apartments})

# ---------------------------------
