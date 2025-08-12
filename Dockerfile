# Python asosiy image
FROM python:3.10-slim

# Ishlash muhitini sozlash
WORKDIR /app

# Dasturiy ta'minotni o'rnatish
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Talablar faylini nusxalash
COPY requirements.txt .

# Paketlarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . .

# Portni ochish
EXPOSE 8000

# Dasturni ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "conf.wsgi:application"]