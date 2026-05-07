<img width="1893" height="307" alt="Screenshot 2026-05-07 130019" src="https://github.com/user-attachments/assets/a80d6121-2d05-4cab-bc30-7b08833bdb63" />

# 🎰 Documento dei Requisiti  
## Progetto: Casino Console – Mini Gambling Games

---

## 1. 📌 Titolo del progetto
Casino Console – Mini Gambling Games

---

## 2. 🎯 Obiettivo
Il progetto simula un casinò in ambiente console.

L’utente può giocare a diversi giochi d’azzardo virtuali, gestire un saldo iniziale e effettuare puntate.


## 3. 👥 Attori
- Utente / Giocatore  
- Sistema (applicazione console)

---

## 4. ⚙️ Requisiti funzionali
Il sistema deve:
- Avviare un menu principale interattivo
- Consentire la scelta tra i giochi:
  - Roulette
  - Dadi
  - Blackjack
- Gestire un saldo iniziale del giocatore
- Permettere di effettuare puntate
- Gestire decisioni di gioco (hit / stand nel blackjack)
- Generare risultati casuali tramite random
- Calcolare vincite e perdite
- Aggiornare il saldo in tempo reale
- Bloccare puntate superiori al saldo
- Mostrare l’esito di ogni partita
- Permettere ritorno al menu o uscita

---

## 5. 🧱 Requisiti non funzionali
- Interfaccia testuale semplice e leggibile
- Codice modulare in file separati
- Gestione robusta degli errori:
  - input non valido
  - valori fuori range
  - puntate errate
- Codice commentato e mantenibile
- Esecuzione stabile senza crash

---

## 6. 🎮 Logica dei giochi

### 🎡 Roulette
- Numeri da 0 a 36
- Puntate:
  - Rosso/Nero → x2
  - Pari/Dispari → x2
  - Numero secco → x36

---

### 🎲 Dadi
- 2 dadi (1–6)
- Regola:
  - Somma > 7 → vittoria
  - Somma ≤ 7 → sconfitta

---

### 🃏 Blackjack
- Obiettivo: arrivare a 21 senza superarlo
- Azioni:
  - hit → pesca carta
  - stand → fermati
- Carte:
  - numeri → valore nominale
  - figure → 10
  - asso → 1 o 11
- Esiti:
  - 21 → sconfitta
  - più vicino del banco → vittoria
  - pari → pareggio

---

## 7. 💰 Sistema di saldo
- Saldo iniziale (es. 100)
- Ogni puntata viene sottratta
- Le vincite vengono aggiunte
- Se saldo = 0 → Game Over

---

## 8. 📁 Struttura del progetto
casino_project/
│
├── main.py
├── roulette.py
├── dice.py
├── blackjack.py
├── utils.py
└── README.md

---

## 9. 🔁 Flusso del programma
Avvio programma  
↓  
Menu principale  
↓  
Scelta gioco  
↓  
Inserimento puntata  
↓  
Esecuzione gioco  
↓  
Calcolo risultato  
↓  
Aggiornamento saldo  
↓  
Mostra esito  
↓  
Ritorno al menu o uscita  

---

## 10. ⚠️ Gestione errori
- bloccare input non numerici
- impedire puntate negative
- impedire puntate superiori al saldo
- richiedere reinserimento in caso di errore

---

## 11. 🚀 Estensioni future
- Salvataggio del saldo su file
- Statistiche win/loss
- Interfaccia grafica (tkinter)
- Miglioramento estetico (colorama)
- Nuovi giochi (poker, ecc.)
- Modalità multiplayer locale

---

## 12. 📅 Cronoprogramma
- Settimana 1 → progettazione
- Settimana 2 → menu + saldo
- Settimana 3 → giochi
- Settimana 4 → test e rifinitura

---

## 13. 📦 Package utilizzati
- random → numeri casuali
- time → pause ed effetti (opzionale)
- colorama → colori in console (opzionale)
- json → salvataggio utente e saldo


## 14. Gannt/Flowchart
<img width="1893" height="307" alt="Screenshot 2026-05-07 130019" src="https://github.com/user-attachments/assets/4f749ac7-1d61-4d97-a5a0-6d9e8fdc06cf" />
<img width="1920" height="527" alt="Screenshot 2026-05-07 124722" src="https://github.com/user-attachments/assets/f1f36983-536f-48dc-8bfc-62032cdba60e" />

---

## ⚖️ Nota finale
Il progetto è puramente educativo e non utilizza denaro reale.
