import wx
import lasio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        
        self.panel = wx.Panel(self)
        
        # Load data from LAS file
        las = lasio.read("15-9-19_SR_COMP.LAS")
        df = las.df()
        df.reset_index(inplace=True)
        df.rename(columns={'DEPT':'DEPTH'}, inplace=True)
        
        # Create a matplotlib figure with the GR curve
        fig = plt.subplots(figsize=(3.2, 1.6*6), tight_layout=True)
        ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
        ax1.plot("GR", "DEPTH", data=df, color="green")
        ax1.set_xlabel("Gamma")
        ax1.set_xlim(min(df['GR']), max(df['GR']/2))
        ax1.set_ylim(df['DEPTH'].iloc[-1], df['DEPTH'].iloc[0])
        ax1.grid()
        
        # Create a canvas and add it to the panel
        self.canvas = FigureCanvas(self.panel, -1, fig[0])
        
        # Create a tree control to display clicked points
        self.tree = wx.TreeCtrl(self.panel)
        self.root = self.tree.AddRoot('Marcked points')
        
        # Create a sizer for the panel and add the canvas and tree
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.SetSizeHints(self.panel)
        
        # Bind the mouse click event to the canvas
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        self.Show()
        
    def on_click(self, event):
        x = event.xdata
        y = event.ydata
        if x is not None and y is not None:
            # Add the clicked point to the tree control
            point_str = '({:.2f}, {:.2f})'.format(x, y)
            self.tree.AppendItem(self.root, point_str)

            # Add a bullet marker on the plot
            ax = self.canvas.figure.axes[0]
            ax.plot(x, y, marker='o', markersize=4, color='red')

            self.canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    app.MainLoop()
