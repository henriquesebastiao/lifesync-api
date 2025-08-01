from fastapi import status

from lifesync.schemas.utils import raises

CREATE_USER = {
    status.HTTP_409_CONFLICT: {
        'model': raises.EmailAlreadyExists,
    }
}

UPDATE_USER = {
    status.HTTP_404_NOT_FOUND: {
        'model': raises.UserDoesNotExists,
    },
    status.HTTP_409_CONFLICT: {
        'model': raises.EmailAlreadyExists,
    },
}

DELETE_USER = {
    status.HTTP_404_NOT_FOUND: {
        'model': raises.UserDoesNotExists,
    }
}
