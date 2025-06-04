from planner import BudgetPlanner, Entry

def show_menu():
    print("\n=== Budget Planer ===")
    print("1) Eintrag hinzufügen")
    print("2) Alle Einträge anzeigen")
    print("3) Zusammenfassung")
    print("4) Beenden")

def prompt_entry():
    typ = input("Typ (income/expense): ").strip().lower()
    if typ not in ["income", "expense"]:
        print(" Ungültiger Typ.")
        return None
    description = input("Beschreibung: ")
    try:
        amount = float(input("Betrag (€): "))
    except ValueError:
        print(" Ungültiger Betrag.")
        return None
    return Entry(typ, description, amount)

def print_entries(entries):
    if not entries:
        print("Keine Einträge vorhanden.")
        return
    for e in entries:
        print(f"{e.date} | {e.type:8} | {e.amount:>7.2f} € | {e.description}")

def print_summary(planner):
    income, expense, balance = planner.get_summary()
    print(f"\n Einnahmen: {income:.2f} €")
    print(f" Ausgaben:  {expense:.2f} €")
    print(f" Saldo:     {balance:.2f} €\n")

def main():
    planner = BudgetPlanner()

    while True:
        show_menu()
        choice = input("Wähle Option (1–4): ")
        if choice == "1":
            entry = prompt_entry()
            if entry:
                planner.add_entry(entry)
                print(" Eintrag gespeichert.")
        elif choice == "2":
            print_entries(planner.list_entries())
        elif choice == "3":
            print_summary(planner)
        elif choice == "4":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == "__main__":
    main()
