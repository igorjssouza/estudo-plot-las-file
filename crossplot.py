import wx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_wxagg as wxagg
import lasio
from matplotlib.path import Path
from matplotlib.widgets import PolygonSelector

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="LAS File Scatter Plot")

        self.panel = wx.Panel(self)

        self.log_choices = []  # Available log choices

        self.button = wx.Button(self.panel, label="Select LAS File", pos=(10, 10))
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.y_label = wx.StaticText(self.panel, label="Y-axis:", pos=(10, 40))
        self.y_combo = wx.ComboBox(self.panel, pos=(70, 40), choices=self.log_choices, style=wx.CB_READONLY)

        self.x_label = wx.StaticText(self.panel, label="X-axis:", pos=(10, 70))
        self.x_combo = wx.ComboBox(self.panel, pos=(70, 70), choices=self.log_choices, style=wx.CB_READONLY)

        self.gr_label = wx.StaticText(self.panel, label="Color:", pos=(10, 110))
        self.gr_combo = wx.ComboBox(self.panel, pos=(70, 110), choices=self.log_choices, style=wx.CB_READONLY)

        # self.button = wx.Button(self.panel, label="Select LAS File", pos=(10, 110))
        # self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.ok_button = wx.Button(self.panel, label="OK", pos=(220, 180))
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok_button_click)

        self.cancel_button = wx.Button(self.panel, label="Cancel", pos=(300, 180))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button_click)


        self.canvas = None
        self.ax = None
        self.polygon_selector = None

        self.df = None  # Store DataFrame

    def on_ok_button_click(self, event):
        if self.y_combo.GetValue() and self.x_combo.GetValue() and self.gr_combo.GetValue():
            self.create_scatter_plot()

    def on_cancel_button_click(self, event):
        self.Close()

    def on_button_click(self, event):
        dialog = wx.FileDialog(self, "Select LAS File", wildcard="LAS files (*.las)|*.las",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()

            # Read LAS file
            las = lasio.read(filename)
            df = las.df()
            df.reset_index(inplace=True)
            # df.rename(columns={'DEPT': 'DEPTH'}, inplace=True)

            self.df = df  # Store DataFrame

            # Update log choices
            self.log_choices = list(df.columns)

            # Update combo boxes
            self.y_combo.Clear()
            self.y_combo.AppendItems(self.log_choices)

            self.x_combo.Clear()
            self.x_combo.AppendItems(self.log_choices)

            self.gr_combo.Clear()
            self.gr_combo.AppendItems(self.log_choices)
        
        dialog.Destroy()

            # Create scatter plot
            # fig, ax = plt.subplots()
            # ax.scatter(x='NEU', y='DEN', data=df, c=df['GR'], vmin=0, vmax=100, cmap='rainbow')
            # ax.set_ylabel('Bulk Density (DEN) - g/cc', fontsize=14)
            # ax.set_xlabel('Neutron Porosity (NEU) - %', fontsize=14)
    def create_scatter_plot(self):
        
        fig, ax = plt.subplots()
        scatter_plot=ax.scatter(x=self.x_combo.GetValue(), y=self.y_combo.GetValue(), data = self.df,
                   c=self.df[self.gr_combo.GetValue()], vmin = 0, vmax=100, cmap='rainbow')
        
        ax.set_ylabel(f"{self.y_combo.GetValue()}", fontsize=14)
        ax.set_xlabel(f"{self.x_combo.GetValue()}", fontsize=14)

        # Add a label beside the color bar
        cbar = plt.colorbar(scatter_plot)
        cbar.ax.set_ylabel(self.gr_combo.GetValue(), rotation=270, labelpad=15, fontsize=12)
        
        # Clear the previous plot, if exists
        if self.canvas is not None:
            self.canvas.Destroy()

        # Remove buttons and combo boxes


        # Create a wxPython panel and embed the new plot in it
        self.canvas = wxagg.FigureCanvasWxAgg(self.panel, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.panel.Layout()

        # Add a colorbar
        # colorbar = fig.colorbar(ax.collections[0])

        # Fit the plot within the panel
        sizer.Fit(self)
        self.Layout()

        # Enable polygon selector
        self.ax = ax
        self.polygon_selector = PolygonSelector(ax, self.on_polygon_select)

        # dialog.Destroy()
        self.y_label.Destroy()
        self.y_combo.Hide()
        self.x_label.Destroy()
        self.x_combo.Hide()
        self.gr_label.Destroy()
        self.gr_combo.Hide()
        self.ok_button.Destroy()
        self.cancel_button.Destroy()

    def on_polygon_select(self, vertices):
        # Convert polygon vertices to a path
        path = Path(vertices)

  
        x = self.df[self.x_combo.GetValue()]
        y = self.df[self.y_combo.GetValue()]
        gr = self.df[self.gr_combo.GetValue()]

        points_inside_polygon = np.array(list(filter(path.contains_point, zip(x, y, gr))))

        if len(points_inside_polygon) > 0:
            # Clear previous scatter plot
            for collection in self.ax.collections:
                collection.remove()

            # Create new scatter plot with points inside the polygon
            self.ax.scatter(x=points_inside_polygon[:, 0], y=points_inside_polygon[:, 1],
                            c=points_inside_polygon[:, 2], vmin=0, vmax=100, cmap='rainbow')

            # Redraw the plot
            self.canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
