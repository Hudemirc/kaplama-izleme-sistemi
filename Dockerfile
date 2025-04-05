# Python tabanlı bir image kullan
FROM python:3.11-slim

# Ortam değişkenleri (gerekli optimizasyonlar)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizini
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını container’a kopyala
COPY . .

# Container içindeki port
EXPOSE 8000

# Başlangıç komutu (geçici olarak runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]