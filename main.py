# Initialize PaddleOCR instance
from paddleocr import PaddleOCR
from sklearn.cluster import KMeans

class VocParser:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False)
        self.parsed_results = {}

    def parse(self, img, lection="example_lection", num_cols=4) -> None:
        result = self.ocr.predict(
            input=img)
        
        #cluster cols
        
        # Visualize the results and save the JSON results
        for res in result:
            res.print()
            res.save_to_img("output")
            res.save_to_json("output")
            
    def export_results(self, lection):
        with open(f"{lection}.txt", "w") as f:
            for line in self.parsed_results[lection]:
                f.write(f"{line[0]};{line[1]}\n")

if __name__ == "__main__":
    parser = VocParser()
    img_path = "img.jpg"
    result = parser.parse(img_path, lection="example_lection") 
    
