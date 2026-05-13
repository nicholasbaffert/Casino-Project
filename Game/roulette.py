import tkinter as tk
import random
from tkinter import messagebox

class Roulette:
    def __init__(self, parent, budget_attuale, callback_chiusura):
        # Finestra secondaria (Toplevel)
        self.window = tk.Toplevel(parent)
        self.window.title("3M CASINO - The Big Roulette")
        self.window.geometry("900x600")
        self.window.configure(bg="#2c5d38")

        # Gestione della chiusura della finestra (sia da tasto che da pulsante X)
        self.window.protocol("WM_DELETE_WINDOW", self.torna_al_menu)

        # Dati del giocatore e callback per il Menu principale
        self.budget = budget_attuale
        self.callback = callback_chiusura

        # Liste e configurazioni della roulette reale
        self.numeri_rossi = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        
        # Array completo e ordinato per il tabellone grafico (Fila 3, Fila 2, Fila 1)
        self.ordine_tabella = [
            0,
            3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36,
            2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35,
            1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
        ]

        # Variabili di scommessa dell'utente
        self.tipo_scommessa = tk.StringVar(value="numero")  # "numero", "rosso", "nero"
        self.valore_scommessa = tk.StringVar(value="0")      # Numero scelto (se tipo è "numero")
        self.importo_fiche = tk.IntVar(value=10)             # Soldi puntati (es. 10€)

        # Variabili di stato per l'animazione
        self.in_corso = False
        self.indice_corrente = 0
        self.passi_rimanenti = 0
        self.velocita_corrente = 50
        self.rettangoli_grafici = {}

        # Generazione dell'interfaccia grafica
        self._setup_grafica()

    def _setup_grafica(self):
        # Titolo
        lbl_titolo = tk.Label(self.window, text="🎲 THE BIG ROULETTE 🎲", font=("Helvetica", 20, "bold"), fg="white", bg="#2c5d38")
        lbl_titolo.pack(pady=10)

        # Canvas per il tabellone dei numeri
        self.canvas = tk.Canvas(self.window, width=750, height=220, bg="#2c5d38", highlightthickness=0)
        self.canvas.pack(pady=5)
        self._disegna_tabellone()

        # -------------------------------------------------------------
        # PANNELLO DELLE SCOMMESSE (Interfaccia di Betting)
        # -------------------------------------------------------------
        frame_betting = tk.LabelFrame(self.window, text=" PANNELLO PUNTATE ", font=("Helvetica", 11, "bold"), fg="white", bg="#1b4d22", bd=2, padx=15, pady=10)
        frame_betting.pack(pady=15, fill="x", padx=40)

        # 1. Selezione Importo della Fiche
        tk.Label(frame_betting, text="Quanto punti (€):", font=("Helvetica", 10, "bold"), fg="yellow", bg="#1b4d22").grid(row=0, column=0, padx=10, sticky="w")
        entry_importo = tk.Entry(frame_betting, textvariable=self.importo_fiche, width=8, font=("Helvetica", 11))
        entry_importo.grid(row=0, column=1, padx=5, sticky="w")

        # 2. Scelta del Tipo di Puntata (Radio Buttons)
        tk.Label(frame_betting, text="Tipo Scommessa:", font=("Helvetica", 10, "bold"), fg="yellow", bg="#1b4d22").grid(row=0, column=2, padx=20, sticky="w")
        
        tk.Radiobutton(frame_betting, text="Numero Singolo", variable=self.tipo_scommessa, value="numero", bg="#1b4d22", fg="white", selectcolor="#2c5d38", font=("Helvetica", 10)).grid(row=0, column=3, padx=5)
        tk.Radiobutton(frame_betting, text="Solo ROSSO", variable=self.tipo_scommessa, value="rosso", bg="#1b4d22", fg="white", selectcolor="#2c5d38", font=("Helvetica", 10)).grid(row=0, column=4, padx=5)
        tk.Radiobutton(frame_betting, text="Solo NERO", variable=self.tipo_scommessa, value="nero", bg="#1b4d22", fg="white", selectcolor="#2c5d38", font=("Helvetica", 10)).grid(row=0, column=5, padx=5)

        # 3. Campo per inserire il numero singolo (attivo solo se si sceglie Numero Singolo)
        tk.Label(frame_betting, text="Quale Numero (0-36):", font=("Helvetica", 10, "bold"), fg="white", bg="#1b4d22").grid(row=1, column=2, padx=20, pady=10, sticky="w")
        entry_num = tk.Entry(frame_betting, textvariable=self.valore_scommessa, width=5, font=("Helvetica", 11))
        entry_num.grid(row=1, column=3, sticky="w")

        # -------------------------------------------------------------
        # AREA DI CONTROLLO INFERIORE (Budget, Avvio e Uscita)
        # -------------------------------------------------------------
        frame_azioni = tk.Frame(self.window, bg="#2c5d38")
        frame_azioni.pack(pady=10)

        # Indicatore Budget
        self.lbl_budget = tk.Label(frame_azioni, text=f"Il tuo Saldo: {self.budget}€", font=("Helvetica", 16, "bold"), fg="gold", bg="#2c5d38")
        self.lbl_budget.pack(side=tk.LEFT, padx=20)

        # Pulsante Gira Ruota
        self.btn_gira = tk.Button(frame_azioni, text="PUNTA E GIRA", font=("Helvetica", 12, "bold"), bg="gold", fg="black", activebackground="#ffd700", padx=15, pady=8, command=self.avvia_giro)
        self.btn_gira.pack(side=tk.LEFT, padx=20)

        # Pulsante Esci e Salva
        btn_esci = tk.Button(frame_azioni, text="TORNA AL MENU", font=("Helvetica", 11, "bold"), bg="#b31a1a", fg="white", activebackground="#d93636", padx=10, pady=6, command=self.torna_al_menu)
        btn_esci.pack(side=tk.LEFT, padx=20)

    def _disegna_tabellone(self):
        self.canvas.delete("all")
        self.rettangoli_grafici.clear()

        # ZERO
        id_0 = self.canvas.create_rectangle(10, 20, 60, 200, fill="#1b4d22", outline="white", width=2)
        self.canvas.create_text(35, 110, text="0", fill="white", font=("Helvetica", 18, "bold"))
        self.rettangoli_grafici[0] = id_0

        # Tabella 1-36
        larghezza_cella = 55
        altezza_cella = 60
        start_x = 65
        start_y = 20

        for riga in range(3):
            for colonna in range(12):
                indice_lista = 1 + (riga * 12) + colonna
                numero = self.ordine_tabella[indice_lista]
                colore_sfondo = "#b31a1a" if numero in self.numeri_rossi else "#1a1a1a"

                x1 = start_x + (colonna * larghezza_cella)
                y1 = start_y + (riga * altezza_cella)
                x2 = x1 + larghezza_cella
                y2 = y1 + altezza_cella

                id_rettangolo = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colore_sfondo, outline="white", width=1.5)
                self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text=str(numero), fill="white", font=("Helvetica", 14, "bold"))
                self.rettangoli_grafici[numero] = id_rettangolo

    def avvia_giro(self):
        if self.in_corso:
            return

        # --- VALIDAZIONE DELLE SCOMMESSE ---
        try:
            puntata = self.importo_fiche.get()
        except tk.TclError:
            messagebox.showerror("Errore", "Inserisci un valore numerico valido per la puntata!")
            return

        if puntata <= 0:
            messagebox.showerror("Errore", "La puntata deve essere maggiore di 0€!")
            return

        if puntata > self.budget:
            messagebox.showerror("Errore", "Non hai abbastanza soldi per questa puntata!")
            return

        # Controllo validità numero inserito
        if self.tipo_scommessa.get() == "numero":
            try:
                num_scelto = int(self.valore_scommessa.get())
                if num_scelto < 0 or num_scelto > 36:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Errore", "Inserisci un numero valido tra 0 e 36!")
                return

        # Scaliamo la puntata dal conto corrente prima del giro
        self.budget -= puntata
        self.lbl_budget.config(text=f"Il tuo Saldo: {self.budget}€")

        # Avvio animazione
        self.in_corso = True
        self.btn_gira.config(state=tk.DISABLED)

        self.indice_corrente = random.randint(0, len(self.ordine_tabella) - 1)
        self.passi_rimanenti = 45
        self.velocita_corrente = 40
        self._aggiorna_animazione()

    def _aggiorna_animazione(self):
        self._disegna_tabellone()

        numero_evidenziato = self.ordine_tabella[self.indice_corrente]
        id_rettangolo = self.rettangoli_grafici[numero_evidenziato]
        self.canvas.itemconfig(id_rettangolo, fill="gold")

        if self.passi_rimanenti > 0:
            self.indice_corrente = (self.indice_corrente + 1) % len(self.ordine_tabella)
            self.passi_rimanenti -= 1
            self.velocita_corrente += 9
            self.window.after(self.velocita_corrente, self._aggiorna_animazione)
        else:
            self.in_corso = False
            self.btn_gira.config(state=tk.NORMAL)
            self._valuta_risultato(numero_evidenziato)

    def _valuta_risultato(self, numero_uscito):
        tipo = self.tipo_scommessa.get()
        puntata = self.importo_fiche.get()
        vincita = 0
        vinto = False

        is_rosso = numero_uscito in self.numeri_rossi
        is_nero = numero_uscito != 0 and not is_rosso

        if tipo == "numero":
            num_scelto = int(self.valore_scommessa.get())
            if num_scelto == numero_uscito:
                vincita = puntata * 36
                vinto = True
        elif tipo == "rosso" and is_rosso:
            vincita = puntata * 2
            vinto = True
        elif tipo == "nero" and is_nero:
            vincita = puntata * 2
            vinto = True

        if vinto:
            self.budget += vincita
            messagebox.showinfo("VINCITA! 🎉", f"🎯 È uscito il numero {numero_uscito}!\nHai vinto {vincita}€!")
        else:
            messagebox.showinfo("Sconfitta ❌", f"🎯 È uscito il numero {numero_uscito}!\nHai perso la tua puntata di {puntata}€.")

        self.lbl_budget.config(text=f"Il tuo Saldo: {self.budget}€")

    def torna_al_menu(self):
        if self.in_corso:
            messagebox.showwarning("Attenzione", "Attendi che la ruota finisca di girare!")
            return
        
        self.callback(self.budget)
        self.window.destroy()
