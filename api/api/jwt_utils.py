def jwt_response_payload_handler(token, user=None, request=None):
    """
    :desc: Overriden handler to add extra data in response
    """

    if user is not None:
        is_admin = user.is_superuser
    else:
        is_admin = False

    return {
        'token': token,
        'is_admin': is_admin,
        'user_id': user.id
    }