# -*- coding: utf-8 -*-
"""Vailantan_ ARMA_Stock_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17AZ6fUCi9g9ycWEaz_T3A97YQH79FAE8
"""

#from statsmodels.tsa.stattools import adfuller

#result = adfuller(data)
#print("1. ADF : ",result[0])
##print("2. P-Value : ", result[1])
#print("3. Num Of Lags : ", result[2])
#print("4. Num Of Observations Used For ADF Regression:", result[3])
#print("5. Critical Values :")
#for key, val in result[4].items():
  #print("\t",key, ": ", val)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
!pip install pmdarima
from pmdarima.arima.utils import ndiffs
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
import statsmodels.api as sm
import datetime

df = pd.read_csv("/content/^NSEI.csv")

def stock_prediction():
  df.Date= pd.to_datetime(df.Date)
  df2 =df.set_index('Date')
  data = list(df2["Close"])
  d_value = ndiffs(data,test = "adf")
  x_train= data[:-100]
  x_test = data[-100:]
  stepwise_fit = auto_arima(data,trace=True,suppress_warnings=True)
  model = sm.tsa.arima.ARIMA(data, order=(0,1,0))
  model = model.fit()
  start=len(x_train)
  end=len(x_train)+len(x_test)-1
  pred = model.predict(start=start,end=end)
  s = pd.Series(pred, index =df2.index[-100:])
  print()
  print("Accuracy")
  print("mean Squared Error",np.sqrt(mean_squared_error(x_test,pred)))
  print("R^2 value is ",r2_score(x_test,pred))
  plt.figure(figsize=(10,6), dpi=100)
  df2['Close'][-100:].plot(label='Actual Stock Price', legend=True)
  s.plot(label='Predicted Price', legend=True,)
  pred_future = model.predict(start=end,end=end+10)
  start_date = datetime.datetime(2023,3,3)
  dates = [start_date + datetime.timedelta(days=idx) for idx in range(11)]
  pred_future2 = pd.Series(pred_future, index = dates)
  print()
  print("Actual Prediction")
  print("On 04/03/23 Stock close at",pred_future2[2])

stock_prediction()