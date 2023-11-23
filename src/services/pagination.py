import httpx
import asyncio

from fastapi import (APIRouter, 
                     HTTPException,
                     status)

from settings.config import (API_KEY, 
                             URL)



router = APIRouter(
    prefix="/pagination",
    tags=['Pagination']
)


async def extract_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return data




@router.get("/get_b_data")
async def get_b_data():
    """
    The router will send a large number of requests to receive data.
    """
    data = []
    items = []
    page = 1

    while True: 
        url = f'{URL}?page={page}&apiKey={API_KEY}'
        full_result = await extract_data(url=url)
        if not full_result:
            break

        for result in full_result['orders']:
            # offer_ids = [res["offer"]["id"] for res in result["items"]]
            # for offer_id in offer_ids:
            #     data_result = {
            #         "offer_id": offer_id,
            #         "bonusesCreditTotal": result["bonusesCreditTotal"],
            #         "bonusesChargeTotal": result["bonusesChargeTotal"],
            #         "externalId": result.get("externalId", []),
            #         "orderType": result["orderType"],
            #         "orderMethod": result.get("orderMethod", []),
            #         "privilegeType": result["privilegeType"], 
            #         "countryIso": result["countryIso"],
            #         "createdAt": result["createdAt"],
            #         "statusUpdatedAt": result["statusUpdatedAt"],
            #         "summ": result["summ"],
            #         "totalSumm": result["totalSumm"],
            #         "prepaySum": result["prepaySum"],
            #         "purchaseSumm": result["purchaseSumm"],
            #         "markDatetime": result["markDatetime"],
            #         "lastName": result.get("lastName", []),
            #         "firstName": result.get("firstName", []),
            #         "phone": result.get("phone", []),
            #         "email": result.get("email", []),
            #         "call": result["call"],
            #         "expired": result["expired"],
            #         "site": result["site"],
            #         "status": result["status"],
            #         "fullPaidAt": result.get("fullPaidAt", []),
            #         "fromApi": result["fromApi"],
            #         "shipmentStore": result["shipmentStore"],
            #         "shipped": result["shipped"],
            #         "currency":  result["currency"]
            #     }
            #     data.append(data_result)

            for res in result["items"]:
                if res != []:
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
                        # "offer_xmlId": res["offer"]["xmlId"],
                        "offer_name": res["offer"]["name"],
                        "offer_article": res["offer"]["article"],
                        "offer_vatRate": res["offer"]["vatRate"],
                        # "offer_properties_type": res["offer"]["properties"]["type"],
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
    print(items)

