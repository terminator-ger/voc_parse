import json
import easyocr
class OCR:
    def __init__(self):
        pass

    def read(self, file) -> str:
        pass
    
class EasyOCR(OCR):
    def __init__(self):
        super().__init__()
        self.reader = easyocr.Reader(['it','de']) # this needs to run only once to load the model into memory

    def read(self, file) -> str:
        result = self.reader.readtext(file)
        output = {"rec_poly": [box for box, _, _ in result],
                  "rec_texts": [txt for _, txt, _ in result]
                  }
        
        ofile = file.removesuffix(".jpg")\
                    .removesuffix(".jpeg")\
                    .removesuffix(".png")\
                    .removesuffix(".JPG")\
                    .removesuffix(".JPEG")\
                    .removesuffix(".PNG")
        ofile += ".json"
        with open(ofile, "w+") as fout:
            json.dump(output, fout)
            
        return ofile

from paddleocr import PaddleOCR
class PaddleOCRWrapper(OCR):
    def __init__(self):
        super().__init__()
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False, 
        )

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
        return f"output/{ofile}_res.json"
            

if __name__ == '__main__':
    ocr = OCR()
    ocr.read('img.jpg')