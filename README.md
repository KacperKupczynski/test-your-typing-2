# Test Your Typing

Link to the project: [https://test-your-typing-2.vercel.app/](https://test-your-typing.vercel.app/)

My school project to test your typing speed and accuracy. It is a simple web application that allows users to practice typing and track their performance. 
It is built using SvelteKit to frontend and Django to backend.

## Features
- Adding custom texts to practice typing
- Tracking typing speed (words per minute)
- History of previous records
- Stats of the user

## TODO
- Responsive design
- Maybe a better name

## Installation
1. Clone the repository
2. Install the dependencies for the frontend and backend
```bash
cd frontend
npm install
cd ../backend
pip install -r requirements.txt
```
3. Migrate the database
```bash
cd backend
python manage.py migrate
```

4. Run the backend server
```bash
cd backend
python manage.py runserver
``` 
5. Run the frontend server
```bash
cd frontend
npm run dev
```

## Deployment
- The frontend is deployed on Vercel and the backend is deployed on Render. The frontend is connected to the backend using the API endpoints provided by Django Rest Framework.