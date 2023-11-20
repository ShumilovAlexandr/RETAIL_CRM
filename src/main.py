import uvicorn

from fastapi import FastAPI


from services import router as service_router

app = FastAPI(
    title="RetailCRM",
    description="A service for extracting data from the Retail CRM website, "
                "cleaning them, and sending them via the API to the database."
)

app.include_router(service_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
