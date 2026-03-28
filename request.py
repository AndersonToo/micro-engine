# request.py  —  Phase 2: HTTP Request Parser

class Request:
    def __init__(self, raw: str):
        self.method = None
        self.path = None
        self.http_version = None
        self.headers = {}
        self.body = ""
        self._parse(raw)

    def _parse(self, raw: str):
        if not raw.strip():
            return  # guard against Chrome's empty pre-connections

        # HTTP format:
        # LINE 1:  METHOD PATH HTTP/VERSION
        # LINES 2+: Header-Name: Header-Value
        # BLANK LINE
        # BODY (optional)

        # Split headers section from body on the blank line
        if "\r\n\r\n" in raw:
            header_section, self.body = raw.split("\r\n\r\n", 1)
        else:
            header_section = raw

        lines = header_section.split("\r\n")

        # Parse the request line (first line)
        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) == 3:
            self.method, self.path, self.http_version = parts

        # Parse headers (remaining lines)
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)  # split on first colon only
                self.headers[key.strip()] = value.strip()

    def __repr__(self):
        return (
            f"<Request {self.method} {self.path}>\n"
            f"  Headers: {self.headers}"
        )