from tkinter import font as ft

font = {}
font['family'] = 'Helvetica'
font['header1'] = (font['family'], 24)
font['header2'] = (font['family'], 16)
font['header3'] = (font['family'], 12)
font['mono'] = ""
def font_mono():
    fam = list(ft.families())
    if font['mono'] == "":
        if 'Courier' in fam:
            font['mono'] = 'Courier'
        elif 'courier' in fam: 
            font['mono'] = 'courier'
        elif 'Monaco' in fam:
            font['mono'] = 'Monaco'
        elif 'Monospace' in fam:
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