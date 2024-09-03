from tkinter import ttk
from tkinter import *
from Calculator import eval_trig

root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
root.option_add('*tearOff', FALSE)

# MENU
menu = Menu(root)
root.config(menu=menu)

# File section
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Nowy')
filemenu.add_command(label='Otwórz...')
filemenu.add_separator()
filemenu.add_command(label='Wyjście', command=root.quit)

# Help section
helpmenu = Menu(menu)
menu.add_cascade(label='Pomoc', menu=helpmenu)
helpmenu.add_command(label='Informacje... ')

root.title("test1")
root.geometry("400x600")

content.grid(column=0, row=0, sticky=(N, S, E, W))

#Tworzy miejsce, gdzie bedzie mozna wpisywac dane
a = Entry(content, font=('Calibri', 40))
a.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="n")  #sticky pozwala na umiejscowienie elementów w obszarze content


#columnconfigure i rowconfigure https://tkdocs.com/tutorial/grid.html
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.rowconfigure(0, weight=1)

root.mainloop()