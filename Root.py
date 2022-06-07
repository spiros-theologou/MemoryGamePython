from tkinter import *
from Menu import Menu

"""Εδώ υλοποιείται το master window
 και καλείται η κλάση Menu που θα παρουσιάσει το 
 αρχικό μενού στον χρήστη"""
master = Tk()
master.geometry("1920x1024")
master.configure(background="green")
master.minsize(1920, 1024)

# Add title
master.title("Memory Card Game in Python")


main_menu = Menu(master)

master.mainloop()
