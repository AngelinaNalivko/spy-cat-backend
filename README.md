# Spy Cat Agency Backend

This is the backend for the **Spy Cat Agency** project. It is built with **FastAPI** and uses **MongoDB** for data storage.

## How to use it:

### 1. Install dependencies

Make sure you are using **Python 3.10+** and have [MongoDB](https://www.mongodb.com/try/download/community) running locally or in the cloud.

```bash

pip install -r requirements.txt
```

### 2. Project Structure

```
backend/
├── main.py                
├── database.py            
├── models/
│   └── spycat.py         
│   └── mission.py          
├── routers/
│   └── missions.py
│   └── spycats.py          
├── services/
│   └── spycatapi.py
└── requirements.txt       
```

### 3. Run the server

```bash

fastapi run main.py
```

## API Collection

You can test the API using the provided Postman collection:
[Postman Collection Link](https://angelina-1815635.postman.co/workspace/Angelina's-Workspace~37295920-0521-442f-8688-a4ef1f8cbf09/collection/45534784-7c9eba34-1dc3-4434-b741-69e5bcd62190?action=share&creator=45534784)
