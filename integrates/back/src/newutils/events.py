from datetime import (
    datetime,
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
from newutils.datetime import (
    convert_to_iso_str,
)
from typing import (
    Any,
    cast,
)


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


def format_data(event: dict[str, Any]) -> dict[str, Any]:
    historic_state = cast(
        list[dict[str, str]], event.get("historic_state", [{}, {}])
    )
    event["closing_date"] = "-"
    if historic_state[-1].get("state") == "SOLVED":
        event["closing_date"] = historic_state[-2].get("date", "")

    return event


def format_accessibility(accessibility: str) -> set[EventAccessibility]:
    return set(
        EventAccessibility.REPOSITORY
        if item == "Repositorio"
        else EventAccessibility.ENVIRONMENT
        for item in accessibility.split()
        if item in {"Repositorio", "Ambiente"}
    )


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
    affected_components_map = {
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

    components_list = affected_components.split("\n")
    return set(affected_components_map[item] for item in components_list)


def format_evidences(item: Item) -> EventEvidences:
    evidence_file = (
        EventEvidence(
            file_name=item["evidence_file"],
            modified_date=convert_to_iso_str(item["evidence_file_date"]),
        )
        if item.get("evidence_file") and item.get("evidence_file_date")
        else None
    )
    evidence_image = (
        EventEvidence(
            file_name=item["evidence"],
            modified_date=convert_to_iso_str(item["evidence_date"]),
        )
        if item.get("evidence") and item.get("evidence_date")
        else None
    )
    return EventEvidences(
        file=evidence_file,
        image=evidence_image,
    )


def format_state(item: Item) -> EventState:
    historic_state = item["historic_state"]
    last_state = historic_state[-1]
    return EventState(
        modified_by=last_state["analyst"],
        modified_date=last_state["date"],
        status=EventStateStatus[last_state["state"]],
    )


def format_event(item: Item) -> Event:
    report_date = convert_to_iso_str(item["historic_state"][0]["date"])
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
        state=format_state(item),
        type=EventType[item["event_type"]],
    )
