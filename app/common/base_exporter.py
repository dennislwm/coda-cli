"""Base class for Coda data exporters with shared API response handling"""

import json


class BaseExporter:
    """Base exporter class with common Coda API response parsing logic"""
    
    def __init__(self, pycoda_client):
        """Initialize exporter with Pycoda client"""
        self.pycoda = pycoda_client
    
    def _parse_api_response(self, response_json):
        """Parse API response handling both JSON array and concatenated JSON formats"""
        if not response_json or response_json == "{}":
            return []

        try:
            parsed = json.loads(response_json)
            data = parsed if isinstance(parsed, list) else [parsed]
        except json.JSONDecodeError:
            # Handle concatenated JSON objects from real API
            data = []
            decoder = json.JSONDecoder()
            idx = 0
            while idx < len(response_json.strip()):
                try:
                    obj, end_idx = decoder.raw_decode(response_json, idx)
                    data.append(obj)
                    idx = end_idx
                except json.JSONDecodeError:
                    idx += 1
                    if idx >= len(response_json):
                        break

        # CON-04: a Coda API error object must abort the export, not become CSV
        # rows -- mirrors template_importer.py's consumer-side check. Without this,
        # a 401 wrote ""\r\n""\r\n and exited 0, clobbering the caller's file.
        for obj in data:
            if isinstance(obj, dict) and "error" in obj:
                raise Exception(f"Coda API error: {obj['error']}")
        return data