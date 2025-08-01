# Project_Vehicle
visit this report for detailed information:
https://drive.google.com/file/d/1yII80yU1app5_VYEHPBEl81Matun5nlX/view?usp=sharing
To run this application:
🔧 Setup Instructions


Clone the repository

bash
git clone https://github.com/23f2003521/Project_Vehicle.git
cd project_Vehicle


Create virtual environment(for backend jobs redis-server to run make sure that you copy folder in ubuntu)

bash
python3 -m venv .env  (make sure path is in root folder)
source .env/bin/activate  # Windows: venv\Scripts\activate

Install dependencies

bash
pip3 install -r requirements.txt (in root path)
flask db init
flask db migrate
flask db upgrade
python app.py (to run the backend)

npm install i (in cd Frontend folder(without env))
npm run dev(to run the frontend, visit frontend localhost to navigate application)

(open 3 more terminals in root path with activated env)
1) redis-server (run redis server)
2) celery -A app.celery worker --loglevel=info
3) celery -A app.celery beat --loglevel=info


 
