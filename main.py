#erstellt von Kubilay Yildirim, Jonas Egger, Valentin Rauter
#dies ist ein Budget Planer, sprich man gibt seine Einkommen und Ausgaben ein.
#somit hat man sein Geld besser im Überblick.
#sollte etwas kreatives sein und sich als nützlich erweisen.

import tkinter as tk  # bibliothek
from tkinter import messagebox  # bibliothek
from tkinter import ttk  # bibliothek
from planner import BudgetPlanner, Entry  # bibliothek

class BudgetGUI:  # klasse des budget planers
    def _init_(self, root):  # werte
        self.root = root
        self.root.title("Budget Planer")  # titel
        self.planner = BudgetPlanner()

        self.setup_widgets()
        self.load_entries()

    def setup_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Beschreibung").grid(row=0, column=0)
        self.description_entry = tk.Entry(input_frame)
        self.description_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Betrag (€)").grid(row=1, column=0)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Typ").grid(row=2, column=0)
        self.type_var = tk.StringVar(value="einkommen")
        ttk.Combobox(input_frame, textvariable=self.type_var, values=["einkommen", "ausgaben"]).grid(row=2, column=1)

        tk.Button(input_frame, text="Hinzufügen", command=self.add_entry).grid(row=3, column=0, columnspan=2, pady=5)

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

        tk.Button(self.root, text="Eintrag löschen", command=self.delete_entry).pack(pady=5)

        self.summary_label = tk.Label(self.root, text="Übriges Geld: 0.00 €", font=("Arial", 12, "bold"))
        self.summary_label.pack(pady=5)

    def add_entry(self):
        desc = self.description_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gültigen Betrag eingeben.")
            return
        typ = self.type_var.get()

        entry = Entry(typ, desc, amount)
        self.planner.add_entry(entry)

        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.load_entries()

    def delete_entry(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return

        index = selection[0]
        confirm = messagebox.askyesno("Eintrag löschen", "Möchtest du diesen Eintrag wirklich löschen?")
        if confirm:
            del self.planner.entries[index]
            self.planner.save_entries()
            self.load_entries()

    def load_entries(self):
        self.listbox.delete(0, tk.END)
        for e in self.planner.list_entries():
            sign = "+" if e.type == "einkommen" else "-"
            self.listbox.insert(tk.END, f"{e.date} | {sign}{e.amount:.2f} € | {e.description}")

        income, expense, balance = self.planner.get_summary()
        self.summary_label.config(
            text=f"Übriges Geld: {balance:.2f} €",
            fg="green" if balance >= 0 else "red"
        )

def main():
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()

if _name_ == "_main_":
    main()
