from tkinter import font as ft

font = {}
font['family'] = 'Helvetica'
font['header1'] = (font['family'], 24)
font['header2'] = (font['family'], 16)
font['header3'] = (font['family'], 12)
font['mono'] = ""
def font_mono():
    if font['mono'] == "":
        if 'Courier' in ft.families():
            font['mono'] = 'Courier'
        elif 'courier' in ft.families(): 
            font['mono'] = 'courier'
        elif 'Monaco' in ft.families():
            font['mono'] = 'Monaco'
        elif 'Monospace' in ft.families():
            font['mono'] = 'Monospace'
    return font['mono']

bg = {}
bg['header2'] = "#e1e1e1"
bg['i'] = "#7c8a8e"
bg['ni'] = bg['header2']
bg['u'] = "#7c8a8e"
bg['nu'] = bg['header2']
bg['iu'] = "#def0c8"
bg['inu'] = "#cbe9f2"
bg['niu'] = "#f1e7cd"
bg['ninu'] = "#f4e1dd"

fg = {}
fg['i'] = "#ffffff"
fg['u'] = "#ffffff"