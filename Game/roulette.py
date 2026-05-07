import tkinter as tk
import math
import random
from tkinter import messagebox #messaggi popup (es. Vincite)

#Classe della roulette
class Roulette:
    #il "costruttore" della classe, eseguito appena il gioco nasce
    def __init__(self, parent, budget_attuale, callback_chiusura):
        self.window = tk.Toplevel(parent)
        self.window.title("3M CASINO - The Big Roulette")

        #Salvataggio dati dal Menu
        self.budget = budget_attuale #Soldi giocatore
        self.callback = callback_chiusura #Rida i soldi al menu dopo il gioco

        #Numeri roulette
        self.numeri = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.numeri_rossi = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        #I neri sono i rimanenti...
        self.puntate = {} #scommesse correnti
        self.angolo_pallina = 0 #animazione pallina
        self.in_corso = False #check per non giocare mentre e gia in corso


        self._setup_grafica() #il "_" per indicare che e una funzione all interno della classe

#Setup Grafico
    def _setup_grafica(self):
        self.window.configure(bg="#2c5d38")

