import ast
import os
from radon.complexity import cc_visit
from vulture import Vulture


class AnalizzatoreProgetto:
    def __init__(self, percorso_cartella):
        self.percorso_cartella = percorso_cartella
        self.file_python = self._recupera_file_py()

    def _recupera_file_py(self):
        lista_file = []
        for radice, _, files in os.walk(self.percorso_cartella):
            for file in files:
                if file.endswith(".py"):
                    lista_file.append(os.path.join(radice, file))
        return lista_file


    def analizza_srp(self):
        report = []
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for nodo in ast.walk(tree):
                    if isinstance(nodo, ast.ClassDef):
                        metodi = [n for n in nodo.body if isinstance(n, ast.FunctionDef)]
                        count = len(metodi)
                        stato = "0"
                        if count > 20:
                            stato = "violazione"
                        elif count > 10:
                            stato = "parziale violazione"
                        report.append(
                            f"Classe {nodo.name} ({os.path.basename(file)}): {count} metodi [{stato}]"
                        )
        return report

    def analizza_ocp(self):
        report = []
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for nodo in ast.walk(tree):
                    if isinstance(nodo, ast.FunctionDef):
                        if_count = sum(isinstance(n, ast.If) for n in ast.walk(nodo))
                        stato = "0"
                        if if_count > 10:
                            stato = "violazione"
                        elif if_count > 5:
                            stato = "parziale violazione"
                        report.append(
                            f"Funzione {nodo.name} ({os.path.basename(file)}): {if_count} if [{stato}]"
                        )
        return report


    def analizza_lsp(self):
        report = []
        class_methods = {}
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for nodo in ast.walk(tree):
                    if isinstance(nodo, ast.ClassDef):
                        methods = {n.name for n in nodo.body if isinstance(n, ast.FunctionDef)}
                        class_methods[nodo.name] = (methods, nodo.bases)

        for cls, (methods, bases) in class_methods.items():
            for base in bases:
                if isinstance(base, ast.Name) and base.id in class_methods:
                    base_methods = class_methods[base.id][0]
                    overridden = methods.intersection(base_methods)
                    stato = "0"
                    if len(overridden) > 5:
                        stato = "violazione"
                    report.append(
                        f"Classe {cls}: override {len(overridden)} metodi da {base.id} [{stato}]"
                    )

        if not report:
            report.append("Nessuna violazione LSP rilevata.")
        return report


    def analizza_isp(self):
        v = Vulture()
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                v.scan(f.read(), filename=file)
        unused = v.get_unused_code()
        file_unused_methods = {}
        for item in unused:
            if item.typ == "method":
                nome_file = os.path.basename(item.filename)
                file_unused_methods.setdefault(nome_file, 0)
                file_unused_methods[nome_file] += 1
        report = []
        for file, count in file_unused_methods.items():
            stato = "0"
            if count >= 3:
                stato = "violazione"
            report.append(f"File {file}: {count} metodi inutilizzati [{stato}]")
        if not report:
            report.append("Nessuna violazione ISP rilevata.")
        return report

    def analizza_dip(self):
        report = []
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for nodo in ast.walk(tree):
                    if isinstance(nodo, ast.ClassDef):
                        deps = {n.id for n in ast.walk(nodo) if isinstance(n, ast.Name) and n.id[0].isupper()}
                        stato = "0"
                        if len(deps) > 3:
                            stato = "violazione"
                        report.append(
                            f"Classe {nodo.name} ({os.path.basename(file)}): {len(deps)} dipendenze concrete [{stato}]")
        return report


    def trova_codice_morto(self):
        v = Vulture()
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                v.scan(f.read(), filename=file)
        report = []
        for item in v.get_unused_code():
            riga = getattr(item, 'lineno', getattr(item, 'first_lineno', '?'))
            report.append(f"{item.typ} inutilizzato: {item.name} (riga {riga})")
        return report


    def analizza_complessita_progetto(self):
        report = []
        for file in self.file_python:
            with open(file, "r", encoding="utf-8") as f:
                for blocco in cc_visit(f.read()):
                    stato = "critica" if blocco.complexity > 10 else "0"
                    report.append(f"{blocco.name} ({os.path.basename(file)}): {blocco.complexity} [{stato}]")
        return report


    def calcola_punteggio(self, dati):
        score = 100

        score -= len(dati.get("dead_code", [])) * 7
        for c in dati.get("complexity", []):
            if "critica" in c:
                score -= 10

        for s in dati.get("srp", []):
            if "violazione" in s: score -= 5
        for o in dati.get("ocp", []):
            if "violazione OCP" in o: score -= 5
        for l in dati.get("lsp", []):
            if "violazione" in l: score -= 5
        for i in dati.get("isp", []):
            if "violazione" in i: score -= 5
        for d in dati.get("dip", []):
            if "violazione" in d: score -= 5
        return max(0, score)
#la sezione punteggio può essere cambiata a piacimento

    def genera_report_finale(self):
        return {
            "progetto": self.percorso_cartella,
            "srp": self.analizza_srp(),
            "ocp": self.analizza_ocp(),
            "lsp": self.analizza_lsp(),
            "isp": self.analizza_isp(),
            "dip": self.analizza_dip(),
            "dead_code": self.trova_codice_morto(),
            "complexity": self.analizza_complessita_progetto()
        }

