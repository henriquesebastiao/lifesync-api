from fastapi import HTTPException, status


class NotEnoughPermissions(HTTPException):
    def __init__(self, detail: str = 'Not enough permission'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
