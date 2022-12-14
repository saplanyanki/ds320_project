# -*- coding: utf-8 -*-
"""Alex Project_Code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AChRYFMHL294FlyRFzcGPonrurecvTCm
"""

#Libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV 
from sklearn.linear_model import Lasso
import scipy
import plotly.express as px
import os

from google.colab import drive
drive.mount('/content/gdrive')

#Read in the Data
#Read in the Data
data = pd.read_csv("/content/gdrive/My Drive/DS320_Project/Data/winemag-data_first150k.csv")
data.head(5)

"""# Data Cleaning

Items to address

*   fillna
*   description
"""

data.isnull().sum()

data.info()

# Remove 'Unnamed: 0'
data.drop('Unnamed: 0', axis=1, inplace=True)

data.isnull().sum()

# Remove rows with missing 'country' and 'province'
data = data.dropna(subset=['country']) # This addresses both missing values

data.isnull().sum()

# Consider dropping 'designation', 'region_1', and 'region_2'
data.drop('designation', axis=1, inplace=True)
data.drop('region_1', axis=1, inplace=True)
data.drop('region_2', axis=1, inplace=True)

data.isnull().sum()

"""Choose One:



*   Overall Mean
*   Variety Mean


"""

# Replace with overall mean
data['price'].fillna(data['price'].mean(), inplace=True)

# Replace with variety mean
varMean = data.groupby(['variety']).mean()
data['price'].fillna(data.groupby(['variety']).mean(), inplace=False)

# Creates a dictionary of province-designation relationships

def analyze(a):
  d1 = a[['province','designation']]
  dic = {}
  for x in d1['province']:
    if x not in dic.keys():
      dic["{}".format(x)] = []
    else:
      None
  for idx, series in d1.iterrows():
    if series['designation'] != 'nan':
      dic[series['province']].append(series['designation'])
    elif series['designation'] == 'nan':
      dic[series['province']].append('Empty')
    else:
      None


  print(dic)
  print(len(dic.keys()))

analyze(data)

"""# Exploratory Data Analysis"""

avgVarietyPrice = data.groupby(['variety']).mean()
avgVarietyPrice

priceDist = data[data['price'] < 250]
priceDistFig = px.histogram(priceDist, 'price', title = 'Distribution of Wine Price', width = 400, height = 400, nbins = 30)
priceDistFig.show()

provinceCount =  data.groupby(['province'])
provinceCount = provinceCount['province'].count()
provinceCount = provinceCount.nlargest(10, 'first')
provinceCount = px.bar(provinceCount, x = 'province', title = 'Top 10 Wine Producing Provinces', width = 400, height = 400)
provinceCount.update_layout(yaxis_title = "province", xaxis_title = "count")
provinceCount.show()

countryCount =  data.groupby(['variety']).size().reset_index(name = "count").nlargest(10, 'count')
countryFig = px.pie(countryCount, 'variety', 'count', color = 'variety', title = 'Top 10 Wine Varieties', width = 800, height = 800)
countryFig.show()

pointsDistFig = px.histogram(data, 'points', title = 'Distribution of Wine Points', width = 800, height = 800, nbins = 30)
pointsDistFig.show()

countryPrice =  data.groupby(['country'])
countryPrice = countryPrice['price'].mean()
countryPrice = countryPrice.nlargest(10, 'first')
countryPrice = countryPrice.plot(kind='bar', ylabel = 'Price', xlabel = 'Country', title = 'Top 10 Wine Producing Countries by Price')
countryPrice

wineryPrice =  data.groupby(['winery'])
wineryPrice = wineryPrice['price'].mean()
wineryPrice = wineryPrice.nlargest(10, 'first')
wineryPrice = wineryPrice.plot(kind='bar', ylabel = 'Price', xlabel = 'Winery', title = 'Top 10 Most Common Wineries by Price')
wineryPrice

provincePrice =  data.groupby(['province'])
provincePrice = provincePrice['price'].mean()
provincePrice = provincePrice.nlargest(10, 'first')
provincePrice = provincePrice.plot(kind='bar', ylabel = 'Price', xlabel = 'Province', title = 'Top 10 Wine Producing Provinces by Price')
provincePrice

commonWineries =  data.groupby(['winery'])
commonWineries = commonWineries['winery'].count()
commonWineries = commonWineries.nlargest(10, 'first')
commonWineries = commonWineries.plot(kind='bar', ylabel = 'Count', xlabel = 'Winery', title = 'Top 10 Most Common Wineries')
commonWineries

varietyPrice =  data.groupby(['variety'])
varietyPrice = varietyPrice['price'].mean()
varietyPrice = varietyPrice.nlargest(10, 'first')
varietyPrice = varietyPrice.plot(kind='bar', ylabel = 'Price', xlabel = 'Variety', title = 'Top 10 Most Common Wine Varieties by Price')
varietyPrice

commonVarieties =  data.groupby(['variety'])
commonVarieties = commonVarieties['variety'].count()
commonVarieties = commonVarieties.nlargest(10, 'first')
commonVarieties = commonVarieties.plot(kind='bar', ylabel = 'Count', xlabel = 'Variety', title = 'Top 10 Most Common Varieties')
commonVarieties
