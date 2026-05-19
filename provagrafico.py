# ==============================================================================
# 1. IMPORTAZIONE LIBRERIE E CONFIGURAZIONI INIZIALI
# ==============================================================================
import tkinter as tk                 # Libreria per finestre, bottoni e grafica
from tkinter import messagebox       # Finestrelle di avviso pop-up
import json                          # Gestisce il salvataggio dei dati in formato JSON
import os                            # Controlla la presenza di file sul computer
import random                        # Genera risultati casuali per i giochi
# import matplotlib.pyplot as plt      # Disegna e mostra i grafici a schermo

# Importa il gioco della Roulette dalla cartella Game (file roulette.py)
from Game.roulette import Roulette

from Game.blackjack import BlackjackApp as Blackjack

DB_FILE = "utenti.json"              # Nome del file che fa da database per i soldi


# ==============================================================================
# 2. FUNZIONI DI GESTIONE DEL DATABASE (LETTURA E SCRITTURA JSON)
# ==============================================================================
def carica_dati():
    """ Carica le informazioni degli utenti dal file JSON """
    if not os.path.exists(DB_FILE):  
        with open(DB_FILE, "w") as f:
            json.dump({}, f)         
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)      
    except json.JSONDecodeError:     
        with open(DB_FILE, "w") as f:
            json.dump({}, f)         
        return {}

def salva_dati(dati):
    """ Salva le informazioni aggiornate nel file JSON """
    with open(DB_FILE, "w") as f:
        json.dump(dati, f, indent=4) 


# ==============================================================================
# 3. APPLICAZIONE PRINCIPALE (STRUTTURA E FINESTRA GRAFICA)
# ==============================================================================
class CasinoApp:
    def __init__(self, root):
        """ Configurazione iniziale della finestra con Tema Dark """
        self.root = root                         
        self.root.title("Casino Gold Premium")           
        self.root.geometry("400x530")            # Altezza aumentata per un layout più arioso
        self.root.config(bg="#1a1a1a")           # Sfondo scuro dell'applicazione di base
        
        self.utente_attuale = None               
        self.saldo_attuale = 0                   
        
        # Pannello invisibile contenitore impostato con sfondo scuro
        self.container = tk.Frame(self.root, bg="#1a1a1a")
        self.container.pack(expand=True, fill="both")
        
        self.mostra_schermata_login()            

    def pulisci_schermata(self):
        """ Cancella tutti i bottoni e testi per fare spazio alla schermata successiva """
        for widget in self.container.winfo_children():
            widget.destroy()                     


# ==============================================================================
# 4. SCHERMATA DI LOGIN / REGISTRAZIONE (STILE PREMIUM)
# ==============================================================================
    def mostra_schermata_login(self):
        """ Disegna la pagina iniziale con l'inserimento del nome utente """
        self.pulisci_schermata()                 
        
        # Spaziatore invisibile in alto per centrare i contenuti verticalmente
        tk.Frame(self.container, bg="#1a1a1a", height=30).pack()
        
        # TITOLO PRINCIPALE: Scrittura dorata elegante
        titolo = tk.Label(
            self.container, 
            text="CASINÒ", 
            font=("Helvetica", 24, "bold"), 
            fg="#ffd700",  
            bg="#1a1a1a"
        )
        titolo.pack(pady=(10, 5))
        
        # SOTTOTITOLO: Stile club d'élite
        sottotitolo = tk.Label(
            self.container, 
            text="« Benvenuto nel Club Della 3M »", 
            font=("Georgia", 10, "italic"), 
            fg="#b3b3b3",  
            bg="#1a1a1a"
        )
        sottotitolo.pack(pady=(0, 35))
        
        # SCHEDA CENTRALE: Box grigio scuro con sottile bordo dorato
        card_form = tk.Frame(self.container, bg="#262626", highlightbackground="#ffd700", highlightthickness=1, bd=0)
        card_form.pack(pady=10, padx=40, fill="x")
        
        lbl_user = tk.Label(
            card_form, 
            text="INSERISCI IL TUO USERNAME", 
            font=("Helvetica", 9, "bold"), 
            fg="#ffffff", 
            bg="#262626"
        )
        lbl_user.pack(pady=(25, 10))
        
        # CASELLA DI INPUT MODERNA: Alta, centrata e scura
        self.entry_user = tk.Entry(
            card_form, 
            font=("Helvetica", 12), 
            bg="#333333", 
            fg="#ffffff", 
            insertbackground="#ffffff", 
            bd=0, 
            justify="center"
        )
        self.entry_user.pack(pady=(0, 25), ipady=6, padx=30, fill="x")
        
        # BOTTONE DI ACCESSO PREMIUM: Dorato piatto con effetto manina al passaggio
        btn_accedi = tk.Button(
            self.container, 
            text="ENTRA NEL GIOCO", 
            command=self.gestisci_accesso, 
            bg="#ffd700", 
            fg="#000000", 
            font=("Helvetica", 11, "bold"), 
            bd=0, 
            cursor="hand2", 
            activebackground="#e6c200", 
            activeforeground="#000000"
        )
        btn_accedi.pack(pady=25, ipady=8, padx=40, fill="x")

    def gestisci_accesso(self):
        """ Logica di login o creazione account """
        username = self.entry_user.get().strip() 
        
        if not username:                         
            messagebox.showwarning("Errore", "Inserisci un nome utente!")
            return                               
        
        dati = carica_dati()                     
        
        if username in dati:                     
            self.utente_attuale = username
            self.saldo_attuale = dati[username]["saldo"] 
            messagebox.showinfo("Login", f"Bentornato {username}!")
            
        else:                                    
            self.utente_attuale = username
            self.saldo_attuale = 1000            
            
            dati[username] = {
                "saldo": self.saldo_attuale,
                "cronologia": [
                    {"gioco": "Inizio", "variazione": 0, "saldo_risultante": 1000}
                ]
            }
            salva_dati(dati)                     
            messagebox.showinfo("Benvenuto", f"Nuovo utente registrato! Saldo: {self.saldo_attuale}€")
        
        self.mostra_menu_principale()            


