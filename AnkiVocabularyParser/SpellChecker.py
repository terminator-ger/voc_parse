from python_spell import SpellChecker
from enum import StrEnum, auto()
from typing import Tuple

class SpellCheckerEngine(StrEnum):
    PythonSpell = auto()


class SpellChecker:
    def __init__(self, lang_0, lang_1):
        self.lang0 = lang_0
        self.lang1 = lang_1

    def check(self, word0, word1): 
        raise NotImplementedError()
    
    def check0(self, word0):
        raise NotImplementedError()
    
    def check1(self, word1):
        raise NotImplementedError()


class PythonSpell(SpellChecker):
    def __init__(self, lang0, lang1):
        super().__init__(lang_0=lang0, lang_1=lang1)
        self.supported_languages = {
            'en': 'english',
            'de': 'german',
            'es': 'spanish',
            'fr': 'french',
            'it': 'italian',
        }    
        for lang in [lang0, lang1]:
            if lang not in self.supported_languages:
                raise ImportError(f"PythonSpell does not support {lang} - only {self.supported_languages.values()} are supported.")
        
 
    def check(self, word0: str, word1: str) -> Tuple[str, str]: 
        self.checker0 = SpellChecker(word0, self.supported_languages[self.lang0])
        self.checker1 = SpellChecker(word1, self.supported_languages[self.lang1])
    
    def check0(self, word0: str) -> str:
        self.checker0 = SpellChecker(word0, self.supported_languages[self.lang0])
    
    def check1(self, word1: str) -> str:
        self.checker1 = SpellChecker(word1, self.supported_languages[self.lang1])
 

def getSpellChecker(args) -> SpellChecker:
    if args.spellcheck_engine == SpellCheckerEngine.PythonSpell:
        return PythonSpell(args.lang0, args.lang1)

    raise ModuleNotFoundError(f"Could not find Spellchecker {args.spellcheck_engine}")
