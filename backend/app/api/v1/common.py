from fastapi import HTTPException, status


def not_implemented(feature: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"{feature}: aún no implementado.",
    )
