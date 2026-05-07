import tkinter as tk
from tkinter import messagebox
import json
import os

# Nome del file database
DB_FILE = "utenti.json"

def carica_dati():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salva_dati(dati):
    with open(DB_FILE, "w") as f:
        json.dump(dati, f, indent=4)

class CasinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Gold")
        self.root.geometry("400x400")
        
        self.utente_attuale = None
        self.saldo_attuale = 0
        
        # Contenitore principale
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both")
        
        self.mostra_schermata_login()

    def pulisci_schermata(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostra_schermata_login(self):
        self.pulisci_schermata()
        
        tk.Label(self.container, text="BENVENUTO AL CASINÒ", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.container, text="Inserisci Username:").pack()
        
        self.entry_user = tk.Entry(self.container)
        self.entry_user.pack(pady=5)
        
        tk.Button(self.container, text="Accedi / Registrati", command=self.gestisci_accesso, bg="gold", width=20).pack(pady=20)

    def gestisci_accesso(self):
        username = self.entry_user.get().strip()
        if not username:
            messagebox.showwarning("Errore", "Inserisci un nome utente!")
            return
        
        dati = carica_dati()
        
        if username in dati:
            # LOGIN
            self.utente_attuale = username
            self.saldo_attuale = dati[username]
            messagebox.showinfo("Login", f"Bentornato {username}!")
        else:
            # REGISTRAZIONE
            self.utente_attuale = username
            self.saldo_attuale =  1000
            dati[username] = self.saldo_attuale
            salva_dati(dati)
            messagebox.showinfo("Benvenuto", f"Nuovo utente registrato! Ti abbiamo regalato {self.saldo_attuale}€")
        
        self.mostra_menu_principale()

    def mostra_menu_principale(self):
        self.pulisci_schermata()
        
        # Header Info
        self.label_info = tk.Label(self.container, text=f"👤 {self.utente_attuale}  |  💰 {self.saldo_attuale}€", 
                                  font=("Arial", 10, "bold"), fg="darkgreen")
        self.label_info.pack(pady=10)

        tk.Label(self.container, text="SCEGLI UN GIOCO", font=("Arial", 14)).pack(pady=10)

        # Bottoni Giochi
        tk.Button(self.container, text="Roulette 🎡", width=20, command=lambda: self.gioca("Roulette")).pack(pady=5)
        tk.Button(self.container, text="Dadi 🎲 (-10€)", width=20, command=self.gioca_dadi).pack(pady=5)
        tk.Button(self.container, text="Esci", width=20, fg="red", command=self.esci).pack(pady=20)

    def gioca_dadi(self):
        costo = 10
        if self.saldo_attuale >= costo:
            self.saldo_attuale -= costo
            self.label_info.config(text=f"👤 {self.utente_attuale}  |  💰 {self.saldo_attuale}€")
            # Qui andrebbe la logica del gioco dei dadi
            messagebox.showinfo("Dadi", "Hai puntato 10€! Buona fortuna.")
        else:
            messagebox.showerror("Errore", "Saldo insufficiente!")

    def gioca(self, nome_gioco):
        messagebox.showinfo("Info", f"Avvio di {nome_gioco}...")

    def esci(self):
        # Salva il saldo prima di chiudere
        dati = carica_dati()
        dati[self.utente_attuale] = self.saldo_attuale
        salva_dati(dati)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoApp(root)
    root.mainloop()