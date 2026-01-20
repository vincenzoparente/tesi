from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

class PDFGenerator:
    def __init__(self, dati):
        self.dati = dati
        self.pdf = PDF()
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.add_page()
        self.larghezza_utile = self.pdf.w - 2 * self.pdf.l_margin

    def crea_pdf(self, voto_finale, nome_file):
        self.pdf.set_font("helvetica", "B", 22)
        self.pdf.set_text_color(44, 62, 80)
        self.pdf.cell(0, 20, "REPORT ANALISI QUALITÀ", ln=True, align='C')
        self.pdf.ln(5)

        if voto_finale >= 70:
            self.pdf.set_text_color(39, 174, 96)
        elif 50 <= voto_finale < 70:
            self.pdf.set_text_color(230, 126, 34)
        else :
            self.pdf.set_text_color(192, 57, 43)

        self.pdf.set_font("helvetica", "B", 16)
        self.pdf.cell(0, 15, f"PUNTEGGIO TOTALE: {voto_finale}/100", border=1, ln=True, align='C', fill=False)

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(10)

        mappa_sezioni = [
            ("srp", "1. Single Responsibility Principle (SRP)"),
            ("ocp", "2. Open/Closed Principle (OCP)"),
            ("lsp", "3. Liskov Substitution Principle (LSP)"),
            ("isp", "4. Interface Segregation Principle (ISP)"),
            ("dip", "5. Dependency Inversion Principle (DIP)"),
            ("dead_code", "6. Analisi codice morto"),
            ("complexity", "7. Complessità ciclomatica")
        ]

        for chiave, titolo in mappa_sezioni:
            self.aggiungi_sezione(titolo, self.dati.get(chiave, []))

        self.pdf.output(nome_file)

    def aggiungi_sezione(self, titolo, contenuto):
        contenuto_filtrato = [riga for riga in contenuto if "[0]" not in riga]

        self.pdf.set_font("helvetica", "B", 12)
        self.pdf.set_fill_color(52, 73, 94)  # blu
        self.pdf.set_text_color(255, 255, 255)  # bianco
        self.pdf.cell(0, 8, f"  {titolo}", ln=True, fill=True)

        self.pdf.ln(2)
        self.pdf.set_font("helvetica", "", 10)

        if not contenuto_filtrato or (len(contenuto_filtrato) == 1 and "Nessuna" in contenuto_filtrato[0]):
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.cell(0, 7, "Nessuna criticità rilevata per questa sezione.", ln=True)
        else:
            for riga in contenuto_filtrato:
                parole_allerta = ["ATTENZIONE", "VIOLAZIONE", "CRITICA", "POSSIBILE"]
                if any(allerta in riga.upper() for allerta in parole_allerta):
                    self.pdf.set_text_color(192, 57, 43)  # rosso
                else:
                    self.pdf.set_text_color(0, 0, 0)

                safe_text = str(riga).encode('latin-1', 'replace').decode('latin-1')
                self.pdf.set_x(15)
                self.pdf.multi_cell(self.larghezza_utile - 5, 6, f"- {safe_text}", border=0)

        self.pdf.ln(5)
        self.pdf.set_text_color(0, 0, 0)