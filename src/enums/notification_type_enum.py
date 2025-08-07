from enum import StrEnum


class NotificationTypeEnum(StrEnum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'
