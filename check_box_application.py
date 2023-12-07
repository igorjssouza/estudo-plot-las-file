import wx
from pubsub import pub

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.panel1 = wx.Panel(self, wx.ID_ANY)
        self.panel2 = wx.Panel(self, wx.ID_ANY)
        self.panel3 = wx.Panel(self, wx.ID_ANY)

        self.checkboxes = []
        for panel in [self.panel1, self.panel2, self.panel3]:
            checkboxes = []
            for i in range(3):
                checkbox = wx.CheckBox(panel, wx.ID_ANY, f"Checkbox {i+1}")
                checkboxes.append(checkbox)
                checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click)
            self.checkboxes.append(checkboxes)

        self.setup_layout()
        self.setup_pubsub()

    def setup_layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        panel_sizer1 = wx.BoxSizer(wx.VERTICAL)
        panel_sizer1.AddStretchSpacer(1)
        for checkbox in self.checkboxes[0]:
            panel_sizer1.Add(checkbox, 0, wx.ALL, 5)
        panel_sizer1.AddStretchSpacer(1)
        self.panel1.SetSizer(panel_sizer1)

        panel_sizer2 = wx.BoxSizer(wx.VERTICAL)
        panel_sizer2.AddStretchSpacer(1)
        for checkbox in self.checkboxes[1]:
            panel_sizer2.Add(checkbox, 0, wx.ALL, 5)
        panel_sizer2.AddStretchSpacer(1)
        self.panel2.SetSizer(panel_sizer2)

        panel_sizer3 = wx.BoxSizer(wx.VERTICAL)
        panel_sizer3.AddStretchSpacer(1)
        for checkbox in self.checkboxes[2]:
            panel_sizer3.Add(checkbox, 0, wx.ALL, 5)
        panel_sizer3.AddStretchSpacer(1)
        self.panel3.SetSizer(panel_sizer3)

        sizer.Add(self.panel1, 1, wx.EXPAND, 0)
        sizer.Add(self.panel2, 1, wx.EXPAND, 0)
        sizer.Add(self.panel3, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def setup_pubsub(self):
        pub.subscribe(self.update_checkboxes, "checkbox_state_changed")

    def on_checkbox_click(self, event):
        checkbox = event.GetEventObject()
        panel_index = -1
        checkbox_index = -1

        # Find the panel and checkbox indices
        for i, checkboxes in enumerate(self.checkboxes):
            if checkbox in checkboxes:
                panel_index = i
                checkbox_index = checkboxes.index(checkbox)
                break

        # Publish the checkbox state change to other panels
        pub.sendMessage("checkbox_state_changed",
                        panel_index=panel_index,
                        checkbox_index=checkbox_index,
                        checked=checkbox.IsChecked())

    def update_checkboxes(self, panel_index, checkbox_index, checked):
        # Update checkboxes in other panels
        for i, checkboxes in enumerate(self.checkboxes):
            if i != panel_index:
                checkboxes[checkbox_index].SetValue(checked)


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, wx.ID_ANY, "Checkbox Sync App")
    frame.Show()
    app.MainLoop()
