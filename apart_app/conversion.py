import pandas as pd
import os
import numpy as np
from scipy.stats import rankdata

header = ['price', 'floorspace', 'numberOfRooms', 'conditionOfTheRealEstate', 'yearOfConsttruction',
              'conveniences', 'energyPerformanceCertificate', 'floor', 'buildingLevels', 'lift', 'interiorHeight',
              'heating', 'airCondittioner', 'overhead', 'accessibility', 'bathroomAndToilet', 'orientation', 'view',
              'balconySize', 'gardenConnection', 'attic', 'parking', 'parkingSpacePrice' ]

header2 = ['floorspace', 'numberOfRooms', 'conditionOfTheRealEstate', 'yearOfConsttruction',
              'conveniences', 'energyPerformanceCertificate', 'floor', 'buildingLevels', 'lift', 'interiorHeight',
              'heating', 'airCondittioner', 'overhead', 'accessibility', 'bathroomAndToilet', 'orientation', 'view',
              'balconySize', 'gardenConnection', 'attic', 'parking', 'parkingSpacePrice','price' ]

# file_path = __file__[0:__file__.rindex("\\")+1]

# apartment_data_vertical = pd.read_csv(file_path + 'assets\\verticals.csv', on_bad_lines='skip', sep=";")
categories = pd.ExcelFile(os.path.abspath(os.path.join('..','apart_project/apart_app/assets','categories.xlsx')))

apartment_data_vertical = None
unique_ids = []

def get_numerical_value(sheet_name, value):
    temp_sheet = categories.parse(sheet_name)

    for i in range(len(temp_sheet)):
        if temp_sheet.iloc[i,0] == value:
            return temp_sheet.iloc[i,1]
    return 'nincs megadva'

def convert_nominal_data_to_numeric_data(apartment_data_vertical):
    for i in range(len(apartment_data_vertical)):
        if apartment_data_vertical.iloc[i,2] in categories.sheet_names:
            apartment_data_vertical.iloc[i,3] = get_numerical_value(apartment_data_vertical.iloc[i,2], apartment_data_vertical.iloc[i,3])
        else:
            if apartment_data_vertical.iloc[i,2] in {'overhead', 'balconySize'} and apartment_data_vertical.iloc[i,3] != "nincs megadva" :
                apartment_data_vertical.iloc[i,3] = apartment_data_vertical.iloc[i,3].split(' ')[0]

            if apartment_data_vertical.iloc[i,2] == header[-1]:
                if not apartment_data_vertical.iloc[i,3].split(' ')[0].isdigit():
                    apartment_data_vertical.iloc[i,3] = np.NaN

def convert_missing_data_to_NaN(apartment_data_vertical):
    for i in range(len(apartment_data_vertical)):
        if apartment_data_vertical.iloc[i,3] == "nincs megadva":
            apartment_data_vertical.iloc[i,3] = np.NaN

def convert_numeric_values_to_ordinal(apartment_data_ordinal):
    
    for i in range(len(unique_ids)):
        temp_data = apartment_data_vertical.query('id == @unique_ids[@i]')
        for j in range(len(header)):
            if j < temp_data.shape[0]:
                if header[j] == temp_data.iloc[j,2]:
                    apartment_data_ordinal.iloc[i,j] = temp_data.iloc[j,3]
                else:
                    apartment_data_ordinal.iloc[i,j] = np.NaN
            else:
                apartment_data_ordinal.iloc[i,j] = np.NaN

def reindex_dataframe(apartment_data_ordinal, header2):
    apartment_data_ordinal = apartment_data_ordinal.reindex(columns=header2)

def rank_apartment_data(apartment_data_ordinal):
    for i in range(apartment_data_ordinal.shape[1] - 1):
        apartment_data_ordinal.iloc[:,i] = rankdata(apartment_data_ordinal.iloc[:,i].astype(float), method='dense')

def start_conversion(input):
    apartment_data_vertical = input
    unique_ids = apartment_data_vertical.iloc[:,0].unique()
    print(len(unique_ids))
    print(apartment_data_vertical)
    convert_nominal_data_to_numeric_data(apartment_data_vertical)
    convert_missing_data_to_NaN(apartment_data_vertical)

    apartment_data_ordinal = pd.DataFrame(columns=header,index=range(len(unique_ids)))
    convert_numeric_values_to_ordinal(apartment_data_ordinal)
    apartment_data_ordinal = apartment_data_ordinal.reindex(columns=header2)
    rank_apartment_data(apartment_data_ordinal)

    return apartment_data_ordinal
