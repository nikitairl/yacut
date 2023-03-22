import re

from . import constants
from .error_handlers import InvalidAPIUsage
from .models import URLMap

DATA_VALIDATORS = {
    lambda data: (not data): (constants.MISSING_REQUEST_BODY),
    lambda data: ("url" not in data): (constants.URL_IS_REQUIRED_FIELD),
}

CUSTOM_ID_VALIDATORS = {
    lambda custom_id: (len(custom_id) > 6): (constants.INVALID_SHORT_LINK),
    lambda custom_id: (re.match(constants.REGEX, custom_id) is None): (
        constants.INVALID_SHORT_LINK
    ),
    lambda custom_id: (not URLMap.available_short(custom_id)): (
        constants.ALREADY_TAKEN
    ),
}


def validation(data):
    data = data
    for validator, message in DATA_VALIDATORS.items():
        if validator(data):
            raise InvalidAPIUsage(message)


def custom_id_validation(data):
    custom_id = data.get("custom_id")
    if custom_id is None:
        custom_id = URLMap.get_unique_short_id()
    for validator, message in CUSTOM_ID_VALIDATORS.items():
        if validator(custom_id):
            raise InvalidAPIUsage(message.format(custom_id))
    return custom_id
