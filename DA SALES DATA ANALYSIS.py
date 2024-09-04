#!/usr/bin/env python
# coding: utf-8

# ### ECOM SALES DATA ANALYSIS

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

import os


# In[2]:


os.chdir('C:\\DA Project Details')


# In[3]:


Orders = pd.read_excel("ECOMM DATA.xlsx" , sheet_name="Orders")
Returns = pd.read_excel("ECOMM DATA.xlsx" , sheet_name="Returns")
People = pd.read_excel("ECOMM DATA.xlsx" , sheet_name="People")


# ### EDA (Exploratory Data Analysis)

# In[4]:


## Checking for data types 
print("Info of Orders Dataframe" , "\n")
Orders.info()
print("\n"*2)

print("Info of Orders Dataframe","\n")
Returns.info()
print("\n"*2)

print("Info of Orders Dataframe","\n")
People.info()


# In[5]:


Orders.columns = Orders.columns.str.replace(" ","_" )
Returns.columns = Returns.columns.str.replace(" ","_" )


# In[6]:


#droping the market column as it is already present in Orders table 
Returns.drop(columns="Market" , inplace=True)


# In[7]:


## Fixing the data types of date columns in orders dataframe

Orders['Order_Date'] = pd.to_datetime(Orders['Order_Date'] , format="%Y-%m-%d")
Orders['Ship_Date']  = pd.to_datetime(Orders['Ship_Date'] , format="%Y-%m-%d")


# In[8]:


## Creating new columns for Year , month , Day
Orders["Year"] =Orders['Ship_Date'].dt.strftime("%Y")
Orders["Month_No"] =Orders['Ship_Date'].dt.month
Orders["Month"] =Orders['Ship_Date'].dt.strftime("%B")
Orders["Weekday"] =Orders['Ship_Date'].dt.strftime("%A")


# In[9]:


#Merging all the three datasets 

Sales_df = pd.merge(Orders , Returns , on="Order_ID" , how = "left").merge(People , on="Region",how="left")


# In[10]:


Sales_df.info()


# In[11]:


## fixing the Return columns like not returned "No" & returned "Yes"
Sales_df["Returned"] = Sales_df.Returned.fillna("No")


# In[13]:


## 5 point Summary of continious data 
Sales_df.select_dtypes("number").drop(columns={"Row_ID" , "Postal_Code" , "Month_No"}).describe().T


# In[15]:


## fixing the negative values in profit columns by putting "0"
Sales_df['Profit'] = np.where(Sales_df['Profit']<=0 , 0 , Sales_df['Profit'])


##Now summary 
Sales_df.select_dtypes("number").drop(columns={"Row_ID" , "Postal_Code" , "Month_No"}).describe().T


# In[16]:


Sales_df.info()


# # 1. total sales..

# In[17]:


Sales_df["Sales"].sum() , "Total Sales"


# ### i.Analysing  profit , sales , quantity , discount , Total return  by each category

# In[18]:


Sales_df.groupby("Category")["Sales"].agg("sum").round(2).sort_values(ascending = False)


# In[19]:


print(plt.style.available)


# In[21]:


#Analysis by category
plt.subplots_adjust(wspace=0.5,
    hspace=1)
plt.figure(figsize=(20,12))

#Category by Sales
plt.subplot(2,2,1)
Sales_df.groupby("Category")["Sales"].agg("sum").round(2).sort_values(
    ascending = False).plot(kind="bar")
plt.title("Total Sales by Category")
plt.xticks(rotation=0)

#Category by Profit
plt.subplot(2,2,2)
Sales_df.groupby("Category")["Profit"].agg("sum").round(2).sort_values(
    ascending = False).plot(kind="bar")
plt.title("Total Profit by Category")
plt.xticks(rotation=0)

#Category by Discount
plt.subplot(2,2,3)
Sales_df.groupby("Category")["Discount"].agg("sum").round(2).sort_values(
    ascending = False).plot(kind="bar")
plt.title("Total Discount by Category")
plt.xticks(rotation=0)

