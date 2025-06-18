#erstellt von Kubilay Yildirim, Jonas Egger, Valentin Rauter
#dies ist ein Budget Planer, sprich man gibt seine Einkommen und Ausgaben ein.
#somit hat man sein Geld besser im Überblick.
#sollte etwas kreatives sein und sich als nützlich erweisen.

import tkinter as tk  # GUI-Bibliothek
from tkinter import messagebox
from tkinter import ttk
from planner import BudgetPlanner, Entry  # Externe Datei planner.py

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budgetplaner")
        self.planer = BudgetPlanner()

        self.erstelle_oberfläche()
        self.lade_einträge()

    def erstelle_oberfläche(self):
        eingabe_rahmen = tk.Frame(self.root)
        eingabe_rahmen.pack(pady=10)

        tk.Label(eingabe_rahmen, text="Beschreibung").grid(row=0, column=0)
        self.beschreibung_eingabe = tk.Entry(eingabe_rahmen)
        self.beschreibung_eingabe.grid(row=0, column=1)

        tk.Label(eingabe_rahmen, text="Betrag (€)").grid(row=1, column=0)
        self.betrag_eingabe = tk.Entry(eingabe_rahmen)
        self.betrag_eingabe.grid(row=1, column=1)

        tk.Label(eingabe_rahmen, text="Typ").grid(row=2, column=0)
        self.typ_var = tk.StringVar(value="Einnahme")
        ttk.Combobox(eingabe_rahmen, textvariable=self.typ_var, values=["Einnahme", "Ausgabe"]).grid(row=2, column=1)

        tk.Button(eingabe_rahmen, text="Hinzufügen", command=self.eintrag_hinzufügen).grid(row=3, column=0, columnspan=2, pady=5)

        self.liste = tk.Listbox(self.root, width=80, height=15)
        self.liste.pack(pady=10)

        tk.Button(self.root, text="Eintrag löschen", command=self.eintrag_löschen).pack(pady=5)

        self.kontostand_label = tk.Label(self.root, text="Kontostand: 0.00 €", font=("Arial", 12, "bold"))
        self.kontostand_label.pack(pady=5)

        self.hinweis_label = tk.Label(
            self.root,
            text="Hinweis: Bei Einnahmen mit 'Lohn' werden automatisch 20 % Steuern abgezogen.",
            fg="gray"
        )
        self.hinweis_label.pack(pady=5)

    def eintrag_hinzufügen(self):
        beschreibung = self.beschreibung_eingabe.get().strip()
        try:
            betrag = float(self.betrag_eingabe.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte einen gültigen Betrag eingeben.")
            return
        typ = self.typ_var.get()

        # Übersetzen: Deutsch → intern Englisch
        typ_englisch = "income" if typ == "Einnahme" else "expense"

        nach_steuer_betrag = betrag
        steuer_abgezogen = False

        if typ_englisch == "income" and "lohn" in beschreibung.lower():
            nach_steuer_betrag = betrag * 0.8
            steuer_abgezogen = True

        if steuer_abgezogen:
            beschreibung += f" (nach Steuern von {betrag:.2f} €: {nach_steuer_betrag:.2f} €)"

        eintrag = Entry(typ_englisch, beschreibung, nach_steuer_betrag)
        self.planer.add_entry(eintrag)

        self.beschreibung_eingabe.delete(0, tk.END)
        self.betrag_eingabe.delete(0, tk.END)

        self.lade_einträge()

    def eintrag_löschen(self):
        auswahl = self.liste.curselection()
        if not auswahl:
            messagebox.showwarning("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return

        index = auswahl[0]
        bestätigen = messagebox.askyesno("Eintrag löschen", "Möchtest du diesen Eintrag wirklich löschen?")
        if bestätigen:
            del self.planer.entries[index]
            self.planer.save_entries()
            self.lade_einträge()

    def lade_einträge(self):
        self.liste.delete(0, tk.END)
        for eintrag in self.planer.list_entries():
            vorzeichen = "+" if eintrag.type == "income" else "-"
            typ_deutsch = "Einnahme" if eintrag.type == "income" else "Ausgabe"
            self.liste.insert(tk.END, f"{eintrag.date} | {vorzeichen}{eintrag.amount:.2f} € | {typ_deutsch} | {eintrag.description}")

        einnahmen, ausgaben, kontostand = self.planer.get_summary()
        self.kontostand_label.config(
            text=f"Kontostand: {kontostand:.2f} €",
            fg="green" if kontostand >= 0 else "red"
        )

        # Letzter Lohn (nach Steuern)
        letzter_lohn = None
        for eintrag in reversed(self.planer.list_entries()):
            if eintrag.type == "income" and "lohn" in eintrag.description.lower():
                letzter_lohn = eintrag.amount
                break

        if letzter_lohn:
            min_sparen = letzter_lohn * 0.05
            max_sparen = letzter_lohn * 0.10
            tipp_sparen = f" Spartipp: Du solltest ca. {min_sparen:.2f}–{max_sparen:.2f} € (5–10 % von deinem Lohn) zurücklegen."

            min_essen = letzter_lohn * 0.05
            max_essen = letzter_lohn * 0.10
            tipp_essen = f" Essens-Ausgaben: Ca. {min_essen:.2f}–{max_essen:.2f} € (5–10 % deines Lohns) als Budget einplanen."
        else:
            tipp_sparen = " Spartipp: Lege bei regelmäßigem Einkommen idealerweise 5–10 % davon zurück."
            tipp_essen = " Essens-Ausgaben: Budgetiere ca. 5–10 % deines Einkommens fürs Essen."

        gesamter_tipp = tipp_sparen + "\n" + tipp_essen

        if hasattr(self, "spartipp_label"):
            self.spartipp_label.config(text=gesamter_tipp)
        else:
            self.spartipp_label = tk.Label(self.root, text=gesamter_tipp, fg="blue", justify="left")
            self.spartipp_label.pack(pady=5)

def main():
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
