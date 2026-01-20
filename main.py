import os
from analizza import AnalizzatoreProgetto
from pdf import PDFGenerator


def avvia_framework_tesi(test):
    if not os.path.exists(test):
        print(f"Errore: La cartella '{test}' non esiste.")
        return

#fase stampa
    print(f"\nAvvio analisi automatica: {test}")
    print("##########################\n")

    checker = AnalizzatoreProgetto(test)
    dati_analisi = checker.genera_report_finale()
    voto = checker.calcola_punteggio(dati_analisi)

    print(f"Valutazione qualità software: {voto}/100\n")

    reporter = PDFGenerator(dati_analisi)
    reporter.crea_pdf(voto, "Report_analisi_qualita.pdf")
    print("##########################\n")

    print("PDF generato correttamente.")
#fine fase stampa

if __name__ == "__main__":
    avvia_framework_tesi("medio")
