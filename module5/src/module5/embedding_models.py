"""
Embedding Model Wrappers for Module 5 RAG System
Supports free sentence-transformers models
"""

from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedder:
    """
    Free embedding model using sentence-transformers
    Default: all-MiniLM-L6-v2 (384 dimensions, fast, good quality)
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize sentence-transformer embedding model
        
        Args:
            model_name: Model from sentence-transformers library
                - all-MiniLM-L6-v2: 384-dim, fast, good for general use
                - all-mpnet-base-v2: 768-dim, better quality, slower
                - paraphrase-multilingual: Supports Thai + English
            device: 'cuda', 'cpu', or None (auto-detect)
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
    def embed_text(self, text: str) -> List[float]:
        """
        Embed single text string
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_texts(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Embed multiple texts in batches
        
        Args:
            texts: List of input texts
            batch_size: Number of texts to process at once
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Return embedding vector dimension"""
        return self.embedding_dim
    
    def __repr__(self):
        return f"SentenceTransformerEmbedder(model={self.model_name}, dim={self.embedding_dim})"


class OpenAIEmbedder:
    """
    OpenAI embedding model (paid, better quality)
    Use this if you have OpenAI API key and budget
    """
    
    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize OpenAI embedding model
        
        Args:
            model_name: OpenAI embedding model
                - text-embedding-3-small: 1536-dim, $0.02/1M tokens
                - text-embedding-3-large: 3072-dim, $0.13/1M tokens
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Install openai: pip install openai")
        
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)
        self.embedding_dim = 1536 if "small" in model_name else 3072
        
    def embed_text(self, text: str) -> List[float]:
        """Embed single text"""
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return response.data[0].embedding
    
    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Embed multiple texts (OpenAI supports up to 8191 tokens per request)"""
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                input=batch,
                model=self.model_name
            )
            embeddings.extend([data.embedding for data in response.data])
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        return self.embedding_dim
    
    def __repr__(self):
        return f"OpenAIEmbedder(model={self.model_name}, dim={self.embedding_dim})"


def get_embedder(
    embedder_type: str = "sentence-transformers",
    model_name: Optional[str] = None,
    **kwargs
) -> SentenceTransformerEmbedder | OpenAIEmbedder:
    """
    Factory function to get embedding model
    
    Args:
        embedder_type: "sentence-transformers" or "openai"
        model_name: Specific model name (optional)
        **kwargs: Additional arguments for embedder
        
    Returns:
        Embedder instance
        
    Example:
        >>> embedder = get_embedder("sentence-transformers")
        >>> embedding = embedder.embed_text("Hello world")
        >>> len(embedding)
        384
    """
    if embedder_type == "sentence-transformers":
        model = model_name or "all-MiniLM-L6-v2"
        return SentenceTransformerEmbedder(model_name=model, **kwargs)
    
    elif embedder_type == "openai":
        model = model_name or "text-embedding-3-small"
        return OpenAIEmbedder(model_name=model, **kwargs)
    
    else:
        raise ValueError(f"Unknown embedder type: {embedder_type}")


if __name__ == "__main__":
    # Test embedder
    print("Testing SentenceTransformerEmbedder...")
    embedder = get_embedder("sentence-transformers")
    print(embedder)
    
    # Single text
    text = "AI Director is a one-man marketing agency powered by AI"
    embedding = embedder.embed_text(text)
    print(f"Text: {text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    
    # Multiple texts
    texts = [
        "Brand identity and visual design",
        "Content creation and strategy",
        "Marketing automation and analytics"
    ]
    embeddings = embedder.embed_texts(texts)
    print(f"\nEmbedded {len(embeddings)} texts")
    print(f"All embeddings have dimension: {len(embeddings[0])}")
