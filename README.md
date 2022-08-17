#Index Creation - Vivek Vinod

**Repository for creating a sample Stock Index based on the Criteria provided in Problem_README.md**

**Results file with the high precision index values can be found in data_sources/results.csv**

Since the given companies have the same amount of shares outstanding, the market capitalization is proportional to the stock price. Therefore when selecting the top three stocks by market cap, we can just select top 3 stocks by their prices.

**Logic followed by the Code** - 

* Inorder to calculate the Index values for each day in the sample, we run an iteration across all the dates in the stock price data file between the start and end dates.
I initialize the Indexvalue on the starting day as 100 and then call a function to return the names of the top 3 stocks by their closing prices on the previous day. 

  Based on the results of this, we have the index rule that 50% allocation should be to the highest market cap stock while the 2nd and 3rd highest get 25% each. 
  Given this, we calculate the number of shares of each of these stocks that the index will allocate to. This is given by the formula - 

  For the Highest Market cap , number of shares in Index = 0.5*Index Value/Price of the stock (replace 0.5 with 0.25 for 2nd and 3rd highest and 0 for others)

* Next for any subsequent date in the sample, we check if it is the first business day of the month by checking if the month matches with the month of the previous trading day. If the months are the same, then it is not a first business day and we use the same allocation (in terms of number of shares) as the first business day of that month.

  Then we multiple this number of shares with the Price on that day to obtain the index value on that particular day.

* Whereas if the date is the first business day of the month, we first calculate the index value as the product of the Index weights on the previous month times the Prices for the shares. Then we run the function to find the top 3 stocks on the last business day of previous month and subsequently find the index allocations that will be used for calculating the index levels in subsequent dates on the month.


**Improvements**

I've prioritized using functions that can convey the logic easily.
There are more efficient methods to calculate the top 3 maximum stocks that the for loop especially once the number of stocks increases.

