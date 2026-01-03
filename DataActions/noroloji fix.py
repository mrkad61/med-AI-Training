import pandas as pd

dosya_yolu = "div_siz_final_veri.csv"
cikti_dosyasi = "egitime_hazir_veri_seti.csv"

print("Veri yükleniyor...")
df = pd.read_csv(dosya_yolu, sep='|', encoding='utf-8-sig')

# 1. 'Noroloji' -> 'Nöroloji' olarak değiştir
df.loc[df['label'] == 'Noroloji', 'label'] = 'Nöroloji'

# 2. 'Fiziksel Tip ve Rehabilitasyon' -> 'Fizik Tedavi ve Rehabilitasyon' (Daha temiz)
df.loc[df['label'] == 'Fiziksel Tip ve Rehabilitasyon', 'label'] = 'Fizik Tedavi ve Rehabilitasyon'

print("-" * 30)
print("Düzeltme Sonrası Dağılım:")
print(df['label'].value_counts())

# Son dosyayı kaydet
df.to_csv(cikti_dosyasi, index=False, sep='|', encoding='utf-8-sig')
print(f"\n✅ Düzeltildi ve '{cikti_dosyasi}' olarak kaydedildi.")