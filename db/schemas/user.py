def user_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'mail': user['mail']
    }


def users_schema(users) -> list:
    return [user_schema(user)for user in users]
