# genpark-structured-pdf-form-field-and-table-extractor-skill

Tabular data matrix extractor, key-value form field normalizer, and semi-structured document chunker.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Key-Value Form Field Harvester**: Parses arbitrary semi-structured invoices, receipts, and tax forms into normalized snake_case key-value dictionaries.
- **Tabular Matrix Extractor**: Detects delimiter-bound and ASCII table structures, returning typed dictionaries with column headers as keys.
- **Section-Aware Smart Chunking**: Segments multi-page documents at logical headings without fragmenting internal table cells or key-value groups.

## Architecture

```
[Raw PDF / OCR Text Stream]
             │
             ▼
┌─────────────────────────────────────────────────────┐
│             StructuredDocumentExtractor             │
│  - Colon-Delimited Form Field Key-Value Normalizer  │
│  - Pipe & ASCII Tabular Matrix Extractor            │
│  - Boundary-Aware Section & Heading Chunk Engine    │
└─────────────────────────────────────────────────────┘
             │
             ▼
[Normalized Key-Values / Structured Table Rows / Section Chunks]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `extract_key_value_pairs`: Extracts normalized key-value fields from semi-structured PDF text extracts and invoices.
- `extract_tables`: Parses tabular matrix blocks from document text into structured list of record dicts.
- `chunk_document_by_sections`: Chunks complex business contracts and reports along section headers without splitting internal tables.

## Quickstart (Python API)

```python
from client import StructuredDocumentExtractor

doc = "Invoice Number: INV-101\nTotal: $500.00"
res = StructuredDocumentExtractor.extract_key_value_pairs(doc)
print("Extracted:", res["fields"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
