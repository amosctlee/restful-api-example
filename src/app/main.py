from fastapi import FastAPI

from routers import products


app = FastAPI()

app.include_router(products.router)


@app.on_event("startup")
async def startup_event():

    from db import Base, engine
    Base.metadata.create_all(bind=engine, tables=[
        Base.metadata.tables["products"]])

    print("initialized db")
