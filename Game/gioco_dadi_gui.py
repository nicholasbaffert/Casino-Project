import tkinter as tk
import random


dati = {
    "soldi": 100,
    "punto": None,
    "puntata": 10
}

def tira_dadi():
    return random.randint(1, 6) + random.randint(1, 6)

def primo_lancio():
    dati["soldi"] -= dati["puntata"]
    risultato = tira_dadi()
    
    testo = f"Lancio: {risultato}\n"
    
    if risultato in (7, 11):
        dati["soldi"] += dati["puntata"] * 2
        label_messaggio.config(text=f"{testo}🎉 VINTO!", fg="green")
    elif risultato in (2, 3, 12):
        label_messaggio.config(text=f"{testo}💀 PERSO!", fg="red")
    else:
        dati["punto"] = risultato
        label_messaggio.config(text=f"{testo}📌 Punto: {dati['punto']}. Rilancia!")
        btn_start.config(state="disabled")
        btn_retry.config(state="normal")
    
    aggiorna_interfaccia()

def rilancio():
    risultato = tira_dadi()
    testo = f"Rilancio: {risultato}\n"
    
    if risultato == dati["punto"]:
        dati["soldi"] += dati["puntata"] * 2
        label_messaggio.config(text=f"{testo}🎉 PUNTO FATTO!", fg="green")
        reset_gioco()
    elif risultato == 7:
        label_messaggio.config(text=f"{testo}💀 7 OUT!", fg="red")
        reset_gioco()
    else:
        label_messaggio.config(text=f"{testo}🔁 Continua...", fg="black")
    
    aggiorna_interfaccia()

def reset_gioco():
    dati["punto"] = None
    btn_start.config(state="normal")
    btn_retry.config(state="disabled")

def aggiorna_ui():
    label_soldi.config(text=f"Soldi: €{dati['soldi']}")

root.label_soldi = tk.Label(root, text =f"soldi:")