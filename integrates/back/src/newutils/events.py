from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.events.enums import (
    EventAccessibility,
    EventActionsAfterBlocking,
    EventActionsBeforeBlocking,
    EventAffectedComponents as AffectedComponents,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventState,
)
from dynamodb.types import (
    Item,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    cast,
)

MASKED: str = "Masked"
ACCESSIBILITY_MAP = {
    "Repositorio": EventAccessibility.REPOSITORY,
    "Ambiente": EventAccessibility.ENVIRONMENT,
    "VPN_CONNECTION": EventAccessibility.VPN_CONNECTION,
}
AFFECTED_COMPONENTS_MAP = {
    "Alteración del ToE": AffectedComponents.TOE_ALTERATION,
    "Código fuente": AffectedComponents.SOURCE_CODE,
    "Conectividad a Internet": AffectedComponents.INTERNET_CONNECTION,
    "Conectividad local (LAN, WiFi)": AffectedComponents.LOCAL_CONNECTION,
    "Conectividad VPN": AffectedComponents.VPN_CONNECTION,
    "Credenciales en el ToE": AffectedComponents.TOE_CREDENTIALS,
    "Datos de prueba": AffectedComponents.TEST_DATA,
    "Documentación del proyecto": AffectedComponents.DOCUMENTATION,
    "Estación de pruebas de FLUID": AffectedComponents.FLUID_STATION,
    "Estación de pruebas del Cliente": AffectedComponents.CLIENT_STATION,
    "Exclusión de alcance": AffectedComponents.TOE_EXCLUSSION,
    "Error en compilación": AffectedComponents.COMPILE_ERROR,
    "Inaccesibilidad del ToE": AffectedComponents.TOE_UNACCESSIBLE,
    "Indisponibilidad del ToE": AffectedComponents.TOE_UNAVAILABLE,
    "Inestabilidad del ToE": AffectedComponents.TOE_UNSTABLE,
    "Privilegios en el ToE": AffectedComponents.TOE_PRIVILEGES,
    "Otro(s)": AffectedComponents.OTHER,
    "Ubicación del ToE (IP, URL)": AffectedComponents.TOE_LOCATION,
}


def adjust_historic_dates(
    historic: tuple[EventState, ...],
) -> tuple[EventState, ...]:
    """Ensure dates are not the same and in ascending order."""
    new_historic = []
    comparison_date = ""
    for entry in historic:
        if entry.modified_date > comparison_date:
            comparison_date = entry.modified_date
        else:
            fixed_date = datetime.fromisoformat(comparison_date) + timedelta(
                seconds=1
            )
            comparison_date = fixed_date.astimezone(
                tz=timezone.utc
            ).isoformat()
        new_historic.append(entry._replace(modified_date=comparison_date))
    return tuple(new_historic)


def convert_to_iso_str(date_str: str) -> str:
    """
    From "%Y-%m-%d %H:%M:%S" or "%Y-%m-%d %H:%M"
    to "YYYY-MM-DDTHH:MM:SS+HH:MM".
    """
    date_format_alt: str = "%Y-%m-%d %H:%M"  # Present in old data
    if datetime_utils.is_valid_format(date_str, date_format_alt):
        datetime_ = datetime_utils.get_from_str(date_str, date_format_alt)
    else:
        datetime_ = datetime_utils.get_from_str(date_str)

    return datetime_utils.get_as_utc_iso_format(datetime_)


async def filter_events_date(
    events: list[dict[str, Any]],
    min_date: datetime,
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if min_date
        and datetime_utils.get_from_str(event["historic_state"][-1]["date"])
        >= min_date
    ]


def format_accessibility(accessibility: str) -> set[EventAccessibility]:
    return set(ACCESSIBILITY_MAP[item] for item in accessibility.split())


def format_accessibility_item(items: set[EventAccessibility]) -> str:
    map_reversed = {v: k for k, v in ACCESSIBILITY_MAP.items()}
    mapped_items = set(map_reversed[item] for item in items)
    return " ".join(mapped_items)


def format_actions_after_blocking(action: str) -> EventActionsAfterBlocking:
    if action == "EXECUTE_OTHER_PROJECT_OTHER_CLIENT":
        return EventActionsAfterBlocking.EXECUTE_OTHER_GROUP_OTHER_CLIENT
    if action == "EXECUTE_OTHER_PROJECT_SAME_CLIENT":
        return EventActionsAfterBlocking.EXECUTE_OTHER_GROUP_SAME_CLIENT
    return EventActionsAfterBlocking[action]


def format_actions_before_blocking(action: str) -> EventActionsBeforeBlocking:
    if action == "DOCUMENT_PROJECT":
        return EventActionsBeforeBlocking.DOCUMENT_GROUP
    return EventActionsBeforeBlocking[action]


