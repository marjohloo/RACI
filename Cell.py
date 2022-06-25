########################################################################
#
# Kerry's Assessment Tracker
#
# A tool to track pupil progress using a simple traffic light system.
#
# https://github.com/marjohloo/raci
#
# Copyright 2022 Martin Looker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
########################################################################

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from   ttkbootstrap.constants import *

# Project imports
from Raci import *

# Useful characters ← ↑ → ↓ × ▲ ► ▼ ◄ ˂ ˃ ˄ ˅

STYLE_FRAME = False
PAD         = 1
WIDTH_ROW   = 32
WIDTH_COL   = 16
WIDTH_BUT   = 1

class Cell:

    def __init__(self, raci, parent, row, col, type, value):
        self.raci       = raci
        self.row       = row
        self.col       = col
        self.type      = type
        self.var       = ttk.StringVar(value=value)
        self.var.trace_add("write", lambda *_: self.var_write())
        self.frame     = ttk.Frame(parent)
        if STYLE_FRAME:
            if row & 0x1:
                if col & 0x1:
                    self.frame.configure(bootstyle="light")
                else:
                    self.frame.configure(bootstyle="dark")
            else:
                if col & 0x1:
                    self.frame.configure(bootstyle="dark")
                else:
                    self.frame.configure(bootstyle="light")
        self.frame.grid(column=self.col, row=self.row, sticky=(W, S, E))
        self.button      = None
        self.entry       = None
        self.button_ul   = None
        self.button_dr   = None
        if self.type == "data":
            self.button = ttk.Button(self.frame, textvariable=self.var, command=self.button_data)
            self.button.grid(column=0, row=0, sticky=(N, W, S, E), padx=PAD, pady=PAD)
            self.frame.columnconfigure(0, weight=1)
            index = 0
            if value in self.raci.roles:
                index = self.raci.roles.index(value)
            self.data_style(index)
            self.raci.saved = False
            #self.raci.window.update()
            #print(self.frame.grid_bbox())
        elif self.type == "row":
            self.button_ul   = ttk.Button(self.frame, text="˄", width=WIDTH_BUT, command=self.button_row_up,    bootstyle="primary")
            self.button      = ttk.Button(self.frame, text="×", width=WIDTH_BUT, command=self.button_row_del,   bootstyle="danger")
            self.button_dr   = ttk.Button(self.frame, text="˅", width=WIDTH_BUT, command=self.button_row_down,  bootstyle="primary")
            self.entry       = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,         bootstyle="primary")
            self.button_ul.grid  (column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.button.grid     (column=1, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.button_dr.grid  (column=2, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.entry.grid      (column=3, row=0, sticky=(N, W, S, E), padx=PAD,     pady=PAD)
            self.frame.columnconfigure(3, weight=1)
            self.view()
            self.raci.saved = False
        elif self.type == "col":
            self.button_ul   = ttk.Button   (self.frame, text="˂", width=WIDTH_BUT, command=self.button_col_left,  bootstyle="info")
            self.button      = ttk.Button   (self.frame, text="×", width=WIDTH_BUT, command=self.button_col_del,   bootstyle="danger")
            self.button_dr   = ttk.Button   (self.frame, text="˃", width=WIDTH_BUT, command=self.button_col_right, bootstyle="info")
            self.entry       = ttk.Entry    (self.frame,           width=WIDTH_COL, textvariable=self.var,         bootstyle="info")
            self.button_ul.grid  (column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=(PAD,0))
            self.button.grid     (column=1, row=0, sticky=(N, W, S, E), padx=PAD,     pady=(PAD,0))
            self.button_dr.grid  (column=2, row=0, sticky=(N, W, S, E), padx=(0,PAD), pady=(PAD,0))
            self.entry.grid      (column=0, row=1, sticky=(N, W, S, E), padx=PAD, pady=PAD, columnspan=3)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.view()
            self.raci.saved = False
        elif self.type == "origin":
            self.button_ul = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.raci.row_add,     bootstyle="primary")
            self.button    = ttk.Button(self.frame, text="*", width=WIDTH_BUT, command=self.raci.view_toggle, bootstyle="success")
            self.button_dr = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.raci.col_add,     bootstyle="info")
            self.entry     = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,        bootstyle="dark")
            if self.col == 0:
                # Arrange like a row (for now)
                self.button_ul.grid(column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.button.grid   (column=1, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.button_dr.grid(column=2, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.entry.grid    (column=3, row=0, sticky=(N, W, S, E), padx=PAD,     pady=PAD)
                self.frame.columnconfigure(3, weight=1)
                # Force an update
                self.raci.window.update()
                # Get size
                x, y, w, h = self.frame.grid_bbox()
                # Apply width as minimum width for column
                self.raci.window.columnconfigure(self.col, minsize=w)
            # Now arrange as we want them
            self.frame.columnconfigure(3, weight=0)
            self.button_ul.grid(column=0, row=1, sticky=(N, W, S, E), padx=(PAD,0), pady=(0,PAD))
            self.button.grid   (column=1, row=1, sticky=(N, W, S, E), padx=PAD,     pady=(0,PAD))
            self.button_dr.grid(column=2, row=1, sticky=(N, W, S, E), padx=(0,PAD), pady=(0,PAD))
            self.entry.grid    (column=0, row=0, sticky=(N, W, S, E), padx=PAD, pady=PAD, columnspan=3)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.view()

    def var_write(self):
        # print(f'var_write       ({self.row}, {self.col})')
        self.raci.saved = False

    def button_data(self):
        print(f'Cell.button_data()')
        value = self.var.get()
        print(f'    value={value}')
        index = 0
        print(f'    index={index}')
        if value in self.raci.roles:
            index = self.raci.roles.index(value)
            print(f'    index={index}')
            index += 1
            if index >= len(self.raci.roles):
                index = 0
        value = self.raci.roles[index]
        print(f'    value={value}, index={index}')
        self.var.set(value)
        self.data_style(index)

    def button_row_del(self):
        # print(f'button_row_del  ({self.row}, {self.col})')
        self.raci.row_del(self.row)

    def button_col_del(self):
        # print(f'button_col_del  ({self.row}, {self.col})')
        self.raci.col_del(self.col)

    def button_row_up(self):
        # print(f'button_row_up   ({self.row}, {self.col})')
        if self.row > 1:
            self.raci.row_swap(self.row, self.row-1)

    def button_row_down(self):
        # print(f'button_row_down ({self.row}, {self.col})')
        if self.row < self.raci.rows - 1:
            self.raci.row_swap(self.row, self.row+1)

    def button_col_left(self):
        # print(f'button_col_left ({self.row}, {self.col})')
        if self.col > 1:
            self.raci.col_swap(self.col, self.col-1)

    def button_col_right(self):
        # print(f'button_col_right({self.row}, {self.col})')
        if self.col < self.raci.cols - 1:
            self.raci.col_swap(self.col, self.col+1)

    def data_style(self, index):
        if index >= len(self.raci.styles):
            index = 0
        self.button.configure(bootstyle=self.raci.styles[index])

    def grid(self):
        self.frame.grid(column=self.col, row=self.row, sticky=(W, S, E))
        if self.type == "row":
            if self.row == 1:
                self.button_ul.configure(state="disabled")
            else:
                self.button_ul.configure(state="normal")
            if self.row == self.raci.rows-1:
                self.button_dr.configure(state="disabled")
            else:
                self.button_dr.configure(state="normal")
        elif self.type == "col":
            if self.col == 1:
                self.button_ul.configure(state="disabled")
            else:
                self.button_ul.configure(state="normal")
            if self.col == self.raci.cols-1:
                self.button_dr.configure(state="disabled")
            else:
                self.button_dr.configure(state="normal")


    def view(self):
        if self.type == "row":
            if self.raci.view == "max":
                self.button_ul.grid()
                self.button_dr.grid()
                self.button.grid()
            else:
                self.button.grid_remove()
                self.button_dr.grid_remove()
                self.button_ul.grid_remove()
        elif self.type == "col":
            if self.raci.view == "max":
                self.button_ul.grid()
                self.button.grid()
                self.button_dr.grid()
            else:
                self.button_dr.grid_remove()
                self.button.grid_remove()
                self.button_ul.grid_remove()
        elif self.type == "origin":
            if self.raci.view == "max":
                self.button.configure(bootstyle="success")
            else:
                self.button.configure(bootstyle="success-outline")

    def move(self, row, col):
        self.row = row
        self.col = col
        self.grid()

    def destroy(self):
        if self.button != None:
            self.button.destroy()
        if self.entry != None:
            self.entry.destroy()
        if self.button_ul != None:
            self.button_ul.destroy()
        if self.button_dr != None:
            self.button_dr.destroy()
        self.frame.destroy()

    def key(row, col):
        return f'R{row:02}C{col:02}'