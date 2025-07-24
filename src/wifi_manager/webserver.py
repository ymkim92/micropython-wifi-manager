from wifi_manager.network_utils import (
    build_root_form,
    parse_request,
    read_credentials,
    write_credentials,
    parse_configure_params,
)


class WebServer:
    def __init__(
        self,
        manager: "WifiManager",  # type: ignore
        logger: "ConsoleLogger",  # type: ignore
        sleep_fn: callable,
        reset_fn: callable,
    ):
        self.manager = manager
        self.logger = logger
        self.wlan_ap = manager.wlan_ap
        self.wlan_sta = manager.wlan_sta
        self.ap_ssid = manager.ap_ssid
        self.ap_password = manager.ap_password
        self.ap_authmode = manager.ap_authmode
        self.wifi_credentials = manager.wifi_credentials
        self.sleep_fn = sleep_fn
        self.reset_fn = reset_fn

        assert self.manager is not None, "Manager must be provided"
        assert self.logger is not None, "Logger must be provided"
        assert self.sleep_fn is not None, "Sleep function must be provided"
        assert self.reset_fn is not None, "Reset function must be provided"

    def _reboot_device(self):
        """Reboot the device after a delay."""
        self.logger.info("The device will reboot in 5 seconds.")
        self.sleep_fn(5)
        self.reset_fn()

    def _handle_client(self, client):
        """Handle a single client connection.
        client: socket object representing the client connection (socket.socket)."""
        try:
            client.settimeout(5.0)
            request = b""
            while True:
                chunk = client.recv(128)
                if not chunk:
                    break
                request += chunk
                if b"\r\n\r\n" in request:
                    break

            self.logger.debug(f"Received request: {request.decode('utf-8', errors='ignore')}")

            url = parse_request(request)
            if url == "":
                self.handle_root(client)
            elif url == "configure":
                self.logger.debug(f"Received request: {request.decode('utf-8', errors='ignore')}")
                self.handle_configure(client, request)
            else:
                self.handle_not_found(client)
        except Exception as error:
            self.logger.debug(f"Error handling client: {error}")
        finally:
            client.close()

    def run(self, client_socket):
        """Start the web server.
        client_socket: socket object representing the client connection (socket.socket)."""
        if client_socket is None:
            self.logger.error("Client socket is not created. Cannot run the web server.")
            return
        self.wlan_ap.active(True)
        self.wlan_ap.config(
            essid=self.ap_ssid, password=self.ap_password, authmode=self.ap_authmode
        )
        output = f"Connect to {self.ap_ssid} with the password {self.ap_password} "
        output += f"and access the captive portal at {self.wlan_ap.ifconfig()[0]}"
        self.logger.info(output)

        while True:
            if self.wlan_sta.isconnected():
                self.wlan_ap.active(False)
                self._reboot_device()
                return  # just for testing

            self._handle_client(client_socket)

    def send_header(self, client, status_code=200):
        """Send HTTP headers to the client."""
        client.send(f"HTTP/1.1 {status_code} OK\r\n".encode("utf-8"))
        client.send("Content-Type: text/html\r\n".encode("utf-8"))
        client.send("Connection: close\r\n\r\n".encode("utf-8"))

    def send_response(self, client, payload, status_code=200):
        """Send an HTTP response with HTML content."""
        self.send_header(client, status_code)
        client.sendall(
            f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>WiFi Manager</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="icon" href="data:,">
                </head>
                <body>
                    {payload}
                </body>
            </html>
            """.encode("utf-8")
        )
        client.close()

    def handle_root(self, client, scan_results: list[bytes]):
        """Handle the root URL."""
        ssids = [net.decode() for net in scan_results]
        html = build_root_form(ssids)
        self.send_response(client, html)

    def handle_configure(self, client, request: bytes) -> None:
        """Handle the configure URL."""
        params = parse_configure_params(request)
        if not params:
            self.send_response(client, "<p>Parameters not found!</p>", 400)
            return
        ssid, password = params
        if not ssid:
            self.send_response(
                client, "<p>SSID must be provided!</p><p>Go back and try again!</p>", 400
            )
        elif self.manager.wifi_connect(ssid, password):
            self.send_response(
                client,
                f"<p>Successfully connected to</p><h1>{ssid}</h1><p>IP address: "
                f"{self.wlan_sta.ifconfig()[0]}</p>",
            )
            profiles = read_credentials(self.wifi_credentials, self.logger)
            profiles[ssid] = password
            write_credentials(self.wifi_credentials, profiles)
            self._reboot_device()
        else:
            self.send_response(
                client, f"<p>Could not connect to</p><h1>{ssid}</h1><p>Go back and try again!</p>"
            )
            self.sleep_fn(5)

    def handle_not_found(self, client):
        """Handle unknown URLs."""
        self.send_response(client, "<p>Page not found!</p>", 404)
