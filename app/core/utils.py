"""
Utility functions for the application.

This module contains helper functions used across the application.
"""

import re
import unicodedata


def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from text.
    
    Converts text to lowercase, removes accents, replaces spaces with hyphens,
    and removes any characters that are not alphanumeric or hyphens.
    
    Args:
        text: The text to convert to a slug
        
    Returns:
        URL-friendly slug string
        
    Examples:
        >>> generate_slug("My Awesome Project")
        'my-awesome-project'
        >>> generate_slug("Análise de Dados")
        'analise-de-dados'
        >>> generate_slug("Project #1: Data Engineering")
        'project-1-data-engineering'
    """
    # Normalize unicode characters (remove accents)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    
    # Remove any character that is not alphanumeric or hyphen
    text = re.sub(r'[^a-z0-9-]', '', text)
    
    # Replace multiple consecutive hyphens with a single hyphen
    text = re.sub(r'-+', '-', text)
    
    # Remove leading and trailing hyphens
    text = text.strip('-')
    
    return text
