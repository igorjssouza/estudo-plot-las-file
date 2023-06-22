# import wx
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.backends.backend_wxagg as wxagg
# import lasio
# from matplotlib.path import Path
# # from matplotlib.widgets import PolygonSelector

# class MyFrame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, title="LAS File Scatter Plot")

#         self.panel = wx.Panel(self)

#         self.log_choices = []  # Available log choices

#         self.button = wx.Button(self.panel, label="Select LAS Files", pos=(10, 10))
#         self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

#         self.las_label = wx.StaticText(self.panel, label="LAS Files:", pos=(10, 35))
#         self.las_combo = wx.ComboBox(self.panel, pos=(70, 35), style=wx.CB_READONLY)

#         self.y_label = wx.StaticText(self.panel, label="Y-axis:", pos=(10, 60))
#         self.y_combo = wx.ComboBox(self.panel, pos=(70, 60), style=wx.CB_READONLY)

#         self.x_label = wx.StaticText(self.panel, label="X-axis:", pos=(10, 90))
#         self.x_combo = wx.ComboBox(self.panel, pos=(70, 90), style=wx.CB_READONLY)

#         self.gr_label = wx.StaticText(self.panel, label="Color:", pos=(10, 130))
#         self.gr_combo = wx.ComboBox(self.panel, pos=(70, 130), style=wx.CB_READONLY)


#         self.dfs = []  # Store DataFrames



#     def on_cancel_button_click(self, event):
#         self.Close()

#     def on_button_click(self, event):
#         dialog = wx.FileDialog(self, "Select LAS Files", wildcard="LAS files (*.las)|*.las",
#                             style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
#         if dialog.ShowModal() == wx.ID_OK:
#             filenames = dialog.GetPaths()

#             self.las_combo.Clear()
#             self.dfs = []

#             for filename in filenames:
#                 # Read LAS file
#                 las = lasio.read(filename)
#                 df = las.df()
#                 df.reset_index(inplace=True)
#                 self.dfs.append(df)

#                 # Update LAS file combo box
#                 self.las_combo.Append(filename)

#             # Update log choices for the selected LAS file
#             selected_index = self.las_combo.GetSelection()
#             selected_df = self.dfs[selected_index]

#             self.log_choices = list(selected_df.columns)

#             # Update combo boxes
#             self.y_combo.Clear()
#             self.y_combo.AppendItems(self.log_choices)

#             self.x_combo.Clear()
#             self.x_combo.AppendItems(self.log_choices)

#             self.gr_combo.Clear()
#             self.gr_combo.AppendItems(self.log_choices)

#         dialog.Destroy()


# if __name__ == '__main__':
#     app = wx.App()
#     frame = MyFrame(None)
#     frame.Show()
#     app.MainLoop()
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))
        
        # Create the panel
        panel = wx.Panel(self)
        
        # Create the combo boxes
        self.name_combo = wx.ComboBox(panel, choices=['Data 1', 'Data 2', 'Data 3'], style=wx.CB_READONLY)
        self.log_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        
        # Bind an event handler for the name combo box
        self.name_combo.Bind(wx.EVT_COMBOBOX, self.on_name_selected)
        
        # Create a vertical sizer to hold the combo boxes
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label='Name Data:'), flag=wx.ALL, border=5)
        sizer.Add(self.name_combo, flag=wx.EXPAND|wx.ALL, border=5)
        sizer.Add(wx.StaticText(panel, label='Logs Available:'), flag=wx.ALL, border=5)
        sizer.Add(self.log_combo, flag=wx.EXPAND|wx.ALL, border=5)
        
        panel.SetSizer(sizer)
        
    def on_name_selected(self, event):
        selected_name = self.name_combo.GetValue()
        
        # Update the logs available based on the selected name
        if selected_name == 'Data 1':
            logs = ['Log 1', 'Log 2', 'Log 3']
        elif selected_name == 'Data 2':
            logs = ['Log A', 'Log B', 'Log C']
        elif selected_name == 'Data 3':
            logs = ['Log X', 'Log Y', 'Log Z']
        else:
            logs = []
        
        self.log_combo.Clear()
        self.log_combo.AppendItems(logs)


app = wx.App()
frame = MyFrame(None, title='ComboBox Example')
frame.Show()
app.MainLoop()

