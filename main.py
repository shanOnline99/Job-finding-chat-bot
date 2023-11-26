from fastapi import FastAPI
import mysql.connector


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Replace these with your actual database credentials
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "1234",
    "database": "job",
}

# Establish a connection to the database
connection = mysql.connector.connect(**db_config)
