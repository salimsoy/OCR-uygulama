# Fatura ve Belge Okuma 
Bu proje, EasyOCR ve Tesseract kütüphanelerini kullanarak fatura veya belge görüntüleri üzerinden metin çıkarma işlemi gerçekleştiren bir Python sınıfı içerir. İki farklı OCR motorunun sonuçlarını karşılaştırmak ve verileri yapılandırılmış JSON formatında saklamak için tasarlanmıştır.

# OCR 
OCR (Optik Karakter Tanıma) taranmış kağıt belgeler PDF dosyaları veya görüntüler gibi farklı türdeki dokümanları makine tarafından okunabilir verilere dönüştürmeye yarayan araçlardır. Bu toollar ve APIlar veri çıkarma sürecini otomatikleştirerek hem zaman hem de emek tasarrufu sağlar. Web ve mobil uygulamalar dahil çeşitli platformlarla sorunsuz şekilde çalışır, böylece kurumlar sıfırdan bir çözüm geliştirmeden sistemlerine OCR yeteneklerini entegre edebilir.

Bu projede iki farklı yaklaşım kullanılmaktadır:
- Tesseract: Google tarafından desteklenen, geleneksel ve yaygın kullanılan bir OCR motorudur.
- EasyOCR: Derin öğrenme (Deep Learning) tabanlı, GPU hızlandırması kullanabilen ve 70'ten fazla dili destekleyen modern bir OCR aracıdır.

** Temel Mantık **
Kod, belirtilen bir dizindeki tüm .jpg formatındaki görselleri tarar ve aşağıdaki adımları izler:

- Hazırlık: Görüntü klasörünü ve OCR motorlarını (EasyOCR için Türkçe/İngilizce dil desteği, Tesseract için .exe yolu) başlatır.
- Tarama: Klasördeki her bir görsel sırayla işleme alınır.
- Metin Çıkarma:
     - Görüntü önce EasyOCR ile işlenir ve metinler birleştirilir.
     - Aynı görüntü Tesseract ile işlenir ve metin dizgisi oluşturulur.
- Veri Yapılandırma: Okunan metinler, dosya isimleriyle eşleştirilerek bellekte tutulur.
- Kaydetme: İşlem bitiminde sonuçlar easy_ocr.json ve tesseract_ocr.json dosyalarına ayrı ayrı kaydedilir.

Avantajları
- Karşılaştırma İmkanı: Hangi OCR kütüphanesinin fatura formatında daha başarılı olduğunu görmeyi sağlar.
- Otomasyon: Çok sayıda faturayı manuel yazmak yerine saniyeler içinde dijital metne çevirir.
- Veri Yapılandırma: Çıktıları JSON formatında verdiği için bu veriler başka yazılımlarda veya veritabanlarında kolayca kullanılabilir.
- Çoklu Dil Desteği: Türkçe ve İngilizce faturaları okuyabilir.

OCR Uygulaması
main fonksiyonu şu şekilde çalışır:

- Klasördeki dosyaları listeler.
- Sadece .jpg uzantılı dosyaları filtreler.
- Her dosyayı sırasıyla easy_ocr ve tesseract fonksiyonlarına gönderir.
- Okuma işlemleri tamamlandığında save fonksiyonları ile verileri diske yazar.

Aşağıda Python kodu ve açıklamaları yer almaktadır:
```python
import easyocr
import pytesseract
from PIL import Image
import os
import json


class OcrInvoice:
    def __init__(self):
        # İşlenecek fatura görsellerinin bulunduğu klasör yolu
        self.folder_path = "C:/Users/salim/Desktop/python-kodlari/staj/OCR/fatura"
        
        # EasyOCR okuyucusunu başlat (Türkçe ve İngilizce, GPU aktif)
        self.reader = easyocr.Reader(['tr', 'en'], gpu=True)
        
        # Tesseract yüklü olduğu yol (Windows için)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Sonuçları tutacak listeler
        self.tesseract_list = []
        self.easy_ocr_list = []
    
    
    def easy_ocr(self, foto_path, index, file_name):
        try:
            print(f"{index}. Resim Okunuyor (EasyOCR)")
            # detail=0 sadece metni döndürür, koordinatları vermez
            texts = self.reader.readtext(foto_path, detail=0)
            
            # Liste dönen metni stringe çevir
            text = "\n".join(texts)
            # Dosya adını metnin başına ekle
            text = "file name:" + file_name + "\n" + text
            self.easy_ocr_list.append(text)

        except FileNotFoundError:
            print("Belirtilen resim dosyası bulunamadı")
        except Exception as e:
            print(f"Hata: {e}")
            

    def tesseract(self, foto_path, index, file_name):
        try:
            print(f"{index}. Resim Okunuyor (Tesseract)")
            # PIL kütüphanesi ile resmi aç ve Tesseract'a gönder
            text = pytesseract.image_to_string(Image.open(foto_path))
            
            # Dosya adını metnin başına ekle
            text = "file name:" + file_name + "\n" + text
            self.tesseract_list.append(text)
            
        except FileNotFoundError:
            print("Belirtilen resim dosyası bulunamadı")
        except Exception as e:
            print(f"Hata: {e}")
    
            
    def easy_ocr_save(self):
        result = []
        for texts in self.easy_ocr_list:
            # Metni dosya adı ve içerik olarak ayır
            first_line, _ ,text = texts.partition("\n")
            file_name = first_line.split(":")[1]
            
            # Sözlük yapısına çevir
            result.append({
                "file name": file_name, 
                "text": text
            })
        
        # JSON dosyasına kaydet
        with open("easy_ocr.json","w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
       
            
    def tesseract_save(self):
        result = []
        for texts in self.tesseract_list:
            # Metni dosya adı ve içerik olarak ayır
            first_line, _ ,text = texts.partition("\n")
            file_name = first_line.split(":")[1]
            
            # Sözlük yapısına çevir
            result.append({
                "file name": file_name, 
                "text": text
            })
        
        # JSON dosyasına kaydet
        with open("tesseract_ocr.json","w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
    
    def main(self):
        # Klasördeki dosyaları döngüye al
        for index, file_name in enumerate(os.listdir(self.folder_path)):
            if file_name.lower().endswith(".jpg"):
                foto_path = self.folder_path + "/" + file_name
                print(foto_path)
                
                # Her iki motor ile okuma yap
                self.easy_ocr(foto_path, index+1, file_name)
                self.tesseract(foto_path, index+1, file_name)
                
        # Tüm işlemler bitince kaydet
        self.tesseract_save()
        self.easy_ocr_save()
                
                
            
if __name__ == "__main__":
    proses = OcrInvoice()
    proses.main()

```
