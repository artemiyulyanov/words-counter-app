from openpyxl import Workbook

class ExcelExporter:
    def export(self, stats: dict, path: str):
        wb = Workbook()
        ws = wb.active

        ws.append(["Словоформа", "Количество во всём документе", "Количество в каждой строке"])

        for lemma, stat in stats.items():
            ws.append([
                lemma,
                stat["total"],
                ",".join(map(str, stat["lines"]))
            ])

        wb.save(path)