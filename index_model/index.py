import datetime as dt
import pandas as pd
import numpy as np

#Function to return the column names of the first 3 maximum values from the list  
def findmax(x1,stocknames):

    max1 = stocknames[0]
    max2 = stocknames[1]
    max3 = stocknames[2]

    for k in range(1,10):
       
        if x1[stocknames[k]]>x1[max1]:
            max3 = max2
            max2 = max1
            max1 = stocknames[k]
            
        elif x1[stocknames[k]]>x1[max2]:
            max3 = max2
            max2 = stocknames[k]
           
        elif x1[stocknames[k]]>x1[max3]:
            max3 = stocknames[k]
            
            
    return(max1,max2,max3)    



class IndexModel:
    def __init__(self):
                
        pass

    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:
        
        #Load the data with daily stock prices, to edit this path based on the location of the data file
        stock_prices = pd.read_csv(r"C:\Users\vivek\Assessment-Index-Modelling/data_sources/stock_prices.csv")
        stock_prices['Date'] = pd.to_datetime(stock_prices['Date'],format='%d/%m/%Y')
        
        #Column names of Stock A:J (10 stocks), can make this dynamic to automatically work for different sample size at a later stage
        stocknames = stock_prices.columns[1:11]
        
        #Creating a new dataframe to calculate the number of shares of a particular stock the index owns on rebalancing dates
        df_copy = pd.DataFrame().reindex_like(stock_prices)
        df_copy['Date'] = stock_prices['Date']
        df_copy['Indexvalue'] = float(0)
        df_copy.iloc[:,1:11] = 0
        
        for i,row in stock_prices.iterrows():
    
        #Initializing the Index on the start date to Index level 100 and choosing the allocations
            if stock_prices['Date'][i] == start_date:
                df_copy.loc[i,'Indexvalue'] = 100
                new = findmax(stock_prices.iloc[i-1],stocknames)  #returning the first 3 stocks by market cap
                for j in range(0,10):
                    df_copy.loc[i,new[0]] = df_copy.loc[i,"Indexvalue"]*0.5/stock_prices.loc[i,new[0]]
                    df_copy.loc[i,new[1]] = df_copy.loc[i,"Indexvalue"]*0.25/stock_prices.loc[i,new[1]]
                    df_copy.loc[i,new[2]] = df_copy.loc[i,"Indexvalue"]*0.25/stock_prices.loc[i,new[2]]
           
                indexcomp = df_copy.iloc[i,1:11]   
    
            elif stock_prices['Date'][i]>start_date and stock_prices['Date'][i] <= end_date:
        
                #For Index rebalancing dates - first business day of a month
                if stock_prices['Date'][i].month != stock_prices['Date'][i-1].month : 
                    df_copy.loc[i,'Indexvalue'] = np.dot(indexcomp,stock_prices.iloc[i,1:11]) 
               
                    new = findmax(stock_prices.iloc[i-1],stocknames)
                    for j in range(0,10):
                        df_copy.loc[i,new[0]] = df_copy.loc[i,"Indexvalue"]*0.5/stock_prices.loc[i,new[0]]
                        df_copy.loc[i,new[1]] = df_copy.loc[i,"Indexvalue"]*0.25/stock_prices.loc[i,new[1]]
                        df_copy.loc[i,new[2]] = df_copy.loc[i,"Indexvalue"]*0.25/stock_prices.loc[i,new[2]]
                
                    indexcomp = df_copy.iloc[i,1:11]      
            
                elif stock_prices['Date'][i].month == stock_prices['Date'][i-1].month :    
                   df_copy.loc[i,'Indexvalue'] = np.dot(indexcomp,stock_prices.iloc[i,1:11])                
                  
        self.index = df_copy[['Date','Indexvalue']]
        self.index = self.index[self.index['Date'].dt.date >= start_date]
        self.index = self.index[self.index['Date'].dt.date <= end_date]
        
        pass


    def export_values(self, file_name: str):
        #File path to save the csv file
        self.index.to_csv (r"C:\Users\vivek\Assessment-Index-Modelling/data_sources/results.csv", index = False, header=True)

        pass