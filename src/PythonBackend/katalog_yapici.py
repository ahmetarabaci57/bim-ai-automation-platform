import pandas as pd

# Bir mimarlık ofisinin resmi birim fiyat ve poz veritabanı mimarisi
data = {
    "PozNo": [
        "Y.23.012/101", "Y.23.012/102", "Y.23.012/103", "Y.23.012/104", 
        "Y.23.015/201", "Y.23.015/202", 
        "Y.16.050/01", "Y.16.050/02", "Y.19.060/11"
    ],
    "MalzemeTipi": [
        "Pencere", "Pencere", "Pencere", "Pencere",
        "Kapı", "Kapı",
        "Duvar", "Duvar", "Zemin"
    ],
    "Ozellik": [
        "AI_1500x1500mm", "AI_2500x2500mm", "AI_1800x1800mm", "AI_2000x2000mm",
        "Ahşap İç Mekan Kapısı", "Yangın Dayanımlı Çelik Kapı",
        "Tuğla Duvar 20cm", "Alçıpan Bölme Duvar", "Granit Seramik Kaplama"
    ],
    "BirimFiyat": [4500, 7800, 5800, 6400, 8500, 16500, 1200, 850, 1450],
    "Birim": ["Adet", "Adet", "Adet", "Adet", "Adet", "Adet", "m2", "m2", "m2"]
}

df = pd.DataFrame(data)

# Dosyayı doğrudan app.py dosyanızın yanına kaydediyoruz
df.to_excel("fiyat_katalogu.xlsx", index=False)
print(">> [BAŞARILI] Gerçekçi mimarlık fiyat kataloğu 'fiyat_katalogu.xlsx' adıyla üretildi.")
