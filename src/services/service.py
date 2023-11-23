from fastapi import (APIRouter, 
                     Depends, 
                     HTTPException,
                     status)

from utils import (get_data_from_retailcrm, 
                   send_data_to_third_party_api)


router = APIRouter(
    prefix="/service",
    tags=['Work with data']
)


@router.post("/send_data")
async def send_data_to_database(user: str, 
                                data: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends data to the database.
    """
    try:
        url = 'http://94.241.143.164:8000/docs/site/add_site_data/'
        await send_data_to_third_party_api(url=url,
                                           name=user,
                                           data=data[0])
        return {'status': True,
                'message': "Success!"}
    except HTTPException as e:
        return {'message': "There's a mistake somewhere! Check the code.",
                'status': status.HTTP_400_BAD_REQUEST}



@router.post("/send_items")
async def send_items_to_database(user: str, 
                                 items: dict = Depends(get_data_from_retailcrm)):
    """
    The router sends the items to the database.
    """
    try:
        url = 'http://94.241.143.164:8000/docs/site/add_site_items/'
        await send_data_to_third_party_api(url=url,
                                           name=user,
                                           data=items[1])
        return {'status': True,
                'message': "Success!"}
    except HTTPException as e:
        return {'message': "There's a mistake somewhere! Check the code.",
                'status': status.HTTP_400_BAD_REQUEST}

