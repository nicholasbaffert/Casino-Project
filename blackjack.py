import random
import tkinter as tk
from tkinter import messagebox


class BlackjackApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("500x550")
        self.root.configure(bg="#2c3e50")

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

        # Avvio prima partita
        self.avvia_nuova_partita()

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
        self.frame_banco.pack(fill="x", padx=20, pady=10)

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
        self.frame_giocatore.pack(fill="x", padx=20, pady=10)

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
        self.frame_pulsanti.pack(pady=15)

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

        # # Pulsante Nuova Partita
        # self.btn_restart = tk.Button(
        #     self.root,
        #     text="Nuova Partita",
        #     font=("Helvetica", 12, "bold"),
        #     bg="#3498db",
        #     fg="white",
        #     command=self.avvia_nuova_partita,
        # )
        # self.btn_restart.pack(pady=10)

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

        # Ripristino bottoni
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
        # Aggiornamento Giocatore
        punti_g = self.calcola_punteggio(self.carte_giocatore)
        self.lbl_carte_giocatore.config(
            text=f"🎴 Carte: {self.formatta_mano(self.carte_giocatore)}"
        )
        self.lbl_punti_giocatore.config(text=f"🔢 Punteggio totale: {punti_g}")

        # Aggiornamento Banco
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

        if punti_g == 21 and len(self.carte_giocatore) == 2:
            if punti_b == 21 and len(self.carte_banco) == 2:
                msg = "🤝 Entrambi Blackjack! Pareggio."
            else:
                msg = "🏆 BLACKJACK! Hai vinto subito!"
        elif punti_b == 21 and len(self.carte_banco) == 2:
            msg = "📉 Il Banco ha fatto Blackjack. Hai perso."
        elif punti_g > 21:
            msg = "📉 Hai sballato! Il Banco vince."
        elif punti_b > 21:
            msg = "🏆 Il Giocatore vince! (Il Banco ha sballato)"
        elif punti_g > punti_b:
            msg = "🏆 Il Giocatore vince!"
        elif punti_b > punti_g:
            msg = "📉 Il Banco vince."
        else:
            msg = "🤝 È un pareggio!"

        messagebox.showinfo("Risultato Finale", msg)


# Esecuzione dell'applicazione
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()