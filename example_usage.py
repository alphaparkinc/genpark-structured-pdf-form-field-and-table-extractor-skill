"""Example usage for Structured PDF Form Field and Table Extractor."""
from client import StructuredDocumentExtractor


def main():
    sample_doc = """
INVOICE STATEMENT
Invoice Number: INV-2026-9041
Invoice Date: 2026-10-15
Due Date: 2026-11-15
Customer Name: Apex Global Logistics
Total Amount Due: $4,500.00

SECTION 1: LINE ITEMS
| Item Description | Quantity | Unit Price | Total |
|------------------|----------|------------|-------|
| Cloud Compute    | 10       | $250.00    | $2,500|
| Storage Tier B   | 4        | $500.00    | $2,000|

SECTION 2: REMITTANCE TERMS
Please remit payment via ACH within 30 days of invoice date.
Late payments subject to 1.5% monthly finance charge.
"""

    print("=== 1. Extracting Key-Value Form Fields ===")
    kv_res = StructuredDocumentExtractor.extract_key_value_pairs(sample_doc)
    print("Total Pairs:", kv_res["total_pairs_extracted"])
    for k, v in kv_res["fields"].items():
        print(f"  {k}: {v}")

    print("\n=== 2. Extracting Structured Tabular Matrix ===")
    tables = StructuredDocumentExtractor.extract_tables(sample_doc)
    print(f"Tables Found: {len(tables)}")
    if tables:
        t = tables[0]
        print(f"Columns: {t['columns']}")
        print(f"Rows ({t['row_count']}):")
        for r in t["rows"]:
            print(f"  - {r}")

    print("\n=== 3. Chunking Document by Sections ===")
    chunks = StructuredDocumentExtractor.chunk_document_by_sections(sample_doc)
    print(f"Generated {len(chunks)} chunks:")
    for c in chunks:
        print(f"- [{c['section']}] ({c['char_count']} chars)")


if __name__ == "__main__":
    main()
