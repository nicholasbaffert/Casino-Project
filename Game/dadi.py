import random
import time

def animazione_lancio():
    print("\n🎲 Il croupier lancia i dadi...")
    for _ in range(3):
        print("...")
        time.sleep(0.3)

def lancia_dadi():
    animazione_lancio()
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    totale = d1 + d2
    print(f"👉 Risultato: {d1} + {d2} = {totale}")
    return totale

def gioco():
    print("=== 🎰 CRAPS REALISTICO ===")
    print("Regole: vinci subito con 7 o 11, perdi con 2, 3, 12.\n")

    soldi = 100

    while True:
        print(f"\n💰 Soldi attuali: €{soldi}")
        
        if soldi <= 0:
            print("s Hai finito i soldi!")
            break

        scelta = input("Vuoi puntare e lanciare? (s/n): ").lower()

        if scelta == "n":
            print(" Hai lasciato il tavolo.")
            break

        if scelta != "s":
            print(" Scrivi 's' o 'n'")
            continue

        puntata = 10
        soldi -= puntata
        print(f"🎲 Hai puntato €{puntata}")

        risultato = lancia_dadi()

     
        if risultato in (7, 11):
            vincita = puntata * 2
            soldi += vincita
            print(f" HAI VINTO! +€{vincita}")

        elif risultato in (2, 3, 12):
            print("💀 Hai perso la puntata!")

        else:
            punto = risultato
            print(f" Punto: {punto}")

            while True:
                input("Premi INVIO per rilanciare...")
                r = lancia_dadi()

                if r == punto:
                    vincita = puntata * 2
                    soldi += vincita
                    print(f" HAI RIFATTO IL PUNTO! +€{vincita}")
                    break

                elif r == 7:
                    print("💀 7 out! Hai perso!")
                    break

                else:
                    print("🔁 Si continua...")

    print("\n🏁 Fine partita")
    print(f"💰 Soldi finali: €{soldi}")

if __name__ == "__main__":
    gioco()