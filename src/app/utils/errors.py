class AppError(Exception):
    """Base exception type for the application."""


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass
