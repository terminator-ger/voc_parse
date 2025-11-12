import json
import easyocr
from enum import StrEnum, auto()
import importlib

class OCREngine(StrEnum):
    EasyOCR = auto()
    PaddleOCR = auto()

class OCR:
    def __init__(self):
        pass

    def read(self, file) -> str:
        pass
    
class EasyOCR(OCR):
    def __init__(self, lang0, lang1):
        super().__init__()
        self.reader = easyocr.Reader([lang0, lang1]) # this needs to run only once to load the model into memory
        self.supported_languages = {
            "abq": "Abaza",
            "ady": "Adyghe",
            "af": "Afrikaans",
            "ang": "Angika",
            "ar": "Arabic",
            "as": "Assamese",
            "ava": "Avar",
            "az": "Azerbaijani",
            "be": "Belarusian",
            "bg": "Bulgarian",
            "bh": "Bihari",
            "bho": "Bhojpuri",
            "bn": "Bengali",
            "bs": "Bosnian",
            "ch_sim": "Simplified Chinese",
            "ch_tra": "Traditional Chinese",
            "che": "Chechen",
            "cs": "Czech",
            "cy": "Welsh",
            "da": "Danish",
            "dar": "Dargwa",
            "de": "German",
            "en": "English",
            "es": "Spanish",
            "et": "Estonian",
            "fa": "Persian (Farsi)",
            "fr": "French",
            "ga": "Irish",
            "gom": "Goan Konkani",
            "hi": "Hindi",
            "hr": "Croatian",
            "hu": "Hungarian",
            "id": "Indonesian",
            "inh": "Ingush",
            "is": "Icelandic",
            "it": "Italian",
            "ja": "Japanese",
            "kbd": "Kabardian",
            "kn": "Kannada",
            "ko": "Korean",
            "ku": "Kurdish",
            "la": "Latin",
            "lbe": "Lak",
            "lez": "Lezghian",
            "lt": "Lithuanian",
            "lv": "Latvian",
            "mah": "Magahi",
            "mai": "Maithili",
            "mi": "Maori",
            "mn": "Mongolian",
            "mr": "Marathi",
            "ms": "Malay",
            "mt": "Maltese",
            "ne": "Nepali",
            "new": "Newari",
            "nl": "Dutch",
            "no": "Norwegian",
            "oc": "Occitan",
            "pi": "Pali",
            "pl": "Polish",
            "pt": "Portuguese",
            "ro": "Romanian",
            "ru": "Russian",
            "rs_cyrillic": "Serbian (cyrillic)",
            "rs_latin": "Serbian (latin)",
            "sck": "Nagpuri",
            "sk": "Slovak",
            "sl": "Slovenian",
            "sq": "Albanian",
            "sv": "Swedish",
            "sw": "Swahili",
            "ta": "Tamil",
            "tab": "Tabassaran",
            "te": "Telugu",
            "th": "Thai",
            "tjk": "Tajik",
            "tl": "Tagalog",
            "tr": "Turkish",
            "ug": "Uyghur",
            "uk": "Ukranian",
            "ur": "Urdu",
            "uz": "Uzbek",
            "vi": "Vietnamese",
        }
        for lang in [lang0, lang1]:
            if lang not in self.supported_languages:
                raise ImportError(f"EasyOCR does not support {lang} - only {self.supported_languages.values()} are supported.")
 

    def read(self, file) -> str:
        result = self.reader.readtext(file)
        output = {
            "rec_poly": [box for box, _, _ in result],
            "rec_texts": [txt for _, txt, _ in result],
        }
        
        ofile = file.removesuffix(".jpg")\
                    .removesuffix(".jpeg")\
                    .removesuffix(".png")\
                    .removesuffix(".JPG")\
                    .removesuffix(".JPEG")\
                    .removesuffix(".PNG")
        ofile += ".json"
        ofile = importlib.resources('processed.ocr').join(ofile)
        with open(ofile, "w+") as fout:
            json.dump(output, fout)
            
        return ofile

class PaddleOCRWrapper(OCR):
    def __init__(self):
        super().__init__()
        from paddleocr import PaddleOCR
        self.ocr = PaddleOCR(   
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False)

    def read(self, file) -> str:
        result = self.ocr.predict(input=file)
        
        # Visualize the results and save the JSON results
        for res in result:
            res.save_to_img("output")
            res.save_to_json("output")
        
        ofile = file.removesuffix(".jpg")\
                    .removesuffix(".jpeg")\
                    .removesuffix(".png")\
                    .removesuffix(".JPG")\
                    .removesuffix(".JPEG")\
                    .removesuffix(".PNG")\
                    .removeprefix("input/")
        return f"output/{ofile}.json"
            
def getOCR(args):
    if args.ocr_engine == OCREngine.EasyOCR:
        return EasyOCR()
    elif args.ocr_engine == OCREngine.PaddleOCR:
        return PaddleOCRWrapper()
    raise ModuleNotFoundError(f"Could not find OCR {args.ocr_engine}")

if __name__ == '__main__':
    ocr = OCR()
    ocr.read('img.jpg')