import pandas as pd
import matplotlib.pyplot as plt
import lasio

las = lasio.read("Petrobras\\15-9-19_SR_COMP.LAS")

df = las.df()
df.reset_index(inplace=True)
df.rename(columns={'DEPT':'DEPTH'}, inplace=True)
""" df.plot(subplots=True)
plt.show()
 """
print(max(df['GR']))
print()
fig=plt.subplots(figsize=(2.8,1.6*6),layout='tight')
ax1 = plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
ax1.plot("GR","DEPTH",data=df, color="green")
ax1.set_xlabel("Gamma")
ax1.set_xlim(min(df['GR']),max(df['GR']))
ax1.set_ylim(df['DEPTH'].iloc[-1],df['DEPTH'].iloc[0])
ax1.grid()
plt.show()
