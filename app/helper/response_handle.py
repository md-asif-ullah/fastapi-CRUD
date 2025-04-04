
def success_response(
    data: dict = None,
    message: str = "success",
    status_code: int = 200,
) -> dict:
    return {
        "status": status_code,
        "message": message,
        "data": data,
    }

def error_response(
    message: str = "error",
    status_code: int = 400,
) -> dict:
    return {
        "status": status_code,
        "message": message,
        "data": None,
    }