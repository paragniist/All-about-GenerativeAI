"""
PDF processing module using pypdfium2 directly.
Bypasses Docling's ML pipeline entirely to avoid the
'Unable to create tensor / padding=True' batching error.
"""

import re
from pathlib import Path
from typing import List, Dict, Any

import pypdfium2 as pdfium


class PDFProcessor:
    """Class for processing PDF documents and extracting chunks."""

    def __init__(self, min_chunk_length: int = 50):
        """
        Initialize PDF processor.

        Args:
            min_chunk_length: Minimum character length for a chunk to be kept.
        """
        self.min_chunk_length = min_chunk_length
        print("📄 Initialized PDF Processor (pypdfium2 direct — no ML models)")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text chunks from a PDF file.

        Strategy
        --------
        1. Open the PDF with pypdfium2 (pure C library, zero ML).
        2. Extract the text layer from every page.
        3. Split on blank lines to get paragraph-level chunks.
        4. Filter out chunks shorter than min_chunk_length.

        Args:
            pdf_path: Absolute or relative path to the PDF file.

        Returns:
            List of chunk dicts ready for embedding and storage.
        """
        print(f"📄 Extracting content from: {pdf_path}")

        pdf = pdfium.PdfDocument(pdf_path)
        page_texts: List[str] = []

        try:
            for page_index in range(len(pdf)):
                page = pdf[page_index]
                textpage = page.get_textpage()
                text = textpage.get_text_range()
                page_texts.append(text)
        finally:
            pdf.close()

        # Join all pages with a double newline so paragraph splitting works
        # across page boundaries naturally.
        full_text = "\n\n".join(page_texts)
        print(f"📝 Extracted {len(full_text):,} characters from {len(page_texts)} pages")

        chunks = self._split_into_chunks(full_text, pdf_path)

        print(f"✅ Extracted {len(chunks)} chunks from PDF")

        if not chunks:
            print("⚠️  WARNING: No chunks extracted!")
            print(f"   Min chunk length: {self.min_chunk_length}")
            print("   Try reducing chunk_min_length in config.py")
            print("   Or verify the PDF contains a selectable text layer")

        return chunks

    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute basic statistics over the extracted chunks.

        Args:
            chunks: Output of extract_chunks().

        Returns:
            Dict with total_chunks, total_chars, avg/min/max chunk sizes.
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_chars": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0,
            }

        sizes = [c["metadata"]["length"] for c in chunks]
        total = sum(sizes)

        return {
            "total_chunks": len(chunks),
            "total_chars": total,
            "avg_chunk_size": round(total / len(chunks), 2),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_into_chunks(
        self, full_text: str, pdf_path: str
    ) -> List[Dict[str, Any]]:
        """
        Split raw text into paragraph-level chunks.

        Paragraphs are separated by one or more blank lines. Very short
        paragraphs (headers, page numbers, stray whitespace) are dropped.

        Args:
            full_text: Complete text extracted from the PDF.
            pdf_path:  Original PDF path (used to build chunk IDs and source).

        Returns:
            List of chunk dicts.
        """
        stem = Path(pdf_path).stem
        source_name = Path(pdf_path).name

        # Normalise line endings, then split on blank lines
        normalised = full_text.replace("\r\n", "\n").replace("\r", "\n")
        raw_paragraphs = re.split(r"\n{2,}", normalised)

        chunks: List[Dict[str, Any]] = []
        chunk_id = 0

        for para in raw_paragraphs:
            # Collapse internal whitespace / lone newlines within a paragraph
            text = re.sub(r"[ \t]+", " ", para).strip()
            text = re.sub(r"\n+", " ", text)

            if text and len(text) >= self.min_chunk_length:
                chunks.append(
                    {
                        "id": f"{stem}_chunk_{chunk_id}",
                        "text": text,
                        "source": source_name,
                        "chunk_index": chunk_id,
                        "metadata": {
                            "length": len(text),
                            "extraction_method": "pypdfium2",
                        },
                    }
                )
                chunk_id += 1

        return chunks