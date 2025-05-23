from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API Lu Estilo está online!"}