# ==============================================================================
# 5. SCHERMATA MENU PRINCIPALE (STILE LUXURY)
# ==============================================================================
    def mostra_menu_principale(self):
        """ Disegna il menu principale con bottoni modernizzati e ordinati """
        self.pulisci_schermata()                 
        
        # BARRA TOP INFO: Pannello dedicato per utente e portafoglio
        info_panel = tk.Frame(self.container, bg="#262626", highlightbackground="#333333", highlightthickness=1)
        info_panel.pack(pady=(15, 20), padx=20, fill="x")
        
        self.label_info = tk.Label(
            info_panel, 
            text=f"👤 {self.utente_attuale}     |     💰 {self.saldo_attuale}€", 
            font=("Helvetica", 11, "bold"), 
            fg="#ffd700",  # Testo oro per il bilancio
            bg="#262626"
        )
        self.label_info.pack(pady=12)

        tk.Label(self.container, text="SELEZIONA UNA SALA DA GIOCO", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1a1a1a").pack(pady=(0, 15))

        # Stile standard riutilizzabile per i bottoni dei giochi (Scuro con testo bianco)
        stile_bottone_gioco = {
            "font": ("Helvetica", 11, "bold"),
            "bg": "#2d2d2d",
            "fg": "#ffffff",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#404040",
            "activeforeground": "#ffffff"
        }

        # Bottoni dei giochi posizionati all'interno della finestra
        btn_roulette = tk.Button(self.container, text="Roulette 🎡", command=self.avvia_roulette_game, **stile_bottone_gioco)
        btn_roulette.pack(pady=6, ipady=7, padx=40, fill="x")
        
        btn_dadi = tk.Button(self.container, text="Lancio dei Dadi 🎲  (-10€)", command=self.gioca_dadi, **stile_bottone_gioco)
        btn_dadi.pack(pady=6, ipady=7, padx=40, fill="x")
        
        btn_blackjack = tk.Button(self.container, text="Blackjack 🃏", command=self.avvia_blackjack_game, **stile_bottone_gioco)
        btn_blackjack.pack(pady=6, ipady=7, padx=40, fill="x")
        
        # BOTTONE STATISTICHE: Evidenziato in Grigio/Azzurro metallico
        btn_stats = tk.Button(
            self.container, 
            text="Visualizza Statistiche 📊", 
            command=self.mostra_grafico_personale,
            font=("Helvetica", 11, "bold"),
            bg="#3a4f5c",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            activebackground="#4a6373",
            activeforeground="#ffffff"
        )
        btn_stats.pack(pady=(20, 5), ipady=7, padx=40, fill="x")
        
        # BOTTONE ESCI: Rosso scuro elegante piatto
        btn_esci = tk.Button(
            self.container, 
            text="Esci dal Club", 
            command=self.esci,
            font=("Helvetica", 10, "bold"),
            bg="#8b0000",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            activebackground="#a30000",
            activeforeground="#ffffff"
        )
        btn_esci.pack(pady=15, ipady=5, padx=60, fill="x")


# ==============================================================================
# 6. LOGICA DEI GIOCHI E AGGIORNAMENTO DATI
# ==============================================================================
    def avvia_roulette_game(self):
        """ Nasconde il menu e apre la finestra esterna della Roulette """
        self.root.withdraw()                     
        Roulette(self.root, self.saldo_attuale, self.aggiorna_saldo_da_gioco)

    def avvia_blackjack_game(self):
        """ Avviso temporaneo in attesa di blackjack """
        self.root.withdraw()

        Blackjack(self.root, self.saldo_attuale, self.aggiorna_saldo_da_gioco)

    def aggiorna_saldo_da_gioco(self, nuovo_saldo):
        """ Funzione automatica richiamata dalla Roulette quando viene chiusa """
        variazione = nuovo_saldo - self.saldo_attuale 
        self.saldo_attuale = nuovo_saldo         
        
        self.root.deiconify()                    
        self.label_info.config(text=f"👤 {self.utente_attuale}     |     💰 {self.saldo_attuale}€") 
        
        dati = carica_dati()                     
        dati[self.utente_attuale]["saldo"] = self.saldo_attuale 
        
        dati[self.utente_attuale]["cronologia"].append({
            "gioco": "Roulette",
            "variazione": variazione,
            "saldo_risultante": self.saldo_attuale
        })
        salva_dati(dati)                         

    def gioca_dadi(self):
        """ Minigioco istantaneo dei dadi incorporato """
        costo = 10                               
        
        if self.saldo_attuale >= costo:          
            self.saldo_attuale -= costo          
            
            vinto = random.choice([True, False]) 
            
            if vinto:
                premio = 25                      
                self.saldo_attuale += premio     
                variazione = premio - costo      
                messagebox.showinfo("Dadi", "Complimenti! Hai vinto ai dadi!\nGuadagno netto: +15€")
            else:
                variazione = -costo              
                messagebox.showinfo("Dadi", "Ritenta, la fortuna non era dalla tua!\nPerdita: -10€")
            
            self.label_info.config(text=f"👤 {self.utente_attuale}     |     💰 {self.saldo_attuale}€")
            
            dati = carica_dati()                 
            dati[self.utente_attuale]["saldo"] = self.saldo_attuale 
            
            dati[self.utente_attuale]["cronologia"].append({
                "gioco": "Dadi",
                "variazione": variazione,
                "saldo_risultante": self.saldo_attuale
            })
            salva_dati(dati)                     
        else:
            messagebox.showerror("Errore", "Saldo insufficiente per giocare a questa slot!")


# ==============================================================================
# 7. GENERAZIONE DEL GRAFICO STATISTICO (TEMA SCURO ALLINEATO)
# ==============================================================================
    def mostra_grafico_personale(self):
        """ Elabora i dati e mostra un grafico coordinato con lo stile scuro dell'app """
        dati = carica_dati()                     
        cronologia = dati[self.utente_attuale].get("cronologia", []) 
        
        if len(cronologia) <= 1:                 
            messagebox.showinfo("Statistiche", "Effettua almeno una puntata ai tavoli per sbloccare i tuoi grafici!")
            return                               
        
        indici_giocate = list(range(len(cronologia)))                       
        saldi_storici = [giocata["saldo_risultante"] for giocata in cronologia] 
        nomi_giochi = [giocata["gioco"] for giocata in cronologia]          

        # Configurazione dello stile scuro anche per la finestra del grafico Matplotlib
        plt.rcParams['text.color'] = '#ffffff'
        plt.rcParams['axes.labelcolor'] = '#b3b3b3'
        plt.rcParams['xtick.color'] = '#b3b3b3'
        plt.rcParams['ytick.color'] = '#b3b3b3'
        
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor('#1a1a1a') # Sfondo esterno nero fumo
        ax.set_facecolor('#262626')       # Sfondo interno della griglia grigio scuro
        
        # Disegna la linea dell'andamento (colore Oro lucido con marker bianchi)
        ax.plot(indici_giocate, saldi_storici, marker='o', color='#ffd700', markerfacecolor='#ffffff', markeredgecolor='#ffd700', linewidth=2, label="Saldo")
        
        # Testi ed etichette del grafico coordinati
        ax.set_title(f"Andamento Finanziario di {self.utente_attuale}", fontsize=13, fontweight='bold', pad=15, color='#ffd700')
        ax.set_xlabel("Puntate / Eventi effettuati", fontsize=10)
        ax.set_ylabel("Capitale (€)", fontsize=10)
        ax.grid(True, linestyle='--', color='#404040', alpha=0.6) # Griglia grigio scura sfumata
        
        # Scritta del nome del gioco sopra ogni rispettivo punto
        for idx, gioco in enumerate(nomi_giochi):
            ax.annotate(
                gioco, 
                (indici_giocate[idx], saldi_storici[idx]), 
                textcoords="offset points", 
                xytext=(0, 9),                   
                ha='center',                     
                fontsize=8,                      
                fontweight='semibold',
                color='#ffffff'
            )
            
        plt.tight_layout()                       
        plt.show()                               


# ==============================================================================
# 8. CHIUSURA E AVVIO DEL PROGRAMMA
# ==============================================================================
    def esci(self):
        """ Chiude definitivamente l'applicazione grafica """
        self.root.destroy()                      


if __name__ == "__main__":
    root = tk.Tk()                               
    app = CasinoApp(root)                        
    root.mainloop()