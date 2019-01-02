
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd

from collections import Counter


# In[2]:

products = pd.read_csv('products.csv')
tenders = pd.read_csv('tenderModes.csv')


# In[3]:

sample = pd.read_csv('sampleSubmission.csv')


# In[4]:

products['product_code'].fillna(12345, inplace=True)


# In[5]:

products['count'] = range(products.shape[0])
products['identity'] = 1


# In[7]:

products['transactionDate'] = pd.to_datetime(products['transactionDate'])
products['year'] = products['transactionDate'].dt.year
products['month'] = products['transactionDate'].dt.month
products['day'] = products['transactionDate'].dt.day


# In[8]:

products['one'] = 1


# In[71]:

customers = sample['customerID']

products_2017 = products.loc[products['year'] == 2017]
customers_2017 = products_2017['customerID'].unique()
num_mon_purchases_2017 = []
mean_purchases_per_mon_2017 = []

i = 0
for customer in customers:
    #if i%100 == 0:
        #print i, customer
    i += 1
    if customer not in customers_2017:
        num_mon_purchases_2017.append(0)
        mean_purchases_per_mon_2017.append(0)
        continue
    
    total_purchases_2017 = products_2017['one'].loc[products_2017['customerID'] == customer].count()
    mon_purchases = products_2017['month'].loc[products_2017['customerID'] == customer].unique().size
    
    num_mon_purchases_2017.append(mon_purchases)
    mean_purchases_per_mon_2017.append((total_purchases_2017*1.0)/mon_purchases)
    
    #print total_purchases_2017, mon_purchases


# In[195]:

customers = sample['customerID']
most_brought_products_dict_all = {}

count = 0
for customer in customers:
    #print customer
    cust_products = products['product_code'].loc[products['customerID'] == customer]
    most_brought_products = Counter(cust_products).most_common()
    most_brought_products = [int(x[0]) for x in most_brought_products]
    most_brought_products_dict_all[str(customer)] = most_brought_products
    if count % 100 == 0:
        print count, customer#, most_brought_products_dict
    count += 1


# In[ ]:

customers = sample['customerID']
i = 0
cust_no_shop_2016_2017 = []
for customer in customers:
    years = list(products['year'].loc[products['customerID'] == customer].unique())
    #print years
    if 2017 not in years and 2016 not in years:
        print i, customer
        cust_no_shop_2016_2017.append(customer)
    i += 1


# In[426]:

popular_products = products['product_code'].value_counts().index.tolist()[:15]
customers = sample['customerID']
result = []

most_brought_products_count = 4
popular_products_count = 4
i = 0

for customer in customers:
    recs = ''
            
    most_brought_products_count = 4
    popular_products_count = 0
    #print customer
    if customer in cust_no_shop_2016_2017:
        #print customer
        most_brought_products_count = 0
        popular_products_count = 0
    elif num_mon_purchases_2017[i] == 0:
        most_brought_products_count = 0
        popular_products_count = 3
    elif num_mon_purchases_2017[i] >=5 and mean_purchases_per_mon_2017[i] >= 35:
        most_brought_products_count = 15
        popular_products_count = 0
    elif num_mon_purchases_2017[i] >=5 and mean_purchases_per_mon_2017[i] >= 25:
        most_brought_products_count = 10
        popular_products_count = 0
    elif num_mon_purchases_2017[i] >=4 and mean_purchases_per_mon_2017[i] >= 10:
        1 == 1
        most_brought_products_count = 8
        popular_products_count = 0
        
    count = 0
    
    most_brought_products = []
    most_brought_products += most_brought_products_dict_all[str(customer)][:most_brought_products_count]
    
    for most_brought_product in most_brought_products:
        recs += (str(most_brought_product) + ',')
        count += 1
    
    popular_count = 0
    for popular_product in popular_products:
        if popular_product not in most_brought_products and popular_count < popular_products_count: 
            recs += (str(int(popular_product)) + ',')
            count += 1
            popular_count += 1
        
    for _ in range(20, count, -1):
        recs += 'None,'
        
    result.append(recs[:-1])
    i += 1
    #print recs[:-1]


# In[428]:

submit = pd.DataFrame()
submit['customerID'] = sample['customerID']
submit['products'] = result


# In[429]:

submit.to_csv('submit.csv', index=False)

