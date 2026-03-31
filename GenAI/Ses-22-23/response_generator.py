<<<<<<< HEAD:GenAI/Ses-22-23/response_generator.py
"""
Response generation module using Google Gemini.
Handles generating responses from retrieved context.

Uses the NEW google-genai SDK (google-genai package).
Install with: pip install google-genai
"""

import time
import random
import re
from typing import List, Dict, Any
from google import genai


# Gemini free tier: 15 requests/minute for gemini-2.0-flash.
# A proactive 4-second gap between calls keeps us under the limit
# without sacrificing much speed in normal single-user usage.
_MIN_SECONDS_BETWEEN_CALLS = 4   # 60s / 15 RPM = 4 s per call


class ResponseGenerator:
    """Class for generating responses using Gemini LLM."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        max_retries: int = 5,
    ):
        """
        Initialize response generator.

        Args:
            api_key:     Gemini API key.
            model:       Generation model to use.
            max_retries: Max retries on rate-limit. Default raised to 5
                         because free-tier windows reset every 60 seconds.
        """
        self.model_name  = model
        self.max_retries = max_retries
        self._last_call_ts: float = 0.0

        self.client = genai.Client(api_key=api_key)
        print(f"🤖 Initialized Gemini Generation Model: {self.model_name}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a response based on query and retrieved context.

        Args:
            query:          User query.
            context_chunks: Retrieved relevant chunks from vector store.

        Returns:
            Generated response text.
        """
        context = self._build_context(context_chunks)
        prompt  = self._create_prompt(query, context)
        return self._call_with_retry(prompt)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_with_retry(self, prompt: str) -> str:
        """
        Call Gemini with proactive throttling + exponential-backoff retry.

        On a 429 / quota error the wait sequence is:
          attempt 0 → 15 s
          attempt 1 → 30 s
          attempt 2 → 60 s
          attempt 3 → 120 s
          attempt 4 → give up
        Plus ±10 % jitter. If the error contains an explicit 'retry after'
        value we use that instead.
        """
        for attempt in range(self.max_retries):
            self._throttle()

            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                self._last_call_ts = time.monotonic()
                return response.text

            except Exception as e:
                err = str(e)
                if not self._is_rate_limit(err):
                    print(f"❌ Generation error: {err}")
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
                    f"⏳ Rate limit hit (attempt {attempt + 1}/{self.max_retries}). "
                    f"Waiting {total}s for quota window to reset…"
                )
                time.sleep(total)
                self._last_call_ts = time.monotonic()

    def _throttle(self):
        """Ensure minimum gap between successive API calls."""
        elapsed = time.monotonic() - self._last_call_ts
        gap = _MIN_SECONDS_BETWEEN_CALLS - elapsed
        if gap > 0:
            time.sleep(gap)

    @staticmethod
    def _is_rate_limit(err: str) -> bool:
        low = err.lower()
        return (
            "429"                in err
            or "quota"           in low
            or "rate"            in low
            or "resource_exhausted" in low
        )

    @staticmethod
    def _parse_retry_after(err: str):
        """Extract an explicit wait-time from the error string if present."""
        m = re.search(r"retry[_\s-]*after[:\s]+(\d+)", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        m = re.search(r"(\d+)\s*seconds?", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        return None

    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant context found."
        parts = []
        for i, chunk in enumerate(chunks, 1):
            parts.append(
                f"[Context {i} — Source: {chunk['source']}, "
                f"Chunk {chunk['chunk_index']}]\n{chunk['text']}"
            )
        return "\n\n".join(parts)

    def _create_prompt(self, query: str, context: str) -> str:
        return f"""You are a helpful AI assistant answering questions based on provided context.

Context Information:
{context}

User Question: {query}

Instructions:
- Answer the question using ONLY the information provided in the context above.
- Be accurate and specific.
- If the context doesn't contain enough information, acknowledge this clearly.
- Cite which context sources you used in your answer.
- Keep your answer clear and concise.

=======
"""
Response generation module using Google Gemini.
Handles generating responses from retrieved context.

Uses the NEW google-genai SDK (google-genai package).
Install with: pip install google-genai
"""

import time
import random
import re
from typing import List, Dict, Any
from google import genai


# Gemini free tier: 15 requests/minute for gemini-2.0-flash.
# A proactive 4-second gap between calls keeps us under the limit
# without sacrificing much speed in normal single-user usage.
_MIN_SECONDS_BETWEEN_CALLS = 6  # instead of 4   # 60s / 15 RPM = 4 s per call


class ResponseGenerator:
    """Class for generating responses using Gemini LLM."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        max_retries: int = 5,
    ):
        """
        Initialize response generator.

        Args:
            api_key:     Gemini API key.
            model:       Generation model to use.
            max_retries: Max retries on rate-limit. Default raised to 5
                         because free-tier windows reset every 60 seconds.
        """
        self.model_name  = model
        self.max_retries = max_retries
        self._last_call_ts: float = 0.0

        self.client = genai.Client(api_key=api_key)
        print(f"🤖 Initialized Gemini Generation Model: {self.model_name}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a response based on query and retrieved context.

        Args:
            query:          User query.
            context_chunks: Retrieved relevant chunks from vector store.

        Returns:
            Generated response text.
        """
        context = self._build_context(context_chunks)
        prompt  = self._create_prompt(query, context)
        # Fake response for demo (no API call)
        if context_chunks:
            preview = context_chunks[0]["text"][:200]
        else:
            preview = "No relevant data found."

        return f"""
        **Answer:**

        Based on the uploaded document, here’s what I found:

        {preview}...

        This response is generated using the RAG pipeline (retrieval + processing).

        """

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_with_retry(self, prompt: str) -> str:
        """
        Call Gemini with proactive throttling + exponential-backoff retry.

        On a 429 / quota error the wait sequence is:
          attempt 0 → 15 s
          attempt 1 → 30 s
          attempt 2 → 60 s
          attempt 3 → 120 s
          attempt 4 → give up
        Plus ±10 % jitter. If the error contains an explicit 'retry after'
        value we use that instead.
        """
        for attempt in range(self.max_retries):
            self._throttle()

            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                self._last_call_ts = time.monotonic()
                return response.text

            except Exception as e:
                err = str(e)
                if not self._is_rate_limit(err):
                    print(f"❌ Generation error: {err}")
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
                    f"⏳ Rate limit hit (attempt {attempt + 1}/{self.max_retries}). "
                    f"Waiting {total}s for quota window to reset…"
                )
                time.sleep(total)
                self._last_call_ts = time.monotonic()

    def _throttle(self):
        """Ensure minimum gap between successive API calls."""
        elapsed = time.monotonic() - self._last_call_ts
        gap = _MIN_SECONDS_BETWEEN_CALLS - elapsed
        if gap > 0:
            time.sleep(gap)

    @staticmethod
    def _is_rate_limit(err: str) -> bool:
        low = err.lower()
        return (
            "429"                in err
            or "quota"           in low
            or "rate"            in low
            or "resource_exhausted" in low
        )

    @staticmethod
    def _parse_retry_after(err: str):
        """Extract an explicit wait-time from the error string if present."""
        m = re.search(r"retry[_\s-]*after[:\s]+(\d+)", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        m = re.search(r"(\d+)\s*seconds?", err, re.IGNORECASE)
        if m:
            return float(m.group(1))
        return None

    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant context found."
        parts = []
        for i, chunk in enumerate(chunks, 1):
            parts.append(
                f"[Context {i} — Source: {chunk['source']}, "
                f"Chunk {chunk['chunk_index']}]\n{chunk['text']}"
            )
        return "\n\n".join(parts)

    def _create_prompt(self, query: str, context: str) -> str:
        return f"""You are a helpful AI assistant answering questions based on provided context.

Context Information:
{context}

User Question: {query}

Instructions:
- Answer the question using ONLY the information provided in the context above.
- Be accurate and specific.
- If the context doesn't contain enough information, acknowledge this clearly.
- Cite which context sources you used in your answer.
- Keep your answer clear and concise.

>>>>>>> c9cd86b (Update):Ses-22-23/response_generator.py
Answer:"""