from fastapi import HTTPException


def raise_not_found(message):

    raise HTTPException(
        status_code=404,
        detail=message
    )


def raise_bad_request(message):

    raise HTTPException(
        status_code=400,
        detail=message
    )


def raise_server_error(message):

    raise HTTPException(
        status_code=500,
        detail=message
    )