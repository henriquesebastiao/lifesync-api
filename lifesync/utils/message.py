from enum import Enum


class AlreadyExists(str, Enum):
    __complement = ' already exists'

    EMAIL = 'Email' + __complement
    QUOTE = 'Quote' + __complement


class DoesNotExist(str, Enum):
    __complement = ' does not exist'

    USER = 'User' + __complement
    ACCOUNT = 'Account' + __complement
    QUOTE = 'Quote' + __complement
