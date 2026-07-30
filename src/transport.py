from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from .adapters.db import ConnectionPool
from .business import normalize_page_content
from .config import settings
from .models import ProfilePage
from .repository import ProfileRepository, RepositoryError
from .validation import deserialize_profile_payload, parse_json_body, PayloadValidationError


class RequestHandler(BaseHTTPRequestHandler):
    repository: ProfileRepository

    def _set_headers(self, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

    def _json_response(self, payload: dict[str, Any], status: int = 200) -> None:
        self._set_headers(status)
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _handle(self, handler: Any) -> None:
        try:
            handler()
        except PayloadValidationError as exc:
            self._json_response({"error": str(exc)}, status=400)
        except RepositoryError as exc:
            self._json_response({"error": str(exc)}, status=500)
        except Exception:
            self._json_response({"error": "Internal server error."}, status=500)

    def do_GET(self) -> None:
        def handle() -> None:
            if self.path == "/healthz":
                self._json_response({"status": "ok"})
                return
            self._json_response({"error": "Not found."}, status=404)

        self._handle(handle)

    def do_POST(self) -> None:
        def handle() -> None:
            if self.path != "/profile":
                self._json_response({"error": "Not found."}, status=404)
                return

            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length)
            payload = parse_json_body(raw_body)
            page = deserialize_profile_payload(payload)
            normalized = normalize_page_content(page)
            record_id = self.repository.save(serialize_payload(normalized))
            self._json_response({"id": record_id}, status=201)

        self._handle(handle)


def serialize_payload(page: ProfilePage) -> dict[str, object]:
    return {
        "title": page.title,
        "description": page.description,
        "hero": {
            "title": page.hero.title,
            "lead": page.hero.lead,
            "eyebrow": page.hero.eyebrow,
            "actions": [
                {"label": action.label, "target": action.target, "style": action.style}
                for action in page.hero.actions
            ],
            "stats": [
                {"value": stat.value, "description": stat.description}
                for stat in page.hero.stats
            ],
        },
        "sections": [
            {
                "section_id": section.section_id,
                "eyebrow": section.eyebrow,
                "title": section.title,
                "content": section.content,
                "section_type": section.section_type,
            }
            for section in page.sections
        ],
    }


def create_server(host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    pool = ConnectionPool(settings.DATABASE_URL, max_connections=settings.DATABASE_MAX_CONNECTIONS)
    RequestHandler.repository = ProfileRepository(pool)
    return HTTPServer((host, port), RequestHandler)


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = create_server(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
