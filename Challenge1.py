# ---------------------------------------------------------------------------
# Author: Doruk Aksoy
# Date: 04/03/2020
# Data Incubator Application Challenge 1
# ---------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Divide description into color designations
def removeEmptyElements(arr,col):
    arr['Color0']="";arr['Color1']="";arr['Color2']="";arr['Color3']=""
    for el in range(np.size(arr,axis=0)):
        elements = list(filter(None,arr[col][el]))
        for i in range(np.size(elements)):
            arr['Color%i' %i][el] = elements[i]
    return arr

def findCategories(arr,col,torso,legs,accesories):
    arr['Type']=""
    for el in range(np.size(arr,axis=0)):
        name_list = arr[col][el].split(" ")
        for i in range(np.size(name_list)):
            if name_list[i] in torso:
                arr['Type'][el] = "Torso"
            elif name_list[i] in legs:
                arr['Type'][el] = "Legs"
            elif name_list[i] in accesories:
                arr['Type'][el] = "Accesories"  
            else:
                arr['Type'][el] = "NA"  
    return arr
            
# Read in data from given files
clothes_casual = pd.read_csv("hm_da_casual.csv")
clothes_formal = pd.read_csv("hm_da_formal.csv")
clothes_sport = pd.read_csv("hm_da_sport.csv")

# Get rid of tabs and split the colors
clothes_casual['description'] = clothes_casual['description'].str.replace("\t","").str.split("\n")
clothes_formal['description'] = clothes_formal['description'].str.replace("\t","").str.split("\n")
clothes_sport['description'] = clothes_sport['description'].str.replace("\t","").str.split("\n")

# Remove empty elements
clothes_casual = removeEmptyElements(clothes_casual,'description')
clothes_formal = removeEmptyElements(clothes_formal,'description')
clothes_sport = removeEmptyElements(clothes_sport,'description')    

# Delete unnecessary columns
clothes_casual.drop(columns=['web-scraper-order', 'web-scraper-start-url','description'],inplace=True)
clothes_formal.drop(columns=['web-scraper-order', 'web-scraper-start-url','description'],inplace=True)
clothes_sport.drop(columns=['web-scraper-order', 'web-scraper-start-url','description'],inplace=True)

# Correct format for price data
clothes_casual['price'] = clothes_casual['price'].str.strip("$").astype(float)
clothes_formal['price'] = clothes_formal['price'].str.strip("$").astype(float)
clothes_sport['price'] = clothes_sport['price'].str.strip("$").astype(float)

# Plot histograms to show the correlation between Number of clothing type owned vs. Price
fig1, ax1 = plt.subplots()
ax1.set_title('Type of clothing vs. Price',fontsize=18)
ax1.set_ylabel('Number of owned clothing',fontsize = 15)
ax1.set_xlabel('Price ($)',fontsize = 15)
line1 = plt.hist(np.asarray(clothes_casual['price']), label='Casual')
line2 = plt.hist(np.asarray(clothes_formal['price']), label='Formal')
line3 = plt.hist(np.asarray(clothes_sport['price']), label='Sport')
ax1.legend()
plt.show()

# Categorize
torso = ["Top","T-shirt","Shirt","Sweatshirt","Hoodie","Cardigan","Jacket","Coat","Parka","Blazer","Vest"]
legs =["Shorts","Joggers","Pants","Chinos","Tights"]
accesories = ["Hat","Cap"]

# Find categories
clothes_casual = findCategories(clothes_casual,'name',torso,legs,accesories)
clothes_formal = findCategories(clothes_formal,'name',torso,legs,accesories)
clothes_sport = findCategories(clothes_sport,'name',torso,legs,accesories)

# Find mean prices for each type
ave_price_casual = clothes_casual.groupby("Type")['price'].mean()
ave_price_formal = clothes_formal.groupby("Type")['price'].mean()
ave_price_sport = clothes_sport.groupby("Type")['price'].mean()