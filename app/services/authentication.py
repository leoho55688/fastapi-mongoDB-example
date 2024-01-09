from app.db.errors import EntityDoesNotExist
from app.db.collections.users import UserCollection

async def check_username_is_taken(col: UserCollection, username: str) -> bool:
    try:
        await col.get_user_by_username(username=username)
    except EntityDoesNotExist:
        return False
    
    return True

async def check_email_is_taken(col: UserCollection, email:str) -> bool:
    try:
        await col.get_user_by_email(email=email)
    except EntityDoesNotExist:
        return False
    
    return True