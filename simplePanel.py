import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent = None, size = (640, 480))

        self.list1 = wx.ListBox(self, style = wx.LB_HSCROLL)
        self.list2 = wx.ListBox(self, style = wx.LB_HSCROLL)

        self.list1.Append('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.list2.Append('bbbbbbbbbbb')

        self.fgs = wx.FlexGridSizer(1, 2)
        self.fgs.AddMany([(self.list1, 1, wx.EXPAND), (self.list2, 1, wx.EXPAND)])
        self.fgs.AddGrowableRow(0, 1)
        self.fgs.AddGrowableCol(0, 1)
        self.fgs.AddGrowableCol(1, 1)

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Sizer = fgs
        self.Layout()
        self.Show()

    def Exit(self, event):
        self.Close(True)

app = wx.App(False)
frame = MyFrame()
app.MainLoop()