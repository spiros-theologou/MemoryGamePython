from tkinter import *
from Menu import Menu

"""Εδώ υλοποιείται το master window
 και καλείται η κλάση Menu που θα παρουσιάσει το 
 αρχικό μενού στον χρήστη"""
master = Tk()
master.geometry("1920x1024")
master.configure(background="green")
master.minsize(1920, 1024)

# Προσθήκη τίτλου
master.title("Memory Card Game in Python")

# Κλήση της κλάσης Menu
main_menu = Menu(master)

# Έναρξη του mainloop() του παιχνιδιού
master.mainloop()
