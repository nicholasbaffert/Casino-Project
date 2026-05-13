import tkinter as tk
from tkinter import messagebox
import json
import os

# IMPORTAZIONE GIOCHI
# Assicurati che il codice della roulette sia salvato in un file chiamato 'roulette.py' nella stessa cartella
from Game.roulette import Roulette  
# Nota: tieni l'importazione di blackjack attiva se hai il file pronto
# from Game import blackjack  

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
        self.root.geometry("400x450") # Aumentato leggermente per far spazio ai bottoni
        
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
            self.saldo_attuale = 1000
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

        # Bottoni Giochi - Ora vengono visualizzati tutti correttamente
        tk.Button(self.container, text="Roulette 🎡", width=20, command=self.avvia_roulette_game).pack(pady=5)
        tk.Button(self.container, text="Dadi 🎲 (-10€)", width=20, command=self.gioca_dadi).pack(pady=5)
        tk.Button(self.container, text="Blackjack 🃏", width=20, command=self.avvia_blackjack_game).pack(pady=5)
        tk.Button(self.container, text="Esci", width=20, fg="red", command=self.esci).pack(pady=20)

    def avvia_roulette_game(self):
        # Disabilita temporaneamente la finestra del menu per evitare click multipli
        self.root.withdraw()
        
        # Avvia la classe Roulette passandogli il menu (self.root), il saldo e la funzione di ritorno
        Roulette(self.root, self.saldo_attuale, self.aggiorna_saldo_da_gioco)

    def avvia_blackjack_game(self):
        # CORRETTO: Spostato dentro la classe con il rientro giusto
        messagebox.showinfo("Blackjack", "Avvio del gioco Blackjack...")
        # blackjack.start_game(self.root, self.utente_attuale, self.saldo_attuale)

    def aggiorna_saldo_da_gioco(self, nuovo_saldo):
        """ Questa funzione viene chiamata dalla Roulette quando viene chiusa """
        self.saldo_attuale = nuovo_saldo
        
        # Rende di nuovo visibile il menu principale
        self.root.deiconify()
        
        # Aggiorna la grafica del menu principale
        self.label_info.config(text=f"👤 {self.utente_attuale}  |  💰 {self.saldo_attuale}€")
        
        # Salva immediatamente nel file JSON per sicurezza
        dati = carica_dati()
        dati[self.utente_attuale] = self.saldo_attuale
        salva_dati(dati)

    def gioca_dadi(self):
        costo = 10
        if self.saldo_attuale >= costo:
            self.saldo_attuale -= costo
            self.label_info.config(text=f"👤 {self.utente_attuale}  |  💰 {self.saldo_attuale}€")
            messagebox.showinfo("Dadi", "Hai puntato 10€! Buona fortuna.")
            
            # Salva i dati dopo la scommessa dei dadi
            dati = carica_dati()
            dati[self.utente_attuale] = self.saldo_attuale
            salva_dati(dati)
        else:
            messagebox.showerror("Errore", "Saldo insufficiente!")

    def esci(self):
        if self.utente_attuale:
            dati = carica_dati()
            dati[self.utente_attuale] = self.saldo_attuale
            salva_dati(dati)
        self.root.destroy() # .destroy() è più sicuro di .quit() per chiudere le finestre Tkinter


if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoApp(root)
    root.mainloop()
