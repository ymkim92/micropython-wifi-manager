import re


def write_credentials(wifi_credentials, profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("{0};{1}\n".format(ssid, password))
    with open(wifi_credentials, "w") as file:
        file.write("".join(lines))


def read_credentials(wifi_credentials, logger) -> dict:
    """return {ssid, password} for WiFi access point"""
    lines = []
    profiles = {}
    try:
        with open(wifi_credentials, "r") as file:
            lines = file.readlines()
    except Exception as error:
        if logger:
            logger.error(error)
    for line in lines:
        ssid, password = line.strip().split(";")
        profiles[ssid] = password

    return profiles


def url_decode(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    result = bytearray()
    i = 0
    while i < len(data):
        if data[i : i + 1] == b"%":
            if i + 2 < len(data) and data[i + 1 : i + 3].isalnum():
                try:
                    result.append(int(data[i + 1 : i + 3], 16))
                    i += 3
                    continue
                except ValueError:
                    pass
        result.append(data[i])
        i += 1
    return bytes(result)


def parse_request(request_bytes: bytes) -> str | None:
    """Return the URL path from raw HTTP GET/POST bytes, or None on failure."""
    match = re.search(b"(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request_bytes)
    if not match:
        return None
    return match.group(1).decode("utf-8").rstrip("/")
