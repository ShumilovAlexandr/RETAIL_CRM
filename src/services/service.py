import httpx

from fastapi import (APIRouter, 
                     Depends)

from settings.config import (API_KEY, 
                             URL)


router = APIRouter(
    prefix="/service",
    tags=['Work with data']
)


@router.get("/get_data")
def get_data_from_retailcrm():
    """
    The router is designed to receive raw data from a third-party API.

    :param: None
    :return: raw data in json format.
    """
    try:
        data = []
        items = []

        overall_result = httpx.get(f"{URL}?apiKey={API_KEY}").json()["orders"]
        # for res in [*result]:
        #     data_result = {
        #         "offer_id": res["offer"]["id"],
        #         "bonusesCreditTotal": ,
        #         "bonusesChargeTotal": ,
        #         "externalId": ,
        #         "orderType": ,
        #         "orderMethod": ,
        #         "privilegeType": ,
        #         "countryIso": ,
        #         "createdAt": ,
        #         "statusUpdatedAt": ,
        #         "summ": ,
        #         "totalSumm": ,
        #         "prepaySum": ,
        #         "purchaseSumm": ,
        #         "markDatetime": ,
        #         "lastName": ,
        #         "firstName": ,
        #         "phone": ,
        #         "email": ,
        #         "call": ,
        #         "expired": ,
        #         "site": ,
        #         "status": ,
        #         "fullPaidAt": ,
        #         "fromApi": ,
        #         "shipmentStore": ,
        #         "shipped": ,
        #         "currency":  
        #     }
        

        # TODO need to finish
        for result in overall_result:
            if result["items"] != []:
                for res in result["items"]:
                    print(res["offer"])
        return overall_result
        
    except httpx.HTTPError as exc:
        return {"message": f"HTTP Exception for {exc.request.url} - {exc}"}







@router.post("/send_data")
def send_data_to_database(user: str, 
                          data: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends data to the database.
    """
    return


@router.post("/send_items")
def send_items_to_database(user: str, 
                           data: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends the items to the database.
    """
    return
