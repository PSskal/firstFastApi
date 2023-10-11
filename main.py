# import uvicorn
from fastapi import FastAPI
from app.routes import users, basic_auth_users, users_db

app = FastAPI()
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello nesssw"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
