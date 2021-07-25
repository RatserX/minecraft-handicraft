#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing

import wx

class WidgetService:
    def __init__(self, redirect: bool = False, filename: str = None, useBestVisual: bool = False, clearSigInt = True):
        self.__app: wx.App = wx.App(redirect, filename, useBestVisual, clearSigInt)
    
    def __del__(self):
        self.__app.DeletePendingEvents()
        self.__app.Destroy()
    
    def get_app(self):
        return self.__app
    
    def message_dialog_modal(self, parent: typing.Any, message: typing.Any, caption: typing.Any = wx.MessageBoxCaptionStr, style: typing.Literal[0] = wx.OK | wx.CENTRE, pos: wx.Point = wx.DefaultPosition):
        message_dialog: wx.MessageDialog = wx.MessageDialog(parent, message, caption, style, pos)
        
        message_dialog.ShowModal()
        message_dialog.Destroy()
