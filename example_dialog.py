import wx

class ComboBoxDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Combo Box Dialog")

        # Create a static box sizer for each combo box
        static_box_sizer1 = wx.StaticBoxSizer(wx.VERTICAL, self, "Combo Box 1")
        static_box_sizer2 = wx.StaticBoxSizer(wx.VERTICAL, self, "Combo Box 2")
        static_box_sizer3 = wx.StaticBoxSizer(wx.VERTICAL, self, "Combo Box 3")

        # Create combo boxes for each section
        combo_box1 = wx.ComboBox(self, choices=["Option 1", "Option 2", "Option 3"])
        combo_box2 = wx.ComboBox(self, choices=["Option A", "Option B", "Option C"])
        combo_box3 = wx.ComboBox(self, choices=["Choice X", "Choice Y", "Choice Z"])

        # Add combo boxes to the respective static box sizers
        static_box_sizer1.Add(combo_box1, 0, wx.ALL, 5)
        static_box_sizer2.Add(combo_box2, 0, wx.ALL, 5)
        static_box_sizer3.Add(combo_box3, 0, wx.ALL, 5)

        # Create a sizer for the dialog
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add static box sizers to the main sizer
        sizer.Add(static_box_sizer1, 0, wx.ALL, 5)
        sizer.Add(static_box_sizer2, 0, wx.ALL, 5)
        sizer.Add(static_box_sizer3, 0, wx.ALL, 5)

        # Set the main sizer for the dialog
        self.SetSizer(sizer)
        sizer.Fit(self)

        # Show the dialog
        self.ShowModal()
        self.Destroy()

# Create the application
app = wx.App()

# Create the dialog
dialog = ComboBoxDialog(None)

# Run the application
app.MainLoop()