#Category by Quantity
plt.subplot(2,2,4)
Sales_df.groupby("Category")["Quantity"].agg("sum").round(2).sort_values(
    ascending = False).plot(kind="bar")
plt.title("Total Quantity by Category")
plt.xticks(rotation=0)

plt.style.use("bmh")
plt.show()


# In[22]:


# analysing catagory by number of returns
Sales_df[["Category" , "Returned"]].pivot_table(columns="Category" , index = "Returned" ,  
               aggfunc="size")


# In[23]:


Sales_df[["Category" , "Returned"]].pivot_table(columns="Category" , index = "Returned" ,  
               aggfunc="size").plot(kind = "bar" , figsize =(5,3))
plt.title("Productds Returned analysis by category")
plt.legend(loc='upper right' , bbox_to_anchor=(1.6,0.8) ,facecolor = 'grey')
plt.show()


# In[24]:


print(plt.style.available)


# # 2. analyze sales trends over time,

# In[25]:


Sales_df['Month-Year'] = Sales_df['Order_Date'].dt.strftime("%b-%Y")


# In[26]:


Sales_df.groupby(['Month-Year'])['Sales'].sum().sort_values().plot(figsize = (20,5) , marker='.')


# In[33]:


plt.subplots_adjust(wspace=0.3 , hspace=0.8)
plt.figure(figsize = (20,10))

plt.subplot(2,2,1)
Sales_df.groupby(['Year' ])['Sales'].sum().sort_values().plot()
plt.xticks(rotation = 90)
plt.title("Sales by Year")

plt.subplot(2,2,2)
Sales_df.groupby(['Month_No' ])['Sales'].sum().plot()
plt.xticks(rotation = 90)
plt.title('Sales analysis by Month')


plt.subplot(2,2,3)
Sales_df.groupby(['Month'])['Sales'].sum().sort_values().plot(marker = 'o')
plt.xticks(rotation = 90)
plt.title('Sales analysis by Month')


plt.subplot(2,2,4)
Sales_df.groupby(['Weekday' ])['Sales'].sum().sort_values().plot()
plt.xticks(rotation = 90)
plt.title('Sales analysis by Day of week')

plt.show()


# In[38]:


df.info()


# In[51]:


# taking some data from 2013-1014 for forcasting 
df = Sales_df.loc[Sales_df['Year']>='2013']


# In[54]:


df['Year-Month'] = df['Order_Date'].dt.strftime('%Y-%b')


# In[52]:


from statsmodels.graphics.tsaplots import plot_acf , plot_pacf


# In[61]:


Tsa = df.groupby('Year-Month')['Sales'].sum().reset_index()
Tsa.set_index('Year-Month' , inplace = True)


# In[63]:


plot_acf(Tsa)
plt.xlabel("LAGS")
plt.ylabel("AUTOCORRELATION")
plt.show()


# In[ ]:


Xaxis = Represents the lag or time shift.
Y-axis = Measures how strongly the time series at one lag is related to itself.


# In[50]:


from statsmodels.tsa.arima.model import ARIMA

# Aggregate sales data by date
sales_time_series = df.groupby('Year-Month')['Sales'].sum()

# Ensure the index is properly set and sorted by date
sales_time_series = sales_time_series.sort_index()

# Fit an ARIMA model
model = ARIMA(sales_time_series, order=(5, 1, 0))  # (p, d, q) order of ARIMA
model_fit = model.fit()

# Forecasting
forecast = model_fit.forecast(steps=10)  # Forecasting for the next 10 periods
print(forecast)

# Plotting the results
plt.figure(figsize=(20, 3))
plt.plot(sales_time_series, label='Historical Sales')
plt.plot(forecast, label='Forecast', color='red')
plt.title('Sales Forecast')
plt.xticks(rotation = 90)
plt.xlabel('Time zone')
plt.ylabel('Sales')
plt.legend(bbox_to_anchor = (1,1) , facecolor = 'skyblue')
plt.show()


# In[ ]:





# In[ ]:




