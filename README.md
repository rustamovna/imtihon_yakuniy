 
# 🛒 Marketplace (E’lonlar sayti)

Bu loyiha Django asosida ishlab chiqilgan **onlayn marketplace platformasi** bo‘lib, foydalanuvchilar turli kategoriyalarda e’lon joylashlari, mahsulotlar sotib olish/sotish jarayonini amalga oshirishlari va bir-birlari bilan muloqot qilishlari mumkin.  

---

## ✨ Loyihaning asosiy imkoniyatlari

## Texnologiyalar
- Django 5
- Bootstrap 4
- SQLite (standart bazasi)


### 👤 Foydalanuvchi qismi
- Ro‘yxatdan o‘tish, tizimga kirish va chiqish.
- Profilni tahrirlash (rasm va ma’lumotlarni yangilash).
- Parolni tiklash:
  - Foydalanuvchi login, email yoki telefon raqamini kiritadi.
  - Terminal orqali kod yuboriladi.
  - Kodni tasdiqlaganidan so‘ng yangi parol qo‘yadi.

---

### 📢 E’lonlar (Ads)
- Yangi e’lon qo‘shish (rasmlar bilan).
- E’lonni tahrirlash va ko‘rish.
- E’lonlar kategoriyalar bo‘yicha ko‘rsatiladi.
- Qidiruv (nom va tavsif bo‘yicha).
- Har bir e’londa:
  - Ko‘rilganlar soni hisoblanadi.
  - Sotuvchi va xaridor o‘rtasida chat boshlash mumkin.

---

### ❤️ Sevimlilar
- Har bir foydalanuvchi e’lonni **like/favorite** qilishi mumkin.
- Sevimlilarga qo‘shilgan e’lonlar alohida sahifada ko‘rinadi.
- CBV (Class Based Views) asosida yozilgan.

---

### 💬 Muloqot (Chat)
- Xaridor va sotuvchi o‘rtasida **xabar almashish tizimi**.
- Har bir e’lon uchun alohida chat threaddi yaratiladi.
- Real vaqt rejimida xabarlarni ko‘rish (oddiy reload orqali).

---

### 🚨 Shikoyatlar (Complaints)
- Xaridor yoki foydalanuvchi e’londan shikoyat qilishi mumkin.
- Shikoyatlar admin panelda ko‘rinadi.
- E’lonni tasdiqlash yoki bloklash imkoniyati mavjud.

---

### 🛠 Admin panel (Moderator uchun)
- E’lonlarni tasdiqlash/bloklash.
- Kategoriyalar va shaharlarni boshqarish.
- Foydalanuvchi yuborgan shikoyatlarni ko‘rib chiqish.

---

## 📂 Loyiha tuzilishi

marketplace/
│── ads/ # E’lonlar app’i
│ ├── models.py # Ad, Category, Favorite, Complaint
│ ├── views.py # E’lonlar, qidiruv, sevimlilar, shikoyatlar
│ └── templates/
│
│── chat/ # Chat app’i
│ ├── models.py # MessageThread, Message
│ ├── views.py # Xabar yuborish va ko‘rish
│ └── templates/
│
│── users/ # Foydalanuvchilar app’i
│ ├── models.py # Profile
│ ├── views.py # Ro‘yxatdan o‘tish, login, logout, parol tiklash
│ └── templates/
│
│── marketplace_project/ # Asosiy konfiguratsiya
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
└── manage.py




---

## 🚀 Ishga tushirish

1. Loyihani klonlash:
   ```bash
   git clone https://github.com/username/marketplace.git
   cd marketplace

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
## username:  -- Admin05
## Email: -- admin05@gmail.com
## parol: -- Admin@123



python manage.py runserver

