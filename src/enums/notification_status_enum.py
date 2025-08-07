from enum import StrEnum


class NotificationStatusEnum(StrEnum):
    FINAL_DELIVERY_FAILURE = 'final_delivery_failure'
    FINAL_REPROCESSING_FAILURE = 'final_reprocessing_failure'
    INITIAL_PROCESSING_FAILURE = 'initial_processing_failure'
    INTERMEDIATE_PROCESSED = 'intermediate_processed'
    RECEIVED = 'received'
    REPROCESSED_SUCCESSFULLY = 'reprocessed_successfully'
    SENT_SUCCESS = 'sent_success'
