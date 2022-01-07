'''
This script was written using google colab where it has been proven to run and operate well, integrating with google's forms feature. 
'''

import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
#@title Calibrator Elution Volumes
#@markdown Enter elution volumes for calibrators used - "None" if not used.

# TODO: Make this go straight into numpy
Void = 7.72 #@param {type:"number"}
Column_Volume = 23.562 #@param {type: "number"}

thyroglobulin =  None #@param{type:"raw"}
ferritin = 10.56  #@param{type:"raw"}
aldolase = 12.82  #@param{type:"raw"}
conalbumin = 14.1 #@param{type:"raw"}
ovalbumin =  15.01 #@param{type:"raw"}
carbonic_anh =  16.24 #@param{type:"raw"}
ribonuclease =  17.5 7#@param{type:"raw"}
aprotinin =  19.12 #@param{type:"raw"}

Retentions = {"Thyroglobulin":	[660, thyroglobulin], "Ferritin":	[440, ferritin],
              "Aldolase":	[158, aldolase], "Conalbumin":	[75,	conalbumin], 
              "Ovalbumin":	[44,	ovalbumin], "Carbonic Anhydrase":	[29,	carbonic_anh],
              "Ribonuclease":	[13.7,	ribonuclease], "Aprotinin": [6.5, aprotinin]}


# Building a dataframe
# TODO: just go straight to numpy - get rid of pandas.
df = pd.DataFrame.from_dict(Retentions,orient="index", columns=["MW", "Recorded Volume"])
df["Elution Volume"] = df["Recorded Volume"]-Void
df["logMW"] = np.log(df["MW"])
df.dropna(inplace=True)
arr = df[["logMW", "Elution Volume"]].to_numpy()
x_test = arr[0::,0].reshape(-1,1)
y_test = arr[0::,1].reshape(-1,1)

#Calculate Linreg
reg = LinearRegression().fit(X = x_test, y = y_test)
y_pred = reg.predict(x_test)

#Build plot
fig, ax = plt.subplots()
ax.plot(df[["Elution Volume"]], df[["logMW"]], "o")
ax.plot(reg.predict(arr[0::,0].reshape(-1,1)), arr[0::,0].reshape(-1,1), "-")
title = f'Retention Volume = {round(reg.coef_[0][0],5)}*Log(MW)+{round(reg.intercept_[0],5)} with R^2 of {round(r2_score(y_test, y_pred),5)}'
ax.set_xticks(range(0,13))
ax.set_yticks(range(0,6))
ax.grid(axis='both')
ax.set_title(title)
ax.set_xlabel("Elution Volume - Void Volume")
ax.set_ylabel("Log(kDa)")
