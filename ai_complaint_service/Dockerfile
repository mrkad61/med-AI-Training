FROM python:3.9-slim

WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Modeli içine gömmek istenirse bu satır açılabilir, ancak model genelde volume ile verilir.
# COPY model/ ./model/

# Portu aç
EXPOSE 8001

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
