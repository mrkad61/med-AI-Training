import pandas as pd

dosya_yolu = "div_siz_final_veri.csv"

# Veriyi oku
df = pd.read_csv(dosya_yolu, sep='|', encoding='utf-8-sig')

print(f"✅ Toplam Veri Sayısı: {len(df)}")
print("-" * 30)

# 1. Boş Veri Kontrolü (Null Check)
print("Boş (Null) Değer Kontrolü:")
print(df.isnull().sum())
print("-" * 30)

# 2. Sınıf Dağılımı (Hangi branştan kaç soru var?)
print("Kategori (Label) Dağılımı:")
dagilim = df['label'].value_counts()
print(dagilim)

print("-" * 30)
# 3. En az ve en çok verisi olan branşlar
print(f"En çok veri: {dagilim.idxmax()} ({dagilim.max()} adet)")
print(f"En az veri: {dagilim.idxmin()} ({dagilim.min()} adet)")

# 4. Göz ucuyla kontrol için rastgele 3 örnek
print("-" * 30)
print("Rastgele 3 Örnek:")
print(df.sample(3))