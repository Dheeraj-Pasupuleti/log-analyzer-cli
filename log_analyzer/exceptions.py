class LogAnalyzerError(Exception):
    """Base exception for all log-analyzer errors."""


class FileNotFoundError(LogAnalyzerError):
    """Raised when the requested log file does not exist."""


class InvalidLogLevelError(LogAnalyzerError):
    """Raised when an invalid log level is supplied."""


class InvalidDateFormatError(LogAnalyzerError):
    """Raised when a date is invalid or the range is reversed."""


class MalformedLineError(LogAnalyzerError):
    """Raised when a log line cannot be parsed."""
