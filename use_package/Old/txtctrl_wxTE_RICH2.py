import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wxTE_RICH2 TextCtrl", size=(400, 300))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 啟用 wxTE_RICH2 讓 TextCtrl 支援 RTF 文字處理
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_RICH2)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.display_text()

    def display_text(self):
        self.text_ctrl.SetDefaultStyle(wx.TextAttr(wx.BLACK))
        self.text_ctrl.AppendText("這是黑色文字。\n")

        self.text_ctrl.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.text_ctrl.AppendText("這是紅色文字。\n")

        self.text_ctrl.SetDefaultStyle(wx.TextAttr(wx.BLUE))
        self.text_ctrl.AppendText("這是藍色文字。\n")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
