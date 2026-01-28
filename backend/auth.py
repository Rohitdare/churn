from fastapi import Header, HTTPException

VALID_API_KEYS = {
    "tf_test_key_123": "cmp_taskflow"
}

def verify_api_key(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    api_key = authorization.split(" ")[1]
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return VALID_API_KEYS[api_key]
