"""Structured PDF Form Field and Table Extractor.
100% Python Standard Library.
"""

import re
from typing import List, Dict, Any, Optional


class StructuredDocumentExtractor:
    """Extracts structured key-value form fields, tabular data matrices, and semantic sections
    from raw PDF text extracts, invoices, forms, and enterprise documents."""

    @classmethod
    def extract_key_value_pairs(cls, text: str) -> Dict[str, Any]:
        """Parses common key-value form patterns such as:
        'Invoice Number: INV-1002' or 'Total Amount: $1,250.00'."""
        lines = text.splitlines()
        extracted = {}

        # Pattern: Word(s) followed by colon and value
        kv_colon_pattern = re.compile(r'^\s*([A-Za-z0-9\s/_\-#]{2,35})\s*:\s*(.+)$')

        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith("|"):
                continue

            # Skip section markers like SECTION 1:
            if re.match(r'^(?:SECTION|ARTICLE)\b', line_str, re.I):
                continue

            match = kv_colon_pattern.match(line_str)
            if match:
                raw_k = match.group(1).strip()
                raw_v = match.group(2).strip()
                # Normalize key to snake_case
                norm_key = re.sub(r'[^a-zA-Z0-9]+', '_', raw_k.lower()).strip('_')
                if norm_key and raw_v:
                    extracted[norm_key] = raw_v

        return {
            "total_pairs_extracted": len(extracted),
            "fields": extracted,
        }

    @classmethod
    def extract_tables(cls, text: str) -> List[Dict[str, Any]]:
        """Detects and extracts tabular matrices formatted with pipe delimiters or regular whitespace column spacing."""
        lines = text.splitlines()
        tables = []
        current_table_lines = []

        for line in lines:
            # Check if line looks like a pipe table row or separator
            if "|" in line:
                current_table_lines.append(line)
            else:
                if len(current_table_lines) >= 2:
                    table_obj = cls._parse_table_block(current_table_lines)
                    if table_obj and table_obj.get("rows"):
                        tables.append(table_obj)
                current_table_lines = []

        if len(current_table_lines) >= 2:
            table_obj = cls._parse_table_block(current_table_lines)
            if table_obj and table_obj.get("rows"):
                tables.append(table_obj)

        return tables

    @classmethod
    def _parse_table_block(cls, lines: List[str]) -> Optional[Dict[str, Any]]:
        parsed_rows = []
        for line in lines:
            # Skip divider rows like |---|---|
            if re.match(r'^\s*\|?\s*[-:]+[-| :]+\s*\|?\s*$', line):
                continue
            cells = [c.strip() for c in line.split("|")]
            # Strip empty leading/trailing cells from outer pipes
            if cells and cells[0] == "":
                cells.pop(0)
            if cells and cells[-1] == "":
                cells.pop(-1)
            if cells:
                parsed_rows.append(cells)

        if len(parsed_rows) < 2:
            return None

        headers = parsed_rows[0]
        data_rows = parsed_rows[1:]

        structured_records = []
        for row in data_rows:
            record = {}
            for i, col_name in enumerate(headers):
                val = row[i] if i < len(row) else ""
                norm_col = re.sub(r'[^a-zA-Z0-9]+', '_', col_name.lower()).strip('_')
                record[norm_col or f"col_{i}"] = val
            structured_records.append(record)

        return {
            "columns": headers,
            "row_count": len(structured_records),
            "rows": structured_records,
        }

    @classmethod
    def chunk_document_by_sections(
        cls,
        text: str,
        max_chunk_size: int = 800,
    ) -> List[Dict[str, Any]]:
        """Splits document text along natural heading or keyword boundaries, respecting chunk limits."""
        lines = text.splitlines()
        chunks = []
        current_chunk_lines = []
        current_header = "Preamble"

        header_pattern = re.compile(r'^(?:SECTION\s+\d+.*|ARTICLE\s+[IVX]+.*|[A-Z\s]{4,}:?|\#{1,3}\s+.+)$', re.I)

        for line in lines:
            trimmed = line.strip()
            if header_pattern.match(trimmed) and len(trimmed) > 3 and not trimmed.startswith("|"):
                if current_chunk_lines:
                    chunk_text = "\n".join(current_chunk_lines).strip()
                    if chunk_text:
                        chunks.append({
                            "section": current_header,
                            "char_count": len(chunk_text),
                            "content": chunk_text,
                        })
                    current_chunk_lines = []
                current_header = trimmed
                continue

            current_chunk_lines.append(line)
            # If current chunk exceeds max_chunk_size, flush it
            if sum(len(l) for l in current_chunk_lines) >= max_chunk_size:
                chunk_text = "\n".join(current_chunk_lines).strip()
                chunks.append({
                    "section": current_header,
                    "char_count": len(chunk_text),
                    "content": chunk_text,
                })
                current_chunk_lines = []

        if current_chunk_lines:
            chunk_text = "\n".join(current_chunk_lines).strip()
            if chunk_text:
                chunks.append({
                    "section": current_header,
                    "char_count": len(chunk_text),
                    "content": chunk_text,
                })

        return chunks
