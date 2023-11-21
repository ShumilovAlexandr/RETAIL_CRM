from fastapi import FastAPI


from services import router as service_router

app = FastAPI(
    title="RetailCRM",
    description="A service for extracting data from the Retail CRM website, "
                "cleaning them, and sending them via the API to the database."
)

app.include_router(service_router)


