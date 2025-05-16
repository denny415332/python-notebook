import wx
import wx.richtext as rt


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="RichTextCtrl 多色文字", size=(400, 300))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.rich_text = rt.RichTextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.rich_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.display_text()

    def display_text(self):
        self.rich_text.BeginTextColour(wx.BLACK)
        self.rich_text.WriteText("這是黑色文字。\n")
        self.rich_text.EndTextColour()

        self.rich_text.BeginTextColour(wx.RED)
        self.rich_text.WriteText("這是紅色文字。\n")
        self.rich_text.EndTextColour()

        self.rich_text.BeginTextColour(wx.BLUE)
        self.rich_text.WriteText("這是藍色文字。\n")
        self.rich_text.EndTextColour()

        self.rich_text.BeginTextColour(wx.BLACK)
        self.rich_text.WriteText("這是回到黑色的文字。\n")
        self.rich_text.EndTextColour()

        self.rich_text.WriteText("這是文字。\n")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
