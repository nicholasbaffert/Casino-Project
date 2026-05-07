import tkinter as tk
import random

class CrapsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Craps Realistico")
        self.root.geometry("500x650")
        self.root.configure(bg="#2c3e50")

        # Variabili di gioco
        self.soldi = 100
        self.puntata = 10
        self.punto = None

        self.crea_interfaccia()

    def crea_interfaccia(self):
        # Palette Colori
        bg_main = "#2c3e50"
        bg_area = "#34495e"
        oro = "#f1c40f"

        # Titolo
        tk.Label(self.root, text="🎰 CRAPS 🎰", font=("Helvetica", 30, "bold"), 
                 bg=bg_main, fg=oro).pack(pady=20)

        # Dashboard Soldi
        self.lbl_soldi = tk.Label(self.root, text=f"💰 Budget: €{self.soldi}", 
                                  font=("Helvetica", 14, "bold"), bg=bg_main, fg="white")
        self.lbl_soldi.pack(pady=5)

        # Area di Gioco (Dadi e Risultati)
        self.frame_gioco = tk.Frame(self.root, bg=bg_area, padx=20, pady=20)
        self.frame_gioco.pack(fill="x", padx=40, pady=10)

        self.lbl_stato = tk.Label(self.frame_gioco, text="Benvenuto al tavolo!", 
                                  font=("Helvetica", 11, "italic"), bg=bg_area, fg="#bdc3c7")
        self.lbl_stato.pack()

        self.lbl_dadi = tk.Label(self.frame_gioco, text="🎲🎲", 
                                 font=("Helvetica", 40), bg=bg_area, fg="white")
        self.lbl_dadi.pack(pady=15)

        self.lbl_punto_info = tk.Label(self.frame_gioco, text="", 
                                       font=("Helvetica", 12, "bold"), bg=bg_area, fg=oro)
        self.lbl_punto_info.pack()

        # Area Messaggi Log
        self.lbl_log = tk.Label(self.root, text="Punta €10 per iniziare", 
                                font=("Helvetica", 12), bg=bg_main, fg="#ecf0f1")
        self.lbl_log.pack(pady=20)

        # Bottoni
        self.btn_lancia = tk.Button(self.root, text="LANCIA DADI", font=("Helvetica", 14, "bold"),
                                   bg="#2ecc71", fg="white", bd=0, width=15, height=2,
                                   cursor="hand2", command=self.gioca_turno)
        self.btn_lancia.pack(pady=10)

        self.btn_reset = tk.Button(self.root, text="Nuova Partita", font=("Helvetica", 10, "underline"),
                                   bg=bg_main, fg="#3498db", bd=0, cursor="hand2", 
                                   command=self.reset_partita)
        self.btn_reset.pack(pady=20)

    def gioca_turno(self):
        if self.soldi < self.puntata and self.punto is None:
            self.lbl_log.config(text="💀 Soldi finiti!", fg="#e74c3c")
            self.btn_lancia.config(state="disabled")
            return

        # Lancio dadi
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        risultato = d1 + d2
        self.lbl_dadi.config(text=f"{d1}  {d2}")
        
        # Primo lancio (Nessun punto stabilito)
        if self.punto is None:
            self.soldi -= self.puntata
            self.lbl_soldi.config(text=f"💰 Budget: €{self.soldi}")
            
            if risultato in (7, 11):
                vincita = self.puntata * 2
                self.soldi += vincita
                self.lbl_log.config(text=f"🔥 HAI VINTO SUBITO! +€{vincita}", fg="#2ecc71")
            elif risultato in (2, 3, 12):
                self.lbl_log.config(text=f"💀 CRAPS! Hai perso €{self.puntata}", fg="#e74c3c")
            else:
                self.punto = risultato
                self.lbl_punto_info.config(text=f"PUNTO DA RIFARE: {self.punto}")
                self.lbl_log.config(text="🔁 Punto stabilito! Rilancia...", fg="white")
                self.btn_lancia.config(text="RILANCIA", bg="#f39c12")
        
        # Lanci successivi (Caccia al punto)
        else:
            if risultato == self.punto:
                vincita = self.puntata * 2
                self.soldi += vincita
                self.lbl_log.config(text=f"✅ PUNTO FATTO! +€{vincita}", fg="#2ecc71")
                self.reset_turno()
            elif risultato == 7:
                self.lbl_log.config(text="💀 7-OUT! Hai perso tutto.", fg="#e74c3c")
                self.reset_turno()
            else:
                self.lbl_log.config(text="🔁 Continua a lanciare...", fg="white")

        self.lbl_soldi.config(text=f"💰 Budget: €{self.soldi}")

    def reset_turno(self):
        self.punto = None
        self.lbl_punto_info.config(text="")
        self.btn_lancia.config(text="LANCIA DADI", bg="#2ecc71")

    def reset_partita(self):
        self.soldi = 100
        self.lbl_soldi.config(text=f"💰 Budget: €{self.soldi}")
        self.lbl_log.config(text="Nuova partita iniziata!", fg="white")
        self.btn_lancia.config(state="normal")
        self.reset_turno()

if __name__ == "__main__":
    root = tk.Tk()
    app = CrapsApp(root)
    root.mainloop()
    