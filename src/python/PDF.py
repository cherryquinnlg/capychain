import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.image('/Users/guoziting/Desktop/capychain/logo.png', 10, 12, 33)
        self.set_font('Arial', 'B', 11)
        # self.cell(self.WIDTH - 80)
        # self.ln(40)

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images=None):
        # Determine how many plots there are per page and set positions
        # and margins accordingly

        self.image('/Users/guoziting/Desktop/capychain/test.png', 15, 35, self.WIDTH - 30)
        # self.image(images[0], 15, 25, self.WIDTH - 30)
        # self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        # self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)

    # /Users/guoziting/Desktop/capychain/capybara_ps.png

    def print_page(self, images=None):
        # Generates the report
        self.add_page()
        self.page_body(images=None)


pdf = PDF()
pdf.print_page()

pdf.output('/Users/guoziting/Desktop/capychain/account_summary.pdf', 'F')


import yfinance as yf
tickers = yf.Tickers("MSFT")
tickers.tickers["MSFT"].info
data = yf.download("BTC", start="2017-01-01", end="2017-04-30")