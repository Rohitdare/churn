from fastapi import Header, HTTPException

VALID_API_KEYS = {
    "tf_test_key_123": "cmp_taskflow",
    "pt_test_key_456": "cmp_paytrack"
}


def verify_api_key(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        print("❌ Invalid auth header:", authorization)
        raise HTTPException(status_code=401, detail="Invalid auth header")

    api_key = authorization.split(" ")[1]

    if api_key not in VALID_API_KEYS:
        print("❌ Invalid API key received:", api_key)
        raise HTTPException(status_code=401, detail="Invalid API key")

    print("✅ Accepted API key for company:", VALID_API_KEYS[api_key])
    return VALID_API_KEYS[api_key]