def format_affected_components(
    affected_components: str,
) -> set[AffectedComponents]:
    components_list = affected_components.split("\n")
    return set(AFFECTED_COMPONENTS_MAP[item] for item in components_list)


def format_affected_components_item(
    items: set[AffectedComponents],
) -> str:
    map_reversed = {v: k for k, v in AFFECTED_COMPONENTS_MAP.items()}
    mapped_items = set(map_reversed[item] for item in items)
    return "\n".join(mapped_items)


def format_data(event: dict[str, Any]) -> dict[str, Any]:
    historic_state = cast(
        list[dict[str, str]], event.get("historic_state", [{}, {}])
    )
    event["closing_date"] = "-"
    if historic_state[-1].get("state") == "SOLVED":
        event["closing_date"] = historic_state[-2].get("date", "")

    return event


def format_evidences(item: Item) -> EventEvidences:
    evidence_file = (
        EventEvidence(
            file_name=item["evidence_file"],
            modified_date=convert_to_iso_str(item["evidence_file_date"])
            if item["evidence_file_date"] != MASKED
            else MASKED,
        )
        if item.get("evidence_file") and item.get("evidence_file_date")
        else None
    )
    evidence_image = (
        EventEvidence(
            file_name=item["evidence"],
            modified_date=convert_to_iso_str(item["evidence_date"])
            if item["evidence_date"] != MASKED
            else MASKED,
        )
        if item.get("evidence") and item.get("evidence_date")
        else None
    )
    return EventEvidences(
        file=evidence_file,
        image=evidence_image,
    )


def format_historic_state(item: Item) -> tuple[EventState, ...]:
    historic_state = item["historic_state"]
    return tuple(
        EventState(
            modified_by=state["analyst"],
            modified_date=convert_to_iso_str(state["date"]),
            status=EventStateStatus[state["state"]],
        )
        for state in historic_state
    )


def format_state_item(state: EventState) -> Item:
    return {
        "analyst": state.modified_by,
        "date": datetime_utils.convert_from_iso_str(state.modified_date),
        "state": state.status.value,
    }


def format_type(event_type: str) -> EventType:
    if event_type in {
        "CLIENT_APPROVES_CHANGE_TOE",
        "CLIENT_EXPLICITLY_SUSPENDS_PROJECT",
        "CLIENT_CANCELS_PROJECT_MILESTONE",
        "CLIENT_DETECTS_ATTACK",
        "HIGH_AVAILABILITY_APPROVAL",
    }:
        return EventType.OTHER
    return EventType[event_type]


def format_event(item: Item) -> Event:
    report_date = convert_to_iso_str(item["historic_state"][0]["date"])
    historic_state = format_historic_state(item)
    return Event(
        action_after_blocking=format_actions_after_blocking(
            item["action_after_blocking"]
        )
        if item.get("action_after_blocking")
        else None,
        action_before_blocking=format_actions_before_blocking(
            item["action_before_blocking"]
        )
        if item.get("action_before_blocking")
        else None,
        accessibility=format_accessibility(item["accessibility"])
        if item.get("accessibility")
        else None,
        affected_components=format_affected_components(
            item["affected_components"]
        )
        if item.get("affected_components")
        else None,
        client=item.get("client", ""),
        context=item.get("context"),
        description=item["detail"],
        evidences=format_evidences(item),
        group_name=item["project_name"],
        hacker=item["analyst"],
        id=item["event_id"],
        report_date=report_date,
        root_id=item.get("root_id"),
        state=historic_state[-1],
        type=format_type(item.get("event_type", "OTHER")),
    )


def format_event_item(event: Event) -> Item:
    item = {
        "action_after_blocking": event.action_after_blocking,
        "action_before_blocking": event.action_before_blocking,
        "accessibility": format_accessibility_item(event.accessibility)
        if event.accessibility
        else None,
        "affected_components": format_affected_components_item(
            event.affected_components
        )
        if event.affected_components
        else None,
        "client": event.client,
        "context": event.context,
        "detail": event.description,
        "project_name": event.group_name,
        "analyst": event.hacker,
        "event_id": event.id,
        "root_id": event.root_id,
        "historic_state": [format_state_item(event.state)],
        "event_type": event.type.value,
    }
    if event.evidences.image:
        item["evidence"] = event.evidences.image.file_name
        item["evidence_date"] = datetime_utils.convert_from_iso_str(
            event.evidences.image.modified_date
        )
    if event.evidences.file:
        item["evidence_file"] = event.evidences.file.file_name
        item["evidence_file_date"] = datetime_utils.convert_from_iso_str(
            event.evidences.file.modified_date
        )

    return item
