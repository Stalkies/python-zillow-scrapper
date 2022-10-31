def decode_url(url: str) -> str:
    url = url.replace('%22', '"')
    url = url.replace('%7B', '{')
    url = url.replace('%7D', '}')
    url = url.replace('%3A', ':')
    url = url.replace('%2C', ',')
    url = url.replace('%5B', '[')
    url = url.replace('%5D', ']')
    url = url.replace('%20', ' ')
    url = url.replace('%2F', '/')
    url = url.replace('%3F', '?')
    url = url.replace('%3D', '=')
    url = url.replace('%26', '&')
    url = url.replace('%25', '%')
    return url

def encode_url(url: str) -> str:
    url = url.replace('"', '%22')
    url = url.replace(':', '%3A')
    url = url.replace('\'', '')
    return url