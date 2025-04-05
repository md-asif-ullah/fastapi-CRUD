from datetime import datetime, timedelta, timezone
import jwt
from config.config import settings


def jwt_encoded_data(user_data):
    """
    Function to encode user data into JWT token
    """
    try:
        # Set the expiration time for the token
        encoded_data = user_data.copy()
        encoded_data["exp"] = datetime.now(timezone.utc) + timedelta(days=1)

        # Create JWT token
        encoded_jwt = jwt.encode(
            payload=encoded_data,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
    except Exception as e:
        return None

def jwt_decode_data(token):
    """
    Function to decode JWT token
    """
    try:
        decoded_data = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return decoded_data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None