import tkinter as tk

def add_entry():
    description = description_entry.get()
    amount = amount_entry.get()
    listbox.insert(tk.END, f"{description}: {amount} €")
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Einfacher Budget Planer")

tk.Label(root, text="Beschreibung").pack()
description_entry = tk.Entry(root)
description_entry.pack()

tk.Label(root, text="Betrag (€)").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Hinzufügen", command=add_entry).pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

root.mainloop()
