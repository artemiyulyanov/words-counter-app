from collections import defaultdict

class ProcessFileUtil:
    def __init__(self, normalizer, excel):
        self.normalizer = normalizer
        self.excel = excel

    def execute(self, input_path: str, output_path: str):
        stats = {}

        with open(input_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                words = line.strip().split()

                for word in words:
                    lemma = self.normalizer.normalize(word)

                    if lemma not in stats:
                        stats[lemma] = {
                            "total": 0,
                            "lines": []
                        }

                    stat = stats[lemma]
                    stat["total"] += 1

                    while len(stat["lines"]) <= i:
                        stat["lines"].append(0)

                    stat["lines"][i] += 1

        self.excel.export(stats, output_path)