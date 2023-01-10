from amazon_kclpy.kcl import (
    Checkpointer,
    CheckpointError,
    KCLProcess,
)
from amazon_kclpy.messages import (
    InitializeInput,
    ProcessRecordsInput,
    Record as KCLRecord,
    ShutdownInput,
)
from amazon_kclpy.v2 import (
    processor,
)
from dynamodb.triggers import (
    TRIGGERS,
)
from dynamodb.utils import (
    format_record,
)
import json
import logging
from time import (
    sleep,
)
from typing import (
    Optional,
)

LOGGER = logging.getLogger(__name__)


class RecordProcessor(processor.RecordProcessorBase):
    def __init__(self) -> None:
        self.checkpoint_retries = 5
        self.sleep_seconds = 5

    def initialize(self, _initialize_input: InitializeInput) -> None:
        """Called by the KCL when the worker has been instanced"""

    def checkpoint(
        self,
        checkpointer: Checkpointer,
        sequence_number: Optional[str] = None,
        sub_sequence_number: Optional[int] = None,
    ) -> None:
        """Keep track of progress so the KCL can pick up from there later"""
        retries = 0

        while retries < self.checkpoint_retries:
            try:
                checkpointer.checkpoint(sequence_number, sub_sequence_number)
                return
            except CheckpointError as ex:
                if ex.value == "ShutdownException":
                    LOGGER.info("Shutting down, skipping checkpoint.")
                    return

                if ex.value == "ThrottlingException":
                    LOGGER.info(
                        "Checkpoint throttled, waiting %s seconds.",
                        self.sleep_seconds,
                    )
                else:
                    LOGGER.exception(ex)

            retries += 1
            sleep(self.sleep_seconds)

        LOGGER.error(
            "Couldn't checkpoint after %s retries", self.checkpoint_retries
        )

    def process_records(
        self, process_records_input: ProcessRecordsInput
    ) -> None:
        """Called by the KCL when new records are read from the stream"""
        kcl_records: list[KCLRecord] = process_records_input.records
        records = tuple(
            format_record(json.loads(record.binary_data.decode("utf-8")))
            for record in kcl_records
        )

        for trigger in TRIGGERS:
            matching_records = tuple(
                record for record in records if trigger.records_filter(record)
            )

            if matching_records:
                try:
                    trigger.records_processor(matching_records)
                # Must keep going even if one processor fails
                # pylint: disable-next=broad-except
                except Exception as ex:
                    LOGGER.exception(
                        ex,
                        extra={
                            "extra": {
                                "matching_records": {
                                    record.sequence_number: record
                                    for record in matching_records
                                },
                                "trigger": trigger.records_processor.__name__,
                            }
                        },
                    )

        self.checkpoint(
            process_records_input.checkpointer,
            kcl_records[-1].sequence_number,
            kcl_records[-1].sub_sequence_number,
        )

    def shutdown(self, shutdown_input: ShutdownInput) -> None:
        """Called by the KCL when the worker will shutdown"""
        if shutdown_input.reason == "TERMINATE":
            self.checkpoint(shutdown_input.checkpointer)


def consume() -> None:
    """Consumes the DynamoDB stream"""
    try:
        kclprocess = KCLProcess(RecordProcessor())
        kclprocess.run()
    except KeyboardInterrupt:
        LOGGER.info("Shutting down")

    LOGGER.info("Stream consumption completed.")
