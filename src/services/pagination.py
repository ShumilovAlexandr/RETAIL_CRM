import httpx
import datetime

from fastapi import (APIRouter, 
                     HTTPException,
                     status, 
                     Depends)

from settings.config import (API_KEY, 
                             URL)
from utils import send_data_to_third_party_api



router = APIRouter(
    prefix="/pagination",
    tags=['Pagination']
)


async def extract_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return data


async def get_big_data():
    """
    The function is responsible for receiving data.
    """
    data = []
    items = []
    page = 1

    start_func = datetime.datetime.now()
    while True: 
        url = f'{URL}?page={page}&apiKey={API_KEY}'
        full_result = await extract_data(url=url)
        if not full_result:
            break

        for result in full_result["orders"]:
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
                    "firstName": result.get("firstName", []),
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

            for res in result["items"]:
                items_result = {
                    "bonusesChargeTotal": res["bonusesChargeTotal"],
                    "bonusesCreditTotal": res["bonusesCreditTotal"],
                    "initialPrice": res["initialPrice"],
                    "discountTotal": res["discountTotal"],
                    "vatRate": res["vatRate"],
                    "createdAt": res["createdAt"],
                    "quantity_1": res["quantity"],
                    "status": res["status"],
                    "purchasePrice": res["purchasePrice"],
                    "ordering": res["ordering"],
                    "offer_displayName": res["offer"]["displayName"],
                    "offer_id": res["offer"]["id"],
                    "offer_externalId": res["offer"]["externalId"],
                    "offer_xmlId": res.get("offer", []).get("xmlId", []),
                    "offer_name": res["offer"]["name"],
                    "offer_article": res["offer"]["article"],
                    "offer_vatRate": res["offer"]["vatRate"],
                    "offer_properties_type": res.get("offer", []).get("properties", []).get("type", []),
                    "offer_unit_code": res["offer"]["unit"]["code"],
                    "offer_unit_name": res["offer"]["unit"]["name"],
                    "offer_unit_sym": res["offer"]["unit"]["sym"],
                    "price": float(str([price["price"] for price in res["prices"]])[1:-1])
                }
                items.append(items_result)
        
        if page == full_result["pagination"]["totalPageCount"]:
            break
        else:
            page += 1
    end_func = datetime.datetime.now()
    func_time = end_func - start_func
    
    return data, items, page, func_time


@router.post("/send_big_data")
async def send_data_to_database(user: str, 
                                data: dict = Depends(get_big_data)):
    """
    The router sends big data to the database.
    """
    try:
        url = 'http://94.241.143.164:8000/docs/site/add_site_data/'
        await send_data_to_third_party_api(url=url,
                                           name=user,
                                           data=data[0])
        return {'status': True,
                'message': f"Created - {data[2]} repetitions in {data[3]}"}
    except HTTPException as e:
        return {'message': "There's a mistake somewhere! Check the code.",
                'status': status.HTTP_400_BAD_REQUEST}



@router.post("/send_big_items")
async def send_items_to_database(user: str, 
                                 items: dict = Depends(get_big_data)):
    """
    The router sends the big items to the database.
    """
    try:
        url = 'http://94.241.143.164:8000/docs/site/add_site_items/'
        await send_data_to_third_party_api(url=url,
                                           name=user,
                                           data=items[1])
        return {'status': True,
                'message': f"Created - {items[2]} repetitions in {items[3]}"}
    except HTTPException as e:
        return {'message': "There's a mistake somewhere! Check the code.",
                'status': status.HTTP_400_BAD_REQUEST}

