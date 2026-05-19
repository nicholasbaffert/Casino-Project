import random
import tkinter as tk
from tkinter import messagebox


class BlackjackApp:

    def __init__(self, root, saldo_attuale, aggiorna_saldo_da_gioco):
        self.main_root = root
        self.root = tk.Toplevel(root)
        self.saldo_attuale = saldo_attuale
        self.aggiorna_saldo_da_gioco = aggiorna_saldo_da_gioco
        self.root.title("Blackjack")
        self.root.geometry("500x650")  # Allungato leggermente per l'area puntate
        self.root.configure(bg="#2c3e50")

        # Intercettiamo la "X" della finestra
        self.root.protocol("WM_DELETE_WINDOW", self.chiudi_gioco)

        # Variabili di gioco
        self.puntata_attuale = 0

        # Dati del mazzo
        self.semi_carte = {
            "Cuori": "♥️",
            "Quadri": "♦️",
            "Fiori": "♣️",
            "Picche": "♠️",
        }
        self.lista_carte = [
            "Asso",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Fante",
            "Regina",
            "Re",
        ]

        # Creazione UI
        self.crea_interfaccia()

        # Prepariamo la schermata per la prima puntata
        self.attendi_puntata()

    def crea_interfaccia(self):
        # Titolo
        titolo = tk.Label(
            self.root,
            text="🃏 BLACKJACK 🃏",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        titolo.pack(pady=10)

        # Mostra il saldo
        self.lbl_saldo = tk.Label(
            self.root,
            text=f"Saldo: {self.saldo_attuale}€",
            font=("Helvetica", 14, "bold"),
            bg="#2c3e50",
            fg="gold",
        )
        self.lbl_saldo.pack(pady=5)

        # AREA PUNTATA (Nuova)
        self.frame_puntata = tk.Frame(self.root, bg="#2c3e50")
        self.frame_puntata.pack(pady=10)

        tk.Label(
            self.frame_puntata,
            text="Inserisci Puntata (€):",
            font=("Helvetica", 11, "bold"),
            bg="#2c3e50",
            fg="white",
        ).grid(row=0, column=0, padx=5)

        self.entry_puntata = tk.Entry(
            self.frame_puntata, font=("Helvetica", 11), width=10
        )
        self.entry_puntata.grid(row=0, column=1, padx=5)
        self.entry_puntata.insert(0, "10")  # Valore di default

        self.btn_punta = tk.Button(
            self.frame_puntata,
            text="Scommetti 💰",
            font=("Helvetica", 10, "bold"),
            bg="#f1c40f",
            command=self.gestisci_puntata,
        )
        self.btn_punta.grid(row=0, column=2, padx=5)

        # Area Banco
        self.frame_banco = tk.LabelFrame(
            self.root,
            text="BANCO",
            font=("Helvetica", 12, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10,
        )
        self.frame_banco.pack(fill="x", padx=20, pady=5)

        self.lbl_carte_banco = tk.Label(
            self.frame_banco,
            text="",
            font=("Helvetica", 12),
            bg="#34495e",
            fg="white",
            wraplength=400,
            justify="center",
        )
        self.lbl_carte_banco.pack(pady=5)

        self.lbl_punti_banco = tk.Label(
            self.frame_banco,
            text="",
            font=("Helvetica", 11, "italic"),
            bg="#34495e",
            fg="#bdc3c7",
        )
        self.lbl_punti_banco.pack()

        # Area Giocatore
        self.frame_giocatore = tk.LabelFrame(
            self.root,
            text="GIOCATORE",
            font=("Helvetica", 12, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10,
        )
        self.frame_giocatore.pack(fill="x", padx=20, pady=5)

        self.lbl_carte_giocatore = tk.Label(
            self.frame_giocatore,
            text="",
            font=("Helvetica", 12),
            bg="#34495e",
            fg="white",
            wraplength=400,
            justify="center",
        )
        self.lbl_carte_giocatore.pack(pady=5)

        self.lbl_punti_giocatore = tk.Label(
            self.frame_giocatore,
            text="",
            font=("Helvetica", 11, "italic"),
            bg="#34495e",
            fg="#bdc3c7",
        )
        self.lbl_punti_giocatore.pack()

        # Area Pulsanti di Gioco
        self.frame_pulsanti = tk.Frame(self.root, bg="#2c3e50")
        self.frame_pulsanti.pack(pady=10)

        self.btn_hit = tk.Button(
            self.frame_pulsanti,
            text="Carta (Hit)",
            font=("Helvetica", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=12,
            command=self.hit,
        )
        self.btn_hit.grid(row=0, column=0, padx=10)

        self.btn_stand = tk.Button(
            self.frame_pulsanti,
            text="Stai (Stand)",
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=12,
            command=self.stand,
        )
        self.btn_stand.grid(row=0, column=1, padx=10)

        # Bottone per uscire
        self.btn_exit = tk.Button(
            self.root,
            text="Torna al Menu Principale ↩",
            font=("Helvetica", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            command=self.chiudi_gioco,
        )
        self.btn_exit.pack(pady=5)

    def attendi_puntata(self):
        # Blocca i bottoni di gioco finché non si punta
        self.btn_hit.config(state="disabled")
        self.btn_stand.config(state="disabled")
        self.btn_punta.config(state="normal")
        self.entry_puntata.config(state="normal")

        # Pulisce i vecchi testi grafici
        self.lbl_carte_giocatore.config(text="Effettua una puntata per iniziare")
        self.lbl_punti_giocatore.config(text="")
        self.lbl_carte_banco.config(text="In attesa delle fiches...")
        self.lbl_punti_banco.config(text="")

    def gestisci_puntata(self):
        try:
            puntata = int(self.entry_puntata.get().strip())
        except ValueError:
            messagebox.showerror(
                "Errore", "Inserisci un numero intero valido!", parent=self.root
            )
            return

        if puntata <= 0:
            messagebox.showerror(
                "Errore",
                "La puntata deve essere maggiore di 0€!",
                parent=self.root,
            )
            return

        if puntata > self.saldo_attuale:
            messagebox.showerror(
                "Errore",
                f"Saldo insufficiente! Hai solo {self.saldo_attuale}€.",
                parent=self.root,
            )
            return

        # Sottrae la puntata e aggiorna le variabili
        self.puntata_attuale = puntata
        self.saldo_attuale -= self.puntata_attuale
        self.lbl_saldo.config(text=f"Saldo: {self.saldo_attuale}€")

        # Disabilita i campi puntata durante la mano
        self.btn_punta.config(state="disabled")
        self.entry_puntata.config(state="disabled")

        # Avvia la partita vera e propria
        self.avvia_nuova_partita()

    def inizializza_mazzo(self):
        mazzo = []
        for seme in self.semi_carte.keys():
            for carta in self.lista_carte:
                mazzo.append((carta, seme))
        random.shuffle(mazzo)
        return mazzo

    def valore_carta(self, carta_tupla):
        nome_carta = carta_tupla[0]
        if nome_carta in ["Fante", "Regina", "Re"]:
            return 10
        elif nome_carta == "Asso":
            return 11
        else:
            return int(nome_carta)

    def calcola_punteggio(self, mano):
        punteggio = sum(self.valore_carta(carta) for carta in mano)
        num_assi = sum(1 for carta in mano if carta[0] == "Asso")

        while punteggio > 21 and num_assi > 0:
            punteggio -= 10
            num_assi -= 1
        return punteggio

    def formatta_mano(self, mano):
        return " , ".join(
            [f"{valore} di {self.semi_carte[seme]}" for valore, seme in mano]
        )

    def avvia_nuova_partita(self):
        # Setup iniziale dati
        self.mazzo = self.inizializza_mazzo()
        self.carte_giocatore = [self.mazzo.pop(), self.mazzo.pop()]
        self.carte_banco = [self.mazzo.pop(), self.mazzo.pop()]

        # Attiva pulsanti di gioco
        self.btn_hit.config(state="normal")
        self.btn_stand.config(state="normal")

        # Controllo Blackjack immediato
        punti_g = self.calcola_punteggio(self.carte_giocatore)
        punti_b = self.calcola_punteggio(self.carte_banco)

        if punti_g == 21 or punti_b == 21:
            self.aggiorna_grafica(nascondi_banco=False)
            self.concludi_partita()
        else:
            self.aggiorna_grafica(nascondi_banco=True)

    def aggiorna_grafica(self, nascondi_banco=True):
        punti_g = self.calcola_punteggio(self.carte_giocatore)
        self.lbl_carte_giocatore.config(
            text=f"🎴 Carte: {self.formatta_mano(self.carte_giocatore)}"
        )
        self.lbl_punti_giocatore.config(text=f"🔢 Punteggio totale: {punti_g}")

        if nascondi_banco:
            valore, seme = self.carte_banco[0]
            mano_coperta = (
                f"{valore} di {self.semi_carte[seme]} , [CARTA COPERTA]"
            )
            self.lbl_carte_banco.config(text=f"🎴 Carte: {mano_coperta}")
            self.lbl_punti_banco.config(
                text=f"🔢 Punteggio visibile: {self.valore_carta(self.carte_banco[0])}"
            )
        else:
            punti_b = self.calcola_punteggio(self.carte_banco)
            self.lbl_carte_banco.config(
                text=f"🎴 Carte: {self.formatta_mano(self.carte_banco)}"
            )
            self.lbl_punti_banco.config(text=f"🔢 Punteggio totale: {punti_b}")

    def hit(self):
        self.carte_giocatore.append(self.mazzo.pop())
        punteggio = self.calcola_punteggio(self.carte_giocatore)

        if punteggio >= 21:
            self.btn_hit.config(state="disabled")
            self.btn_stand.config(state="disabled")
            self.aggiorna_grafica(nascondi_banco=False)
            self.concludi_partita()
        else:
            self.aggiorna_grafica(nascondi_banco=True)

    def stand(self):
        self.btn_hit.config(state="disabled")
        self.btn_stand.config(state="disabled")

        punteggio_banco = self.calcola_punteggio(self.carte_banco)
        while punteggio_banco < 17:
            self.carte_banco.append(self.mazzo.pop())
            punteggio_banco = self.calcola_punteggio(self.carte_banco)

        self.aggiorna_grafica(nascondi_banco=False)
        self.concludi_partita()

    def concludi_partita(self):
        punti_g = self.calcola_punteggio(self.carte_giocatore)
        punti_b = self.calcola_punteggio(self.carte_banco)

        msg = ""
        moltiplicatore = 0  # Determina quanto vince il giocatore rispetto alla puntata

        if punti_g == 21 and len(self.carte_giocatore) == 2:
            if punti_b == 21 and len(self.carte_banco) == 2:
                msg = "🤝 Entrambi Blackjack! Pareggio."
                moltiplicatore = 1  # Restituisce la puntata
            else:
                msg = "🏆 BLACKJACK! Hai vinto!"
                moltiplicatore = 2.5  # Paga 2.5 volte la puntata (es. punti 10€, riprendi 25€)
        elif punti_b == 21 and len(self.carte_banco) == 2:
            msg = "📉 Il Banco ha fatto Blackjack. Hai perso."
        elif punti_g > 21:
            msg = "📉 Hai sballato! Il Banco vince."
        elif punti_b > 21:
            msg = "🏆 Il Giocatore vince! (Il Banco ha sballato)"
            moltiplicatore = 2  # Raddoppio
        elif punti_g > punti_b:
            msg = "🏆 Il Giocatore vince!"
            moltiplicatore = 2  # Raddoppio
        elif punti_b > punti_g:
            msg = "📉 Il Banco vince."
        else:
            msg = "🤝 È un pareggio!"
            moltiplicatore = 1  # Restituisce la puntata

        # Calcolo vincita reale e accredito sul saldo
        vincita_reale = int(self.puntata_attuale * moltiplicatore)
        self.saldo_attuale += vincita_reale
        self.lbl_saldo.config(text=f"Saldo: {self.saldo_attuale}€")

        messagebox.showinfo("Risultato Finale", msg, parent=self.root)

        # Chiede se rigiocare o tornare al menu
        scelta = messagebox.askyesno(
            "Nuova Partita", "Vuoi giocare un'altra mano?", parent=self.root
        )
        if scelta:
            self.attendi_puntata()
        else:
            self.chiudi_gioco()

    def chiudi_gioco(self):
        self.root.destroy()
        self.aggiorna_saldo_da_gioco(self.saldo_attuale)


if __name__ == "__main__":
    root = tk.Tk()

    def finto_aggiorna_saldo(nuovo_saldo):
        print(f"Saldo finale salvato: {nuovo_saldo}€")

    app = BlackjackApp(root, 1000, finto_aggiorna_saldo)
    root.mainloop()
