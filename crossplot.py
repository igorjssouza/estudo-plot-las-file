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

        self.button = wx.Button(self.panel, label="Select LAS Files", pos=(10, 10))
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.las_label = wx.StaticText(self.panel, label="LAS File:", pos=(10, 40))
        self.las_combo = wx.ComboBox(self.panel, pos=(70, 40), style=wx.CB_READONLY)
        self.las_combo.Bind(wx.EVT_COMBOBOX, self.on_las_combo_select)


        self.y_label = wx.StaticText(self.panel, label="Y-axis:", pos=(10, 40+30))
        self.y_combo = wx.ComboBox(self.panel, pos=(70, 40+30), choices=self.log_choices, style=wx.CB_READONLY)

        self.x_label = wx.StaticText(self.panel, label="X-axis:", pos=(10, 70+30))
        self.x_combo = wx.ComboBox(self.panel, pos=(70, 70+30), choices=self.log_choices, style=wx.CB_READONLY)

        self.gr_label = wx.StaticText(self.panel, label="Color:", pos=(10, 110+30))
        self.gr_combo = wx.ComboBox(self.panel, pos=(70, 110+30), choices=self.log_choices, style=wx.CB_READONLY)

        self.ok_button = wx.Button(self.panel, label="OK", pos=(220, 180))
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok_button_click)

        self.cancel_button = wx.Button(self.panel, label="Cancel", pos=(300, 180))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button_click)

        self.canvas = None
        self.ax = None
        self.polygon_selector = None

        self.dataframes = []  # Store multiple DataFrames

    def on_las_combo_select(self, event):
        selected_las = self.las_combo.GetValue()
        if selected_las:
            self.update_log_choices(selected_las)

    def on_ok_button_click(self, event):
        if self.y_combo.GetValue() and self.x_combo.GetValue() and self.gr_combo.GetValue():
            self.create_scatter_plots()

    def on_cancel_button_click(self, event):
        self.Close()

    def on_button_click(self, event):
        dialog = wx.FileDialog(
            self,
            "Select LAS Files",
            wildcard="LAS files (*.las)|*.las",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        )
        if dialog.ShowModal() == wx.ID_OK:
            filenames = dialog.GetPaths()

            self.dataframes = {}  

            for filename in filenames:
                # Read LAS file
                las = lasio.read(filename)
                df = las.df()
                df.reset_index(inplace=True)

                # Store DataFrame
                self.dataframes[filename] = df
                self.las_combo.Append(filename)

            # self.las_combo.SetSelection(0)  # Select the first LAS file
            # Update log choices
            # self.update_log_choices()
            # self.update_log_choices(self.las_combo.GetValue())

        dialog.Destroy()

    def create_scatter_plots(self):
        fig, ax = plt.subplots()
        x=self.x_combo.GetValue()
        y=self.y_combo.GetValue()
        c=self.gr_combo.GetValue()
        scatter_plot = ax.scatter(x,y,data=self.df,c=c,vmin=0,vmax=100,
            cmap='rainbow'
        )

        ax.set_ylabel(f"{self.y_combo.GetValue()}", fontsize=14)
        ax.set_xlabel(f"{self.x_combo.GetValue()}", fontsize=14)

        # Add a label beside the color bar
        cbar = plt.colorbar(scatter_plot)
        cbar.ax.set_ylabel(self.gr_combo.GetValue(), rotation=270, labelpad=15, fontsize=12)

        # Clear the previous plot, if exists
        if self.canvas is not None:
            self.canvas.Destroy()

        # Create a wxPython panel and embed the new plot in it
        self.canvas = wxagg.FigureCanvasWxAgg(self.panel, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.panel.Layout()

        # Enable polygon selector
        self.ax = ax
        self.polygon_selector = PolygonSelector(ax, self.on_polygon_select)

        # Remove buttons and combo boxes
        self.y_label.Destroy()
        self.y_combo.Hide()
        self.x_label.Destroy()
        self.x_combo.Hide()
        self.gr_label.Destroy()
        self.gr_combo.Hide()
        self.ok_button.Destroy()
        self.cancel_button.Destroy()
        self.button.Destroy()

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
            self.ax.scatter(
                x=points_inside_polygon[:, 0],
                y=points_inside_polygon[:, 1],
                c=points_inside_polygon[:, 2],
                vmin=0,
                vmax=100,
                cmap='rainbow'
            )

            # Redraw the plot
            self.canvas.draw()

    def update_log_choices(self, selected_las):
        self.log_choices = []

        self.df = self.dataframes.get(selected_las)  # Get DataFrame for selected LAS file

        if self.df is not None:
            self.log_choices.extend(list(self.df.columns))

        self.y_combo.Clear()
        self.y_combo.AppendItems(self.log_choices)

        self.x_combo.Clear()
        self.x_combo.AppendItems(self.log_choices)

        self.gr_combo.Clear()
        self.gr_combo.AppendItems(self.log_choices)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
