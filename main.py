#!/usr/bin/env python

"""
Создать программу, позволяющую вычислять систему линейных уравнений. 
"""
from tkinter import Tk
from window import main

__author__ = "___указать автора ___"
__copyright__ = "__указать копирайт, например___Copyright 2018, Nikolay Zhukov"
__email__ = "__указать почту___"


def start():
    root = Tk()
    main(root)
    root.mainloop()



if __name__ == '__main__':
    start()
