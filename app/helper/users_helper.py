def serizlized_users_data(users):
    users["_id"] =str(users["_id"])
    
    return users
