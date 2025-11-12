import os
class AnkiExporter:
    def __init__(self, title="", lang0="it", lang1="de"):
        self.vocabularies = []
        self.title = title
        self.lang0 = lang0
        self.lang1 = lang1
    
    def add(self, results):
        [self.vocabularies.append(x) for x in results]
    
    def save(self, filename):
        ofile0 = os.path.join("output", f"{self.title}_{self.lang0}_{self.lang1}_{filename}.txt")
        ofile1 = os.path.join("output", f"{self.title}_{self.lang1}_{self.lang0}_{filename}.txt")
        with open(ofile0, 'w+', encoding="utf-8") as fout:
            fout.write("#html:true\n")
            fout.write(f"#deck:{self.title}::{self.lang0} -> {self.lang1}::{filename}\n")
            for line in self.vocabularies:
                fout.write(f"{line[0]};{line[1]}\n")
                
        with open(ofile1, 'w+', encoding="utf-8") as fout:
            fout.write("#html:true\n")
            fout.write(f"#deck:{self.title}::{self.lang1} -> {self.lang0}::{filename}\n")
            for line in self.vocabularies:
                fout.write(f"{line[1]};{line[0]}\n")
 
        self.vocabularies = []