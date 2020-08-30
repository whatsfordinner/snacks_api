from snackdrawer import db

def find_by_name(name: str) -> object:
    pass

def find_by_id(id: int) -> object:
    pass

def get_user_drawers(user_id: int) -> list:
    pass

def get_contents(drawer_id: int) -> list:
    snacks = []
    results = db.get_db().get_snacks_in_drawer(drawer_id)
    for result in results:
            snacks.append(result)
    
    return snacks