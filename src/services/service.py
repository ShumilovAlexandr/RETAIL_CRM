import httpx
import json
import pandas as pd

from fastapi import (APIRouter, 
                     Depends)

from settings.config import (API_KEY, 
                             URL)


router = APIRouter(
    prefix="/service",
    tags=['Work with data']
)


@router.get("/get_data")
async def get_data_from_retailcrm():
    """
    The router is designed to receive raw data from a third-party API.

    :param: None
    :return: raw data in json format.
    """
    data = []
    items = []

    try:
        overall_result = httpx.get(f"{URL}?apiKey={API_KEY}").json()["orders"]

        for result in overall_result:

            offer_ids = [res["offer"]["id"] for res in result["items"]]

            for offer_id in offer_ids:

                data_result = {
                    "offer_id": offer_id,
                    "bonusesCreditTotal": result["bonusesCreditTotal"],
                    "bonusesChargeTotal": result["bonusesChargeTotal"],
                    "externalId": result.get("externalId", []),
                    "orderType": result["orderType"],
                    "orderMethod": result.get("orderMethod", []),
                    "privilegeType": result["privilegeType"], 
                    "countryIso": result["countryIso"],
                    "createdAt": result["createdAt"],
                    "statusUpdatedAt": result["statusUpdatedAt"],
                    "summ": result["summ"],
                    "totalSumm": result["totalSumm"],
                    "prepaySum": result["prepaySum"],
                    "purchaseSumm": result["purchaseSumm"],
                    "markDatetime": result["markDatetime"],
                    "lastName": result.get("lastName", []),
                    "firstName": result["firstName"],
                    "phone": result.get("phone", []),
                    "email": result.get("email", []),
                    "call": result["call"],
                    "expired": result["expired"],
                    "site": result["site"],
                    "status": result["status"],
                    "fullPaidAt": result.get("fullPaidAt", []),
                    "fromApi": result["fromApi"],
                    "shipmentStore": result["shipmentStore"],
                    "shipped": result["shipped"],
                    "currency":  result["currency"]
                }
                data.append(data_result)

        return data

        


        
    except httpx.HTTPError as exc:
        return {"message": f"HTTP Exception for {exc.request.url} - {exc}"}







@router.post("/send_data")
async def send_data_to_database(user: str, 
                                data: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends data to the database.
    """
    return


@router.post("/send_items")
async def send_items_to_database(user: str, 
                                 data: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends the items to the database.
    """
    return
