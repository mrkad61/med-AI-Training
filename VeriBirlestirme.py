import pandas as pd
import glob
import os

# --- AYARLAR ---
dosya_yolu = "data/*.csv"  # CSV dosyalarının olduğu klasör
cikti_dosyasi = "temizlenmis_birlesik_veri.csv"
# ---------------
kodlamalar = ['utf-8-sig', 'utf-8', 'cp1254', 'latin1']
dosyalar = glob.glob(dosya_yolu)
tum_veriler = []

print(f"Toplam {len(dosyalar)} dosya işlenecek...")

for dosya in dosyalar:
    try:
        with open(dosya, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # İlk satır başlık mı kontrol et (header)
            # Eğer dosyalarında header (text,label gibi) yoksa bu kısmı sil.
            # Varsa ve standartsa atlamak için:
            if "text" in lines[0].lower() and "label" in lines[0].lower():
                lines = lines[1:]

            for line in lines:
                line = line.strip()  # Baştaki/sondaki boşlukları temizle
                if not line: continue  # Boş satırsa geç

                # SİHİRLİ KISIM: rsplit(',', 1)
                # Satırı SAĞDAN başlayerek, sadece 1 kere virgülden böl.
                parcalar = line.rsplit(',', 1)

                if len(parcalar) == 2:
                    text_kismi = parcalar[0]
                    label_kismi = parcalar[1]

                    # Eğer tırnak içine alınmış satırsa ("..."), tırnakları temizle
                    if text_kismi.startswith('"') and text_kismi.endswith('"'):
                        text_kismi = text_kismi[1:-1]

                    # İçindeki çift tırnakları tek tırnağa çevir (CSV'yi bozmasın diye)
                    text_kismi = text_kismi.replace('"', "'")

                    tum_veriler.append({'text': text_kismi, 'label': label_kismi})
                else:
                    # Bölünemeyen garip satırlar varsa burada görürsün
                    pass

    except Exception as e:
        print(f"Dosya okunurken hata: {os.path.basename(dosya)} - {e}")

# Veriyi DataFrame'e çevir
if tum_veriler:
    df_yeni = pd.DataFrame(tum_veriler)

    # Tekrarlayan verileri temizle
    df_yeni.drop_duplicates(subset=['text'], inplace=True)

    print(f"Veriler birleştirildi. Toplam satır: {len(df_yeni)}")
    print("Örnek veri:")
    print(df_yeni.head())

    # KAYDEDERKEN PIPE (|) KULLANIYORUZ
    # Böylece metin içindeki virgüller bir daha sorun yaratmayacak.
    df_yeni.to_csv(cikti_dosyasi, index=False, sep='|', encoding='utf-8-sig')
    print(f"Dosya başarıyla kaydedildi: {cikti_dosyasi}")
else:
    print("Hiç veri bulunamadı.")