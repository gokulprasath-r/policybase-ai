from fastapi import FastAPI,status

app = FastAPI()

@app.get("/",status_code=status.HTTP_200_OK)
def main():
    return "Welcome to PolicyBase AI API"
