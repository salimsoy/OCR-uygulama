import easyocr
import pytesseract
from PIL import Image
import os
import json


class OcrInvoice:
    def __init__(self):
        self.folder_path = "C:/Users/salim/Desktop/python-kodlari/staj/OCR/fatura"
        self.reader = easyocr.Reader(['tr', 'en'], gpu=True)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.tesseract_list = []
        self.easy_ocr_list = []
    
    
    def easy_ocr(self, foto_path, index, file_name):
        try:
            print(f"{index}. Resim Okunuyor")
            texts = self.reader.readtext(foto_path, detail=0)
            text = "\n".join(texts)
            text = "file name:" + file_name + "\n" + text
            self.easy_ocr_list.append(text)

        except FileNotFoundError:
            print("Belirtilen resim dosyası bulunamadı")
        except Exception as e:
            print(f"Hata: {e}")
            

    def tesseract(self, foto_path, index, file_name):
        try:
            print(f"{index}. Resim Okunuyor")
            text = pytesseract.image_to_string(Image.open(foto_path))
            text = "file name:" + file_name + "\n" + text
            self.tesseract_list.append(text)
            
        except FileNotFoundError:
            print("Belirtilen resim dosyası bulunamadı")
        except Exception as e:
            print(f"Hata: {e}")
    
            
    def easy_ocr_save(self):
        result = []
        for texts in self.easy_ocr_list:
            first_line, _ ,text = texts.partition("\n")
            file_name = first_line.split(":")[1]
            result.append({"file name": file_name, 
                         "text": text
                         })
        
        with open("easy_ocr.json","w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
       
            
    def tesseract_save(self):
        result = []
        for texts in self.tesseract_list:
            first_line, _ ,text = texts.partition("\n")
            file_name = first_line.split(":")[1]
            result.append({"file name": file_name, 
                         "text": text
                         })
        
        with open("tesseract_ocr.json","w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
    
    def main(self):
        for index, file_name in enumerate(os.listdir(self.folder_path)):
            if file_name.lower().endswith(".jpg"):
                foto_path = self.folder_path + "/" + file_name
                print(foto_path)
                self.easy_ocr(foto_path, index+1, file_name)
                self.tesseract(foto_path, index+1, file_name)
                
        self.tesseract_save()
        self.easy_ocr_save()
                
                
            
if __name__ == "__main__":
    proses = OcrInvoice()
    proses.main()

                
    