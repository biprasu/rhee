#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

This example creates a simple toolbar.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx
import os
import traceback
import ply.lex as lex
import ply.yacc as yacc
import NepLexer as NepL
import NepParser as NepP
import NepInterpreter as NepI


KeyInput = ''
class InputHandler(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(InputHandler, self).__init__(*args, **kw)
        self.InitUI()
        self.SetSize((200, 200))
        self.SetTitle(u"डाटा दिनुहोस")
        
        
    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label=u'डाटा दिनुहोस')

        font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        font2 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        sb.SetFont(font1)
        
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        self.tcH = wx.TextCtrl(pnl)
        self.tcH.SetFont(font2)
        hbox1.Add(self.tcH, flag=wx.LEFT, border=5)
        sbs.Add(hbox1)
        
        pnl.SetSizer(sbs)
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, 
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
    def OnOk(self, e):
        global KeyInput
        KeyInput = self.tcH.GetValue();
        self.Destroy()

    def OnClose(self, e):
        self.Destroy()

class Example(wx.Frame):
    
    filePath = ""

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        self.Centre()
        self.Maximize()
        self.Show(True)
    
    

    def write(self, text, filepath = None):
        filepath = filepath if filepath else self.filePath
        try:
            print "Printed"
            open (filepath,"w").write(text.encode("UTF8"))
            print "Printed"
        except Exception,e:
            pass

    def InitUI(self):
        toolbar = self.CreateToolBar()
        ntool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('icons/gtk-new.png'))
        otool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('icons/gtk-open.png'))
        stool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('icons/gtk-save.png'))
        satool = toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('icons/gtk-save-as.png'))
        qtool = toolbar.AddLabelTool(wx.ID_ANY, 'Quit', wx.Bitmap('icons/gtk-cancel.png'))
        rtool = toolbar.AddLabelTool(wx.ID_ANY, 'Run', wx.Bitmap('icons/gtk-go-forward-ltr.png'))
        stop = toolbar.AddLabelTool(wx.ID_ANY, 'Stop', wx.Bitmap('icons/gtk-no.png'))


        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.newFile, ntool)
        self.Bind(wx.EVT_TOOL, self.openFile, otool)
        self.Bind(wx.EVT_TOOL, self.saveFile, stool)
        self.Bind(wx.EVT_TOOL, self.saveAsFile, satool)
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        self.Bind(wx.EVT_TOOL, self.RunProgram, rtool)
        # self.Bind(wx.EVT_TOOL, self.getInputData, stop)



        self.panel = wx.Panel(self)

        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(9)
        self.font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font1.SetPointSize(18)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # st1 = wx.StaticText(panel, label='Class Name')
        # st1.SetFont(font)
        # hbox1.Add(st1, flag=wx.RIGHT, border=8)
        # tc = wx.TextCtrl(panel)
        # hbox1.Add(tc, proportion=1)
        # vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # vbox.Add((-1, 10))

        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # st2 = wx.StaticText(panel, label='Rhee')
        # st2.SetFont(font1)
        # hbox2.Add(st2)
        # vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        self.vbox.Add((-1, 10))

        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc2 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)

        font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.tc2.SetFont(font1)
        # self.tc2.SetFont(font1)
        self.hbox3.Add(self.tc2, proportion=2, flag=wx.EXPAND)
        self.vbox.Add(self.hbox3, proportion=2, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)

        self.vbox.Add((-1, 25))

        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc3 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.tc3.SetFont(font1)

        # self.tc3.SetEditable(True)
        self.hbox4.Add(self.tc3, proportion=1, flag=wx.EXPAND)
        self.vbox.Add(self.hbox4, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        self.vbox.Add((-1, 25))

        # hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        # cb1 = wx.CheckBox(panel, label='Case Sensitive')
        # cb1.SetFont(font)
        # hbox4.Add(cb1)
        # cb2 = wx.CheckBox(panel, label='Nested Classes')
        # cb2.SetFont(font)
        # hbox4.Add(cb2, flag=wx.LEFT, border=10)
        # cb3 = wx.CheckBox(panel, label='Non-Project classes')
        # cb3.SetFont(font)
        # hbox4.Add(cb3, flag=wx.LEFT, border=10)
        # vbox.Add(hbox4, flag=wx.LEFT, border=10)

        # vbox.Add((-1, 25))

        # hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        # btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        # hbox5.Add(btn1,flag=wx.RIGHT, border=8)
        # # btn2 = wx.Button(panel, label='Close', size=(70, 30))
        # # hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        # st3 = wx.StaticText(panel, label='Rhee')
        # st3.SetFont(font1)
        # hbox5.Add(st3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border =10)
        # vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        self.panel.SetSizer(self.vbox)

        self.SetSize((250, 200))
        self.SetTitle(u'ऋ - नेपाली भाषामा प्रोग्राम्मिंग')
        ico = wx.Icon('rhee.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.Centre()
        # self.getInputData()
        
    def getInputData(self):
        chgdep = InputHandler(None, 
            title='Input')
        chgdep.ShowModal()
        chgdep.Destroy()
        return KeyInput

    def newFile(self, e):
        ret  = wx.MessageBox(u'तपाई कोडलाई save गर्न चाहनुहुन्छ?', 'Question', 
                    wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT, self)

        if ret == wx.YES:
            self.saveFile(e)
        elif ret == wx.CANCEL:
            return

        self.tc2.SetValue("")
        self.filePath = ""

    def openFile(self, e):
        wildcard = "Rhee source (*.rhee)|*.rhee|" \
                    "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, u"फाइल छान्नु होस", os.getcwd(),"", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath()
            # print unicode(open(dialog.GetPath(),"r").read(),'UTF8')
            self.tc2.SetValue(unicode(open(dialog.GetPath(),"r").read(),'UTF8'))
        dialog.Destroy()
    
    def saveFile(self, e):
        wildcard = "Rhee source (*.rhee)|*.rhee|" \
                    "All files (*.*)|*.*"
        if not self.filePath:
            dialog = wx.FileDialog(None, u"फाइल save गर्न ठाउँ छान्नु होस", os.getcwd(),"", wildcard, wx.SAVE|wx.OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                self.filePath = dialog.GetPath()
            dialog.Destroy()
        self.write(self.tc2.GetValue())

    def saveAsFile(self, e):
        wildcard = "Rhee source (*.rhee)|*.rhee|" \
                    "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, u"फाइल save गर्न ठाउँ छान्नु होस", os.getcwd(),"", wildcard, wx.SAVE|wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath()
            # print self.tc2.GetValue()
            # print dialog.GetPath()
        dialog.Destroy()

        self.write(self.tc2.GetValue())

    def RunProgram(self, e):
        try:
            input = self.tc2.GetValue()
            lexer = lex.lex(module=NepL)
            parser = yacc.yacc(module=NepP)
            ast = parser.parse(input, lexer=lexer)
            #print ast
            self.tc3.SetValue('')
            NepI.interpret(ast,None,self)
        except Exception, e:
            print e.message



    
    def StopProgram(self, e):
        a = wx.MessageBox()
        print a
    
    def OnQuit(self, e):
        ret  = wx.MessageBox(u'प्रोग्राम बन्द गर्दिम त?', 'Question', 
                    wx.YES_NO | wx.NO_DEFAULT, self)

        if ret == wx.YES:
            self.Close()


def main():
    global win
    ex = wx.App()
    win = Example(None)
    ex.MainLoop()    



if __name__ == '__main__':
    main()