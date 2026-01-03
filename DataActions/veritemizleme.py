import pandas as pd
import os

# --- AYARLAR ---
# En son oluşturduğun (veya üzerinde çalıştığın) dosyanın adını buraya yaz
giris_dosyasi = "temizlenmis_birlesik_veri.csv"
cikis_dosyasi = "div_siz_final_veri.csv"
# ---------------

print("Dosya okunuyor...")

# Önce pipe (|) ile okumayı dener, olmazsa virgül ile dener (Garanti Yöntem)
try:
    df = pd.read_csv(giris_dosyasi, sep='|', encoding='utf-8-sig')
    print("-> Pipe (|) ayırıcı ile okundu.")
except:
    try:
        df = pd.read_csv(giris_dosyasi, sep=',', encoding='utf-8-sig', on_bad_lines='skip')
        print("-> Virgül (,) ayırıcı ile okundu.")
    except Exception as e:
        print(f"HATA: Dosya okunamadı. Sebep: {e}")
        exit()

baslangic_sayisi = len(df)
print(f"Başlangıç Veri Sayısı: {baslangic_sayisi}")

# --- FİLTRELEME İŞLEMİ ---
# İçinde "<div" geçen satırları tespit et ve SİL (Tersini al: ~)
# case=False: Büyük/küçük harf duyarlılığını kapatır (<DIV> de olsa siler)
# na=False: Boş (NaN) veri varsa hata vermez, onu da silmez.
df_temiz = df[~df['text'].str.contains('<div', case=False, na=False)]

bitis_sayisi = len(df_temiz)
silinen_sayisi = baslangic_sayisi - bitis_sayisi

print("-" * 30)
if silinen_sayisi > 0:
    print(f"⚠️ {silinen_sayisi} adet satır içinde '<div>' bulunduğu için silindi.")
else:
    print("✅ Hiçbir satırda '<div>' etiketine rastlanmadı, silme yapılmadı.")

print(f"Kalan Temiz Veri Sayısı: {bitis_sayisi}")

# --- KAYDETME ---
if bitis_sayisi > 0:
    # Yine pipe (|) ile kaydediyoruz ki karışıklık çıkmasın
    df_temiz.to_csv(cikis_dosyasi, index=False, sep='|', encoding='utf-8-sig')
    print(f"💾 Dosya kaydedildi: {cikis_dosyasi}")
else:
    print("❌ Filtreleme sonucu elinizde hiç veri kalmadı! (Tüm verilerde <div> olabilir mi?)")