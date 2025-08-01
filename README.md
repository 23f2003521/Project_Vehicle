# 🚗 Project_Vehicle – Smart Park V2

📄 **Visit this report for detailed information:**  
[Smart Park Final Report (Google Drive)](https://drive.google.com/file/d/1yII80yU1app5_VYEHPBEl81Matun5nlX/view?usp=sharing)

---

## 🔧 Setup Instructions

### 🌀 Clone the repository

```bash
git clone https://github.com/23f2003521/Project_Vehicle.git
cd project_Vehicle
```

---

### 🐍 Create virtual environment  
*(For backend jobs like `redis-server` to run, make sure you copy the folder into Ubuntu if you're using WSL)*

```bash
python3 -m venv .env  # make sure you're in the root folder
source .env/bin/activate  # Windows: .env\Scripts\activate
```

---

### 📦 Install dependencies

```bash
pip3 install -r requirements.txt  # from the root directory

flask db init
flask db migrate
flask db upgrade

python app.py  # to run the Flask backend
```

---

### 🌐 Frontend Setup

```bash
cd Frontend  # move into the frontend folder (not inside .env)

npm install
npm run dev  # visit http://localhost:5173 or similar to use the app
```

---

### 🔁 Start Background Workers (Open 3 more terminals in root path with activated env)

1️⃣ **Start Redis server**
```bash
redis-server
```

2️⃣ **Start Celery worker**
```bash
celery -A app.celery worker --loglevel=info
```

3️⃣ **Start Celery beat**
```bash
celery -A app.celery beat --loglevel=info
```

---
