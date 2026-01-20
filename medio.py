class GestoreOrdini:

    def calcola_prezzo(self, tipo_prodotto, prezzo_base):
        if tipo_prodotto == "elettronica":
            return prezzo_base * 1.2
        elif tipo_prodotto == "abbigliamento":
            return prezzo_base * 1.1
        elif tipo_prodotto == "cibo":
            return prezzo_base * 1.05
        elif tipo_prodotto == "libri":
            return prezzo_base * 1.02
        elif tipo_prodotto == "giocattoli":
            return prezzo_base * 1.15
        elif tipo_prodotto == "sport":
            return prezzo_base * 1.12
        return prezzo_base

    def salva_ordine(self, ordine):
        print(f"Ordine {ordine} salvato.")

def funzione_inutile():
    a = 10
    b = 20
    return a + b

def funzione_inutile2():
    a = 10
    b = 50
    return a + b
def funzione_inutile3():
    a = 10
    b = 50
    return a + b

def funzione_inutile4():
    a = 10
    b = 50
    return a + b



if __name__ == "__main__":
    gestore = GestoreOrdini()
    print(gestore.calcola_prezzo("elettronica", 100))