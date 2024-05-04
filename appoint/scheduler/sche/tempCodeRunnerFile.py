ef create_token(userid,salt):
    #convert userid to bytes
    userid_bytes=str(userid).encode()
    
    hmac_hash=hmac.new(salt,userid_bytes,hashlib.sha256).digest()
    
    token=base64.b64encode(hmac_hash.digest()).decode()
    
    return token 