import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import lasio

las = lasio.read("15-9-19_SR_COMP.LAS")

df = las.df()
df.reset_index(inplace=True)
df.rename(columns={'DEPT':'DEPTH'}, inplace=True)

fig=plt.subplots(figsize=(3.2,1.6*6),layout='tight')
ax1 = plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
ax1.plot("GR","DEPTH",data=df, color="green")
ax1.set_xlabel("Gamma")
ax1.set_xlim(min(df['GR']),max(df['GR']/2))
ax1.set_ylim(df['DEPTH'].iloc[-1],df['DEPTH'].iloc[0])
ax1.grid()

clicks = []
def on_click(event):
    if event.button is MouseButton.LEFT:
        print(f'xData {event.xdata:.2f} yData {event.ydata:.2f}')
        clicks.append((event.xdata, event.ydata))
        """,
              f'pixel coords {event.x} {event.y}')"""

binding_id = plt.connect('motion_notify_event', on_click)
plt.connect('button_press_event', on_click)


plt.show()
with open('clicks.txt', 'w') as f:
    for click in clicks:
        f.write(f'{click[0]:.2f}, {click[1]:.2f}\n')