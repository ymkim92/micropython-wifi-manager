from wifi_manager.network_utils import build_root_form, parse_request, url_decode

# def test_write_and_read_credentials(tmp_path):
#     file_path = tmp_path / "wifi.dat"
#     profiles = {"ssid1": "pass1", "ssid2": "pass2"}
#     write_credentials(str(file_path), profiles)
#     loaded = read_credentials(str(file_path))
#     assert loaded == profiles


# def test_write_and_read_credentials_exception(tmp_path):
#     file_path = tmp_path / "wifi.dat"
#     loaded = read_credentials(str(file_path), debug=True)
#     assert loaded == {}


# def test_write_and_read_empty_credentials(tmp_path):
#     file_path = tmp_path / "wifi.dat"
#     profiles = {}
#     write_credentials(str(file_path), profiles)
#     loaded = read_credentials(str(file_path))
#     assert loaded == profiles


def test_url_decode_basic():
    assert url_decode("abc%20def") == b"abc def"
    assert url_decode(b"abc%20def") == b"abc def"
    assert url_decode("") == b""


def test_url_decode_non_encoded():
    assert url_decode("plainstring") == b"plainstring"
    assert url_decode(b"plainstring") == b"plainstring"


def test_url_decode_partial_percent():
    # Should not raise, just return as-is
    assert url_decode("abc%2") == b"abc%2"
    assert url_decode(b"abc%2") == b"abc%2"


def test_url_decode_invalid_percent():
    # Should not raise, just return as-is
    assert url_decode("abc%zz") == b"abc%zz"
    assert url_decode(b"abc%zz") == b"abc%zz"


def test_parse_request_valid():
    request = b"GET /configure HTTP/1.1\r\n\r\n"
    url = parse_request(request)
    assert url == "configure"


def test_parse_request_invalid():
    request = b"BAD REQUEST"
    url = parse_request(request)
    assert url is None


def test_build_root_form_generates_expected_html():
    ssid_list = ["HomeWiFi", "GuestNetwork", "IoT"]
    html = build_root_form(ssid_list)

    # Check that each SSID is correctly used in input and label
    for ssid in ssid_list:
        assert f"<input type='radio' name='ssid' value='{ssid}' id='{ssid}' />" in html
        assert f"<label for='{ssid}'>{ssid}</label>" in html

    # Check static parts of the form
    assert '<form action="/configure" method="post"' in html
    assert 'type="password"' in html
    assert 'name="password"' in html
    assert 'type="submit"' in html
    assert 'value="Connect"' in html


def test_build_root_form_empty_list():
    html = build_root_form([])

    # No radio inputs should be present
    assert "<input type='radio'" not in html

    # Form should still include password and submit fields
    assert 'type="password"' in html
    assert 'type="submit"' in html
