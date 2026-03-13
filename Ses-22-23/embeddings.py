"""
Embedding generation module using Google Gemini.
Handles text-to-vector conversion with retry logic.

Uses the NEW google-genai SDK (google-genai package).
Install with: pip install google-genai

Do NOT use the old google-generativeai package — it calls the v1beta
endpoint which no longer supports the current embedding models.
"""

import time
import random
import re
from typing import List
from google import genai
from google.genai import types


# Gemini free tier: 1,500 requests/minute for gemini-embedding-001.
# That's very generous, but we still add a tiny gap to be safe.
_MIN_SECONDS_BETWEEN_CALLS = 0.1   # 1500 RPM → well under limit


class EmbeddingGenerator:
    """Class for generating embeddings using Gemini API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-embedding-001",
        max_retries: int = 5,
    ):
        """
        Initialize embedding generator.

        Args:
            api_key:     Gemini API key.
            model:       Embedding model to use.
            max_retries: Max retries on rate-limit errors.
        """
        self.model = model
        self.max_retries = max_retries
        self._last_call_ts: float = 0.0

        self.client = genai.Client(api_key=api_key)
        print(f"🤖 Initialized Gemini Embedding Model: {self.model}")

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def generate_document_embedding(self, document: str) -> List[float]:
        """Generate embedding for a document chunk."""
        return self._generate(document, task_type="RETRIEVAL_DOCUMENT")

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        return self._generate(query, task_type="RETRIEVAL_QUERY")

    # kept for backwards-compat with any direct callers
    def generate(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        return self._generate(text, task_type)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _generate(self, text: str, task_type: str) -> List[float]:
        """
        Call the Gemini embedding API with proactive throttling and
        exponential-backoff retry on 429 / quota errors.
        """
        for attempt in range(self.max_retries):
            self._throttle()

            try:
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                    config=types.EmbedContentConfig(task_type=task_type),
                )
                self._last_call_ts = time.monotonic()
                # result.embeddings is a list of ContentEmbedding objects
                return result.embeddings[0].values

            except Exception as e:
                err = str(e)
                if not self._is_rate_limit(err):
                    print(f"❌ Embedding error: {err}")
                    raise

                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        f"❌ Rate limit exceeded after {self.max_retries} retries. "
                        "Wait ~60 seconds and try again, or switch to a paid API key."
                    ) from e

                wait   = self._parse_retry_after(err) or min(15 * (2 ** attempt), 120)
                jitter = wait * random.uniform(-0.1, 0.1)
                total  = round(wait + jitter)
                print(
                    f"⏳ Embedding rate limit (attempt {attempt + 1}/{self.max_retries}). "
                    f"Waiting {total}s…"
                )
                time.sleep(total)
                self._last_call_ts = time.monotonic()

    def _throttle(self):
        elapsed = time.monotonic() - self._last_call_ts
        gap = _MIN_SECONDS_BETWEEN_CALLS - elapsed
        if gap > 0:
            time.sleep(gap)

    @staticmethod
    def _is_rate_limit(err: str) -> bool:
        low = err.lower()
        return (
            "429"                   in err
            or "quota"              in low
            or "rate"               in low
            or "resource_exhausted" in low
        )

    @staticmethod
    def _parse_retry_after(err: str):
        m = re.search(r"retry[_\s-]*after[:\s]+(\d+)", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        m = re.search(r"(\d+)\s*seconds?", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        return None