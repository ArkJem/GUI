from tkinter import ttk
from tkinter import *
from Calculator import eval_trig

def update_display(value):
    current_text = display.get()
    new_text = current_text + value
    display.set(new_text)

root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
root.option_add('*tearOff', FALSE)

# MENU
menu = Menu(root)
root.config(menu=menu)

# File section
filemenu = Menu(menu)
menu.add_cascade(label='Plik', menu=filemenu)
filemenu.add_command(label='Nowy')
filemenu.add_command(label='Otwórz...')
filemenu.add_separator()
filemenu.add_command(label='Wyjście', command=root.quit)

# Help section
helpmenu = Menu(menu)
menu.add_cascade(label='Pomoc', menu=helpmenu)
helpmenu.add_command(label='Informacje... ')

root.title("test1")
root.geometry("400x400")

content.grid(column=0, row=0, sticky=(N, S, E, W))

display = StringVar()
display.set("")

#Tworzy miejsce, gdzie bedzie mozna wpisywac dane
a = Entry(content, textvariable=display, font=("Arial", 18), justify="right")
a.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="n")  #sticky pozwala na umiejscowienie elementów w obszarze content


#columnconfigure i rowconfigure https://tkdocs.com/tutorial/grid.html
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.rowconfigure(0, weight=1)

row_val = 1
col_val = 0

button_labels = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

for label in button_labels:
    if label == '=':
        ttk.Button(content, text=label).grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")
    elif label == 'C':
        ttk.Button(content, text=label).grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")
    else:
        ttk.Button(content, text=label, command=lambda l=label: update_display(l)).grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

root.mainloop()