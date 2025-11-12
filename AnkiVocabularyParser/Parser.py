# Initialize PaddleOCR instance
from sklearn.cluster import AgglomerativeClustering
import json
import numpy as np
import re
from VocabularyParser.SpellChecker import getSpellChecker

class Parser:
    def __init__(self, config):
        self.checker = getSpellChecker(config)
    
    def parse(self, json_file):
        data = json.load(open(json_file, 'r', encoding='utf-8'))

        cluster = AgglomerativeClustering(n_clusters=None, 
                                          linkage="single", 
                                          distance_threshold=25)
        x_left = [poly[0][0] for poly in data['rec_polys']]
        x_left = np.array(x_left).reshape(-1, 1)
        cluster.fit_predict(x_left)
        num_rows = len(set(cluster.labels_))

        text = [[] for _ in range(num_rows)]
        boxes = [[] for _ in range(num_rows)]
        for idx, j in enumerate(cluster.labels_):
                text[j].append(data['rec_texts'][idx])
                boxes[j].append(data['rec_polys'][idx])
        
        # order clusters left to right
        cluster_centers = [np.median(x_left[np.array(cluster.labels_)==i]) for i in range(num_rows)]
        sorted_indices = np.argsort(cluster_centers)
        text = [text[i] for i in sorted_indices]
        boxes = [boxes[i] for i in sorted_indices]

        #sort text and boxed top to bottom within each cluster 
        for i in range(num_rows):
            y_coords = [box[0][1] for box in boxes[i]]
            sorted_indices = np.argsort(y_coords)
            text[i] = [text[i][j].strip() for j in sorted_indices]
            boxes[i] = [boxes[i][j] for j in sorted_indices]

        text = [self.re_filter(txt) for txt in text]
        box_centers = [self.calc_box_centers(box) for box in boxes]
        merged = [self.merge(bc, t) for bc,t in zip(box_centers, text)]
        boxes_merged = [m[0] for m in merged]
        text_merged = [m[1] for m in merged]

        results = [self.fifo_match(boxes_merged.pop(0), 
                                   text_merged.pop(0), 
                                   boxes_merged.pop(0), 
                                   text_merged.pop(0)) for _ in range(len(boxes)//2)]

        results = [self.check_spelling(res) for res in results] 
        results = [self.add_html(res) for res in results]
        return results
    
    def check_spelling(self, results):
        for idx, (it, de) in enumerate(results):
            results[idx] = self.check_spelling.check(it, de)
        
    
    def add_html(self, results):
        for idx, (it, de) in enumerate(results):
            if " pl " in it:
                results[idx][0] = it.replace(" pl ", " <i> pl ").replace("\"", "") + " </i>"
                results[idx][0] = f"\"{results[idx][0]}\""
            if " inf " in it:
                results[idx][0] = it.replace(" inf ", " <i> inf ").replace("\"", "") + " </i>"
                results[idx][0] = f"\"{results[idx][0]}\""
        return results 
    
    def re_filter(self, text):
        lection_number_pattern = re.compile(r'\d.')
        for j in range(len(text)):
            text[j] = re.sub(lection_number_pattern, '', text[j]).strip() 
        return text

       
    def calc_box_centers(self, boxes): 
        return [[(b[0][0]+b[3][0])/2, (b[0][1] + b[3][1]) / 2] for b in boxes]


    def merge(self, box, text):
        avg_dist = np.median((np.asarray(box)[:,1]-np.roll(np.asarray(box)[:,1], 1))[1:])
        idx = 0
        while idx < len(box):
            b0, t0 = box[idx], text[idx]
            if idx+1 >= len(box) :
                return box, text
            b1, t1 = box[idx+1], text[idx+1]
            
            if np.abs(b0[1]-b1[1]) < avg_dist//4:
                # join left to right
                if b0[0] < b1[0]:
                    box[idx] = np.mean([b0, b1],0)
                    text[idx] = " ".join([t0,t1])
                else:
                    box[idx] = np.mean([b1,b0],0)
                    text[idx] = " ".join([t1,t0])
                box.pop(idx+1)
                text.pop(idx+1)
            idx += 1
        
        return box, text               


    def fifo_match(self, box0, text0, box1, text1):
        avg_dist = np.median((np.asarray(box0)[:,1]-np.roll(np.asarray(box0)[:,1], 1))[1:])
        results = []
        b0 = box0[0]
        b1 = box1[0]
        last0 = False
        last1 = False
        while True:
            # lookahead if both boxes are close enough in y axis
            if len(box0) > 0:
                b0 = box0[0]
            if len(box1) > 0:
                b1 = box1[0]
            if len(box0) == 0:
                last0 = True
            if len(box1) == 0:
                last1 = True

            if np.abs(b0[1] - b1[1]) < avg_dist//2:
                b0, it = box0.pop(0), text0.pop(0)
                b1, de = box1.pop(0), text1.pop(0)
                results.append([[it],[de]])

            elif not last0 and b0[1] < b1[1]:
                b0, it = box0.pop(0), text0.pop(0)
                results[-1][0].append(it)
                    
     
            elif not last1 and b0[1] > b1[1]:
                if len(box1) > 0:
                    b1, de = box1.pop(0), text1.pop(0)
                    results[-1][1].append(de)
                    
            elif last0 and len(box1) > 0:
                b1, de = box1.pop(0), text1.pop(0)
                results[-1][1].append(de)

            elif last1 and len(box0) > 0:
                b0, it = box0.pop(0), text0.pop(0)
                results[-1][0].append(it)
                    
                    
            if len(box0) == 0 and len(box1) == 0:
                for idx, (it, de) in enumerate(results):
                    if len(it) > 1:
                        results[idx][0] = [" <br> ".join(it)]
                    if len(de) > 1:
                        results[idx][1] = [" <br> ".join(de)]
                    results[idx][0] = f"\"{results[idx][0][0]}\""
                    results[idx][1] = f"\"{results[idx][1][0]}\""
                return results 
            
            
if __name__ == '__main__':
    parser = Parser()
    results = parser.parse("output/1_bevenuti_1_res.json")
    for list in results:
        for it, de in list:
            print(f"IT: {it} | DE: {de}")