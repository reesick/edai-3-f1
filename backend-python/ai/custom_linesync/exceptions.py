"""
Custom exceptions for LineSync AI service.
"""


class GeminiServiceError(Exception):
    """Exception raised when Gemini API calls fail"""
    pass


class ValidationFailedError(Exception):
    """Exception raised when response validation fails"""
    pass
