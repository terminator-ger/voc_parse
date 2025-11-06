import os
class AnkiExporter:
    def __init__(self, title=""):
        self.vocabularies = []
        self.title = title
    
    def add(self, results):
        [self.vocabularies.append(x) for x in results]
    
    def save(self, filename):
        ofile0 = os.path.join("output", f"{self.title}_{filename}.txt")
 
        with open(ofile0, 'w+', encoding="utf-8") as fout:
            fout.write("#html:true\n")
            fout.write(f"#deck:{self.title}::{filename}\n")
            for line in self.vocabularies:
                fout.write(f"{line[0]};{line[1]}\n")
 
        self.vocabularies = []