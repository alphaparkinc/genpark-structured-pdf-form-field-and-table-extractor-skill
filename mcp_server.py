"""MCP server for Structured PDF Form Field and Table Extractor."""
import sys
import json
from client import StructuredDocumentExtractor


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "extract_key_value_pairs",
                    "description": "Extracts normalized key-value fields from semi-structured PDF text extracts and invoices",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
                {
                    "name": "extract_tables",
                    "description": "Parses tabular matrix blocks from document text into structured list of record dicts",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
                {
                    "name": "chunk_document_by_sections",
                    "description": "Chunks complex business contracts and reports along section headers without splitting internal tables",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "max_chunk_size": {"type": "integer", "default": 800},
                        },
                        "required": ["text"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "extract_key_value_pairs":
            res = StructuredDocumentExtractor.extract_key_value_pairs(args.get("text", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "extract_tables":
            res = StructuredDocumentExtractor.extract_tables(args.get("text", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "chunk_document_by_sections":
            res = StructuredDocumentExtractor.chunk_document_by_sections(
                args.get("text", ""),
                max_chunk_size=args.get("max_chunk_size", 800),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
