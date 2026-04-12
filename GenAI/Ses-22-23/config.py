<<<<<<< HEAD:GenAI/Ses-22-23/config.py
"""
Configuration module for RAG system.
Handles loading and validating environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for RAG system."""

    def __init__(self):
        # Neo4j
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "graphragdb")
        self.neo4j_instance = os.getenv("NEO4J_INSTANCE", "My_instance")

        # Gemini API
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Models
        # text-embedding-004 is deprecated (Jan 14 2026).
        # gemini-embedding-001 is the current GA replacement.
        # Requires the NEW SDK:  pip install google-genai
        self.embedding_model = "gemini-embedding-001"
        self.generation_model = "gemini-2.0-flash"

        # RAG settings
        self.chunk_min_length = 20
        self.top_k_results = 5
        self.max_retries = 3

        self._validate()

    def _validate(self):
        if not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD not found in environment variables")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

    def display_config(self):
        print("=" * 60)
        print("RAG System Configuration")
        print("=" * 60)
        print(f"Neo4j URI:        {self.neo4j_uri}")
        print(f"Neo4j User:       {self.neo4j_user}")
        print(f"Neo4j Database:   {self.neo4j_database}")
        print(f"Embedding Model:  {self.embedding_model}")
        print(f"Generation Model: {self.generation_model}")
        print(f"Chunk Min Length: {self.chunk_min_length}")
        print(f"Top K Results:    {self.top_k_results}")
=======
"""
Configuration module for RAG system.
Handles loading and validating environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for RAG system."""

    def __init__(self):
        # Neo4j
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "graphragdb")
        self.neo4j_instance = os.getenv("NEO4J_INSTANCE", "My_instance")

        # Gemini API
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Models
        # text-embedding-004 is deprecated (Jan 14 2026).
        # gemini-embedding-001 is the current GA replacement.
        # Requires the NEW SDK:  pip install google-genai
        self.embedding_model = "gemini-embedding-001"
        self.generation_model = "gemini-2.0-flash"

        # RAG settings
        self.chunk_min_length = 20
        self.top_k_results = 5
        self.max_retries = 5   # instead of 3

        self._validate()

    def _validate(self):
        if not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD not found in environment variables")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

    def display_config(self):
        print("=" * 60)
        print("RAG System Configuration")
        print("=" * 60)
        print(f"Neo4j URI:        {self.neo4j_uri}")
        print(f"Neo4j User:       {self.neo4j_user}")
        print(f"Neo4j Database:   {self.neo4j_database}")
        print(f"Embedding Model:  {self.embedding_model}")
        print(f"Generation Model: {self.generation_model}")
        print(f"Chunk Min Length: {self.chunk_min_length}")
        print(f"Top K Results:    {self.top_k_results}")
>>>>>>> c9cd86b (Update):Ses-22-23/config.py
        print("=" * 60)