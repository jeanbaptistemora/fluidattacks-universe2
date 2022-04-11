# pylint: disable=too-many-lines
# pylint: disable=invalid-name
from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)


class Platform(Enum):
    NPM: str = "NPM"
    MAVEN: str = "MAVEN"
    NUGET: str = "NUGET"


class Grammar(Enum):
    JAVA9: str = "Java9"
    SCALA: str = "Scala"


class AvailabilityEnum(Enum):
    ALWAYS = "ALWAYS"
    WORKING_HOURS = "WORKING_HOURS"
    NEVER = "NEVER"


class ExecutionQueueConfig(NamedTuple):
    availability: AvailabilityEnum
    name: str


class LocalesEnum(Enum):
    EN: str = "EN"
    ES: str = "ES"


class ExecutionQueue(Enum):
    apk = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="apk"
    )
    cloud = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="cloud"
    )
    control = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="control"
    )
    cookie = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="cookie"
    )
    crypto = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="crypto"
    )
    f014 = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="f014"
    )
    f117 = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="f117"
    )
    http = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="http"
    )
    injection = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="injection"
    )
    leak = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="leak"
    )
    none = ExecutionQueueConfig(
        availability=AvailabilityEnum.NEVER, name="none"
    )
    sca = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sca"
    )
    sql = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sql"
    )
    ssl = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="ssl"
    )
    xss = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="xss"
    )


if len(ExecutionQueue) > 20:
    # We can have at most 20 items in this Enum
    # Each item in this Enum represents 2 queues:
    #   Soon (urgent): used for re-attacks
    #   Later (non-urgent): is used for periodic executions
    # Batch has a limit of 50 queues, 10 for other products
    # https://docs.aws.amazon.com/batch/latest/userguide/service_limits.html
    raise AssertionError("We can't allocate so many queues")


class FindingMetadata(NamedTuple):
    auto_approve: bool
    cwe: int
    description: str
    execution_queue: ExecutionQueue
    impact: str
    recommendation: str
    requirements: List[int]
    threat: str
    title: str

    @classmethod
    def new(
        cls,
        *,
        code: str,
        cwe: int,
        execution_queue: ExecutionQueue,
        auto_approve: bool,
        requirements: List[int],
    ) -> FindingMetadata:
        return FindingMetadata(
            auto_approve=auto_approve,
            cwe=cwe,
            description=f"criteria.vulns.{code[1:]}.description",
            execution_queue=execution_queue,
            impact=f"criteria.vulns.{code[1:]}.impact",
            recommendation=f"criteria.vulns.{code[1:]}.recommendation",
            requirements=requirements,
            threat=f"criteria.vulns.{code[1:]}.threat",
            title=f"criteria.vulns.{code[1:]}.title",
        )


class FindingEnum(Enum):
    F001: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F001",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
    )
    F004: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F004",
        cwe=78,
        execution_queue=ExecutionQueue.injection,
        requirements=[173, 265],
    )
    F008: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F008",
        cwe=79,
        execution_queue=ExecutionQueue.xss,
        requirements=[173],
    )
    F009: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F009",
        cwe=798,
        execution_queue=ExecutionQueue.leak,
        requirements=[156],
    )
    F010: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F010",
        cwe=79,
        execution_queue=ExecutionQueue.xss,
        requirements=[29, 173],
    )
    F011: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F011",
        cwe=937,
        execution_queue=ExecutionQueue.sca,
        requirements=[262],
    )
    F012: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F012",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
    )
    F015: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F015",
        cwe=287,
        execution_queue=ExecutionQueue.http,
        requirements=[228, 319],
    )
    F016: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F016",
        cwe=326,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
    )
    F017: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F017",
        cwe=319,
        execution_queue=ExecutionQueue.http,
        requirements=[32, 181],
    )
    F020: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F020",
        cwe=311,
        execution_queue=ExecutionQueue.crypto,
        requirements=[134, 135, 185, 229, 264, 300],
    )
    F021: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F021",
        cwe=643,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
    )
    F022: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F022",
        cwe=319,
        execution_queue=ExecutionQueue.f014,
        requirements=[181],
    )
    F023: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F023",
        cwe=601,
        execution_queue=ExecutionQueue.http,
        requirements=[173, 324],
    )
    F024: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F024",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[255, 266],
    )
    F031: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F031",
        cwe=250,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186],
    )
    F034: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F034",
        cwe=330,
        execution_queue=ExecutionQueue.crypto,
        requirements=[223, 224],
    )
    F035: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F035",
        cwe=521,
        execution_queue=ExecutionQueue.f014,
        requirements=[130, 132, 133, 139, 332],
    )
    F036: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F036",
        cwe=319,
        execution_queue=ExecutionQueue.http,
        requirements=[26],
    )
    F042: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F042",
        cwe=614,
        execution_queue=ExecutionQueue.cookie,
        requirements=[29],
    )
    F043: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
    )
    F046: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F046",
        cwe=1269,
        execution_queue=ExecutionQueue.apk,
        requirements=[159],
    )
    F048: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F048",
        cwe=250,
        execution_queue=ExecutionQueue.apk,
        requirements=[326],
    )
    F052: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F052",
        cwe=310,
        execution_queue=ExecutionQueue.crypto,
        requirements=[158, 149, 150, 181, 336],
    )
    F055: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F055",
        cwe=530,
        execution_queue=ExecutionQueue.apk,
        requirements=[266],
    )
    F056: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F056",
        cwe=284,
        execution_queue=ExecutionQueue.control,
        requirements=[142, 264, 265, 266, 319],
    )
    F058: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F058",
        cwe=489,
        execution_queue=ExecutionQueue.apk,
        requirements=[77, 78],
    )
    F060: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F060",
        cwe=396,
        execution_queue=ExecutionQueue.none,
        requirements=[359],
    )
    F061: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F061",
        cwe=390,
        execution_queue=ExecutionQueue.none,
        requirements=[75],
    )
    F063: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F063",
        cwe=22,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
    )
    F064: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F064",
        cwe=778,
        execution_queue=ExecutionQueue.http,
        requirements=[75],
    )
    F070: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F070",
        cwe=266,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F071: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F071",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
    )
    F073: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F073",
        cwe=478,
        execution_queue=ExecutionQueue.cloud,
        requirements=[161],
    )
    F075: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F075",
        cwe=284,
        execution_queue=ExecutionQueue.apk,
        requirements=[176],
    )
    F079: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F079",
        cwe=829,
        execution_queue=ExecutionQueue.f117,
        requirements=[302],
    )
    F080: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F080",
        cwe=311,
        execution_queue=ExecutionQueue.cloud,
        requirements=[185],
    )
    F082: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F082",
        cwe=459,
        execution_queue=ExecutionQueue.apk,
        requirements=[183],
    )
    F085: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F085",
        cwe=922,
        execution_queue=ExecutionQueue.leak,
        requirements=[329],
    )
    F086: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F086",
        cwe=353,
        execution_queue=ExecutionQueue.http,
        requirements=[178, 262, 330],
    )
    F089: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F089",
        cwe=501,
        execution_queue=ExecutionQueue.control,
        requirements=[173],
    )
    F091: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F091",
        cwe=117,
        execution_queue=ExecutionQueue.f014,
        requirements=[80, 173],
    )
    F092: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F092",
        cwe=757,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
    )
    F094: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F094",
        cwe=757,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181, 336],
    )
    F096: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F096",
        cwe=502,
        execution_queue=ExecutionQueue.f014,
        requirements=[173, 321],
    )
    F099: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F099",
        cwe=311,
        execution_queue=ExecutionQueue.cloud,
        requirements=[134, 135, 185, 227, 229, 264, 300],
    )
    F100: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F100",
        cwe=918,
        execution_queue=ExecutionQueue.f014,
        requirements=[173, 324],
    )
    F103: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F103",
        cwe=325,
        execution_queue=ExecutionQueue.apk,
        requirements=[178],
    )
    F107: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F107",
        cwe=90,
        execution_queue=ExecutionQueue.injection,
        requirements=[173],
    )
    F109: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F109",
        cwe=681,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F112: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F112",
        cwe=89,
        execution_queue=ExecutionQueue.sql,
        requirements=[169],
    )
    F117: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F117",
        cwe=377,
        execution_queue=ExecutionQueue.f117,
        requirements=[323],
    )
    F127: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F127",
        cwe=843,
        execution_queue=ExecutionQueue.control,
        requirements=[342],
    )
    F128: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F128",
        cwe=1004,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
    )
    F129: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F129",
        cwe=1275,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
    )
    F130: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F130",
        cwe=614,
        execution_queue=ExecutionQueue.http,
        requirements=[29],
    )
    F131: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F131",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62, 181],
    )
    F132: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F132",
        cwe=644,
        execution_queue=ExecutionQueue.http,
        requirements=[62],
    )
    F133: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F133",
        cwe=310,
        execution_queue=ExecutionQueue.ssl,
        requirements=[148, 149, 150, 181],
    )
    F134: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F134",
        cwe=16,
        execution_queue=ExecutionQueue.http,
        requirements=[62, 266, 349],
    )
    F157: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F157",
        cwe=923,
        execution_queue=ExecutionQueue.cloud,
        requirements=[255],
    )
    F160: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F160",
        cwe=378,
        execution_queue=ExecutionQueue.control,
        requirements=[95, 96, 186],
    )
    F177: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F177",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F200: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F200",
        cwe=778,
        execution_queue=ExecutionQueue.cloud,
        requirements=[75, 320],
    )
    F203: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F203",
        cwe=284,
        execution_queue=ExecutionQueue.cloud,
        requirements=[96, 176, 264, 320],
    )
    F206: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F206",
        cwe=295,
        execution_queue=ExecutionQueue.apk,
        requirements=[62, 266, 273],
    )
    F207: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F207",
        cwe=295,
        execution_queue=ExecutionQueue.apk,
        requirements=[93],
    )
    F211: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F211",
        cwe=405,
        execution_queue=ExecutionQueue.control,
        requirements=[72],
    )
    F237: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F237",
        cwe=209,
        execution_queue=ExecutionQueue.leak,
        requirements=[77, 176],
    )
    F239: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F239",
        cwe=200,
        execution_queue=ExecutionQueue.leak,
        requirements=[77, 176],
    )
    F241: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F241",
        cwe=306,
        execution_queue=ExecutionQueue.none,
        requirements=[227, 228, 229, 231, 235, 264, 319],
    )
    F246: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F246",
        cwe=311,
        execution_queue=ExecutionQueue.crypto,
        requirements=[134, 135, 185, 229, 264, 300],
    )
    F247: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F247",
        cwe=311,
        execution_queue=ExecutionQueue.cloud,
        requirements=[134, 135, 185, 229, 264, 300],
    )
    F250: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F250",
        cwe=313,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F252: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F252",
        cwe=284,
        execution_queue=ExecutionQueue.cloud,
        requirements=[237, 266, 327],
    )
    F256: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F256",
        cwe=693,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186, 265],
    )
    F257: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F257",
        cwe=463,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186, 265],
    )
    F258: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F258",
        cwe=463,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186, 265],
    )
    F259: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F259",
        cwe=463,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186, 265],
    )
    F266: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F266",
        cwe=250,
        execution_queue=ExecutionQueue.cloud,
        requirements=[95, 96, 186],
    )
    F267: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F267",
        cwe=250,
        execution_queue=ExecutionQueue.cloud,
        requirements=[95, 186],
    )
    F268: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F268",
        cwe=749,
        execution_queue=ExecutionQueue.apk,
        requirements=[173],
    )
    F277: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F277",
        cwe=521,
        execution_queue=ExecutionQueue.cloud,
        requirements=[130, 132, 133, 139, 332],
    )
    F281: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F281",
        cwe=311,
        execution_queue=ExecutionQueue.cloud,
        requirements=[181],
    )
    F300: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F300",
        cwe=284,
        execution_queue=ExecutionQueue.cloud,
        requirements=[227, 228, 229, 231, 235, 264, 323],
    )
    F313: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F313",
        cwe=295,
        execution_queue=ExecutionQueue.apk,
        requirements=[266],
    )
    F320: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F320",
        cwe=90,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
    )
    F325: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F325",
        cwe=250,
        execution_queue=ExecutionQueue.cloud,
        requirements=[95, 96, 186],
    )
    F333: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F333",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F335: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F335",
        cwe=922,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F338: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F338",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
    )
    F346: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F346",
        cwe=272,
        execution_queue=ExecutionQueue.apk,
        requirements=[95, 96, 186],
    )
    F363: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F363",
        cwe=521,
        execution_queue=ExecutionQueue.cloud,
        requirements=[130, 132, 133, 139, 332],
    )
    F366: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F366",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
    )
    F372: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F372",
        cwe=650,
        execution_queue=ExecutionQueue.cloud,
        requirements=[181],
    )
    F380: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F380",
        cwe=749,
        execution_queue=ExecutionQueue.f014,
        requirements=[266],
    )
    F393: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F393",
        cwe=937,
        execution_queue=ExecutionQueue.sca,
        requirements=[48, 262],
    )
    F394: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F394",
        cwe=117,
        execution_queue=ExecutionQueue.cloud,
        requirements=[80],
    )
    F396: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F396",
        cwe=255,
        execution_queue=ExecutionQueue.cloud,
        requirements=[266],
    )
    F398: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F398",
        cwe=470,
        execution_queue=ExecutionQueue.apk,
        requirements=[266, 173],
    )
    F400: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F400",
        cwe=778,
        execution_queue=ExecutionQueue.cloud,
        requirements=[75, 376, 377, 378],
    )
    F401: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F401",
        cwe=521,
        execution_queue=ExecutionQueue.cloud,
        requirements=[130, 138, 140],
    )
    F402: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F402",
        cwe=778,
        execution_queue=ExecutionQueue.cloud,
        requirements=[75, 376, 377, 378],
    )
    F406: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F406",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[185, 265, 266],
    )
    F407: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F407",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[185, 265, 266],
    )
    F408: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F408",
        cwe=778,
        execution_queue=ExecutionQueue.cloud,
        requirements=[75, 376, 377, 378],
    )
    F409: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F409",
        cwe=16,
        execution_queue=ExecutionQueue.cloud,
        requirements=[185, 265, 266],
    )
    F411: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F411",
        cwe=16,
        execution_queue=ExecutionQueue.control,
        requirements=[147, 151, 181, 224],
    )
    F412: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F412",
        cwe=463,
        execution_queue=ExecutionQueue.cloud,
        requirements=[186, 265],
    )


FINDING_ENUM_FROM_STR: Dict[str, FindingEnum] = {
    __finding.name: __finding for __finding in FindingEnum
}


class FindingEvidenceIDEnum(Enum):
    ANIMATION: str = "ANIMATION"
    EVIDENCE1: str = "EVIDENCE1"
    EVIDENCE2: str = "EVIDENCE2"
    EVIDENCE3: str = "EVIDENCE3"
    EVIDENCE4: str = "EVIDENCE4"
    EVIDENCE5: str = "EVIDENCE5"
    EXPLOIT: str = "EXPLOIT"
    EXPLOITATION: str = "EXPLOITATION"
    RECORDS: str = "RECORDS"


class FindingEvidenceDescriptionIDEnum(Enum):
    EVIDENCE1: str = "EVIDENCE1"
    EVIDENCE2: str = "EVIDENCE2"
    EVIDENCE3: str = "EVIDENCE3"
    EVIDENCE4: str = "EVIDENCE4"
    EVIDENCE5: str = "EVIDENCE5"


class FindingReleaseStatusEnum(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityStateEnum(Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class VulnerabilitySourceEnum(Enum):
    INTEGRATES: str = "integrates"
    SKIMS: str = "skims"


class VulnerabilityVerificationStateEnum(Enum):
    MASKED: str = "MASKED"
    ON_HOLD: str = "ON_HOLD"
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class VulnerabilityVerification(NamedTuple):
    date: datetime
    state: VulnerabilityVerificationStateEnum


class GrammarMatch(NamedTuple):
    start_column: int
    start_line: int


class IntegratesVulnerabilityMetadata(NamedTuple):
    commit_hash: Optional[str] = None
    source: Optional[VulnerabilitySourceEnum] = None
    verification: Optional[VulnerabilityVerification] = None
    uuid: Optional[str] = None


class NVDVulnerability(NamedTuple):
    code: str
    cvss: str
    description: str
    product: str
    url: str
    version: str


class SkimsAPKConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]


class SkimsHttpConfig(NamedTuple):
    include: Tuple[str, ...]


class SkimsPathConfig(NamedTuple):
    exclude: Tuple[str, ...]
    include: Tuple[str, ...]
    lib_path: bool
    lib_root: bool


class SkimsSslTarget(NamedTuple):
    host: str
    port: int


class SkimsSslConfig(NamedTuple):
    include: Tuple[SkimsSslTarget, ...]


class SkimsConfig(NamedTuple):
    apk: SkimsAPKConfig
    checks: Set[FindingEnum]
    group: Optional[str]
    http: SkimsHttpConfig
    language: LocalesEnum
    namespace: str
    output: Optional[str]
    path: SkimsPathConfig
    ssl: SkimsSslConfig
    start_dir: str
    working_dir: str


class SkimsVulnerabilityMetadata(NamedTuple):
    cwe: Tuple[int, ...]
    description: str
    snippet: str
    source_method: str
    developer: DeveloperEnum
    technique: TechniqueEnum


class IntegratesVulnerabilitiesLines(NamedTuple):
    commit_hash: str
    line: str
    path: str
    repo_nickname: str
    state: VulnerabilityStateEnum
    skims_method: Optional[str]
    skims_technique: Optional[str]
    developer: Optional[str]


class IntegratesVulnerabilitiesInputs(NamedTuple):
    field: str
    repo_nickname: str
    state: VulnerabilityStateEnum
    stream: str
    url: str
    skims_method: Optional[str]
    skims_technique: Optional[str]
    developer: Optional[str]


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: VulnerabilityKindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str
    namespace: str
    stream: Optional[str] = "skims"

    integrates_metadata: Optional[IntegratesVulnerabilityMetadata] = None
    skims_metadata: Optional[SkimsVulnerabilityMetadata] = None

    @property
    def digest(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        return hash(
            (
                self.finding,
                self.kind,
                self.namespace,
                self.what,
                self.where,
            )
        )

    @property
    def what_on_integrates(self) -> str:
        if self.kind == VulnerabilityKindEnum.INPUTS:
            what = f"{self.what} ({self.namespace})"
        elif self.kind == VulnerabilityKindEnum.LINES:
            what = f"{self.namespace}/{self.what}"
        elif self.kind == VulnerabilityKindEnum.PORTS:
            what = f"{self.what} ({self.namespace})"
        else:
            raise NotImplementedError()

        return what

    @classmethod
    def what_from_integrates(
        cls, kind: VulnerabilityKindEnum, what_on_integrates: str
    ) -> Tuple[str, str]:
        if kind in {
            VulnerabilityKindEnum.INPUTS,
            VulnerabilityKindEnum.PORTS,
        }:
            if len(chunks := what_on_integrates.rsplit(" (", maxsplit=1)) == 2:
                what, namespace = chunks
                namespace = namespace[:-1]
            else:
                what, namespace = chunks[0], ""
        elif kind == VulnerabilityKindEnum.LINES:
            if len(chunks := what_on_integrates.split("/", maxsplit=1)) == 2:
                namespace, what = chunks
            else:
                namespace, what = "", chunks[0]
        else:
            raise NotImplementedError()

        return namespace, what


Vulnerabilities = Tuple[Vulnerability, ...]


class PersistResult(NamedTuple):
    success: bool
    diff_result: Optional[Any] = None

    def __bool__(self) -> bool:
        return self.success


class DeveloperEnum(Enum):
    ALEJANDRO_SALGADO: str = "asalgado@fluidattacks.com"
    ALEJANDRO_TRUJILLO: str = "atrujillo@fluidattacks.com"
    ANDRES_CUBEROS: str = "acuberos@fluidattacks.com"
    BRIAM_AGUDELO: str = "bagudelo@fluidattacks.com"
    DIEGO_RESTREPO: str = "drestrepo@fluidattacks.com"
    JUAN_ECHEVERRI: str = "jecheverri@fluidattacks.com"
    JUAN_RESTREPO: str = "jrestrepo@fluidattacks.com"
    LUIS_SAAVEDRA: str = "lsaavedra@fluidattacks.com"


class TechniqueEnum(Enum):
    APK: str = "APK"
    SCA: str = "SCA"
    ADVANCE_SAST: str = "ASAST"
    BASIC_SAST: str = "BSAST"
    DAST: str = "DAST"


class MethodInfo(NamedTuple):
    file_name: str
    name: str
    module: str
    finding: FindingEnum
    developer: DeveloperEnum
    technique: TechniqueEnum

    def get_name(self) -> str:
        return f"{self.file_name}.{self.name}"

    def get_cwe(self) -> int:
        return self.finding.value.cwe


class MethodsEnum(Enum):
    CS_SQL_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_sql_injection",
        module="lib_root",
        finding=FindingEnum.F001,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F001 = MethodInfo(
        file_name="query",
        name="query_f001",
        module="sast",
        finding=FindingEnum.F001,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    QUERY_F004 = MethodInfo(
        file_name="query",
        name="query_f004",
        module="sast",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    QUERY_F008 = MethodInfo(
        file_name="query",
        name="query_f008",
        module="sast",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    SYMB_INSEC_ADDHEADER_WRITE = MethodInfo(
        file_name="c_sharp",
        name="insec_addheader_write",
        module="lib_root",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    AWS_CREDENTIALS = MethodInfo(
        file_name="aws",
        name="aws_credentials",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    DOCKER_ENV_SECRETS = MethodInfo(
        file_name="docker",
        name="dockerfile_env_secrets",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    DOCKER_COMPOSE_ENV_SECRETS = MethodInfo(
        file_name="docker",
        name="docker_compose_env_secrets",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_PROP_SENSITIVE = MethodInfo(
        file_name="java",
        name="java_properties_sensitive_data",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    SENSITIVE_KEY_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_key_in_json",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    SENSITIVE_INFO_DOTNET_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_info_in_dotnet_json",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    SENSITIVE_INFO_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_info_in_json",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    WEB_USER_PASS = MethodInfo(
        file_name="conf_files",
        name="web_config_user_pass",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    WEB_DB_CONN = MethodInfo(
        file_name="conf_files",
        name="web_config_db_connection",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JS_CRYPTO_CREDENTIALS = MethodInfo(
        file_name="javascript",
        name="javascript_crypto_js_credentials",
        module="lib_root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JWT_TOKEN = MethodInfo(
        file_name="conf_files",
        name="jwt_token",
        module="lib_path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    MAVEN_POM_XML = MethodInfo(
        file_name="maven",
        name="maven_pom_xml",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
    )
    MAVEN_GRADLE = MethodInfo(
        file_name="maven",
        name="maven_gradle",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
    )
    MAVEN_SBT = MethodInfo(
        file_name="maven",
        name="maven_sbt",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
    )
    NPM_YARN_LOCK = MethodInfo(
        file_name="npm",
        name="npm_yarn_lock",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    NPM_PACKAGE_JSON = MethodInfo(
        file_name="npm",
        name="npm_package_json",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    NPM_PACKAGE_LOCK_JSON = MethodInfo(
        file_name="npm",
        name="npm_package_lock_json",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    NUGET_CSPROJ = MethodInfo(
        file_name="nuget",
        name="nuget_csproj",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    NUGET_PACKAGES_CONFIG = MethodInfo(
        file_name="nuget",
        name="nuget_packages_config",
        module="lib_path",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    JAVA_JPA_LIKE = MethodInfo(
        file_name="java",
        name="java_jpa_like",
        module="lib_root",
        finding=FindingEnum.F012,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_VM_INSEC_AUTH = MethodInfo(
        file_name="terraform",
        name="tfm_azure_virtual_machine_insecure_authentication",
        module="lib_path",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_LNX_VM_INSEC_AUTH = MethodInfo(
        file_name="terraform",
        name="tfm_azure_linux_vm_insecure_authentication",
        module="lib_path",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    WWW_AUTHENTICATE = MethodInfo(
        file_name="analyze_headers",
        name="www_authenticate",
        module="lib_http",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.DAST,
    )
    CFN_INSEC_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_serves_content_over_insecure_protocols",
        module="lib_path",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_INSEC_PROTO = MethodInfo(
        file_name="terraform",
        name="tfm_aws_serves_content_over_insecure_protocols",
        module="lib_path",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_INSEC_PROTO = MethodInfo(
        file_name="terraform",
        name="tfm_azure_serves_content_over_insecure_protocols",
        module="lib_path",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    SSLV3_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="sslv3_enabled",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    TLSV1_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_enabled",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    TLSV1_1_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_1_enabled",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    TLSV1_2_OR_HIGHER_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_2_or_higher_disabled",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    FALLBACK_SCSV_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="fallback_scsv_disabled",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    TLSV1_3_DOWNGRADE = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_3_downgrade",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    HEARTBLEED_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="heartbleed_possible",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    FREAK_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="freak_possible",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    RACCOON_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="raccoon_possible",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    BREACH_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="breach_possible",
        module="lib_ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    CS_JWT_SIGNED = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_jwt_signed",
        module="lib_root",
        finding=FindingEnum.F017,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_VERIFY_DECODER = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_verify_decoder",
        module="lib_root",
        finding=FindingEnum.F017,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F021 = MethodInfo(
        file_name="query",
        name="query_f021",
        module="sast",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    SYMB_XPATH_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="xpath_injection",
        module="lib_root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    JAVA_PROP_UNENCRYPTED_TRANSPORT = MethodInfo(
        file_name="java",
        name="java_properties_unencrypted_transport",
        module="lib_path",
        finding=FindingEnum.F022,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    KT_UNENCRYPTED_CHANNEL = MethodInfo(
        file_name="kotlin",
        name="kotlin_unencrypted_channel",
        module="lib_root",
        finding=FindingEnum.F022,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    LOCATION = MethodInfo(
        file_name="analyze_headers",
        name="location",
        module="lib_http",
        finding=FindingEnum.F023,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.DAST,
    )
    CFN_ANYONE_ADMIN_PORTS = MethodInfo(
        file_name="cloudformation",
        name="cfn_allows_anyone_to_admin_ports",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_SEC_GROUPS_RFC1918 = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_security_groups_ip_ranges_in_rfc1918",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_UNRESTRICTED_PORTS = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ports",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_GROUPS_WITHOUT_EGRESS = MethodInfo(
        file_name="cloudformation",
        name="cfn_groups_without_egress",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_INST_WITHOUT_PROFILE = MethodInfo(
        file_name="cloudformation",
        name="cfn_instances_without_profile",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_UNRESTRICTED_CIDRS = MethodInfo(
        file_name="cloudformation",
        name="cfn_unrestricted_cidrs",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_UNRESTRICTED_IP_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_unrestricted_ip_protocols",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_UNRESTRICTED_PORTS = MethodInfo(
        file_name="cloudformation",
        name="cfn_unrestricted_ports",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_OPEN_ALL_PORTS_PUBLIC = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_open_all_ports_to_the_public",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_UNRESTRICTED_DNS = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_dns_access",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_UNRESTRICTED_FTP = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ftp_access",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_EC2_ALL_TRAFFIC = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_allows_all_outbound_traffic",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_EC2_CFN_UNRESTR_IP_PROT = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_cfn_unrestricted_ip_protocols",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_EC2_UNRESTRICTED_CIDRS = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_unrestricted_cidrs",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EC2_UNRESTRICTED_PORTS = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_ports",
        module="lib_path",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ADMIN_POLICY_ATTACHED = MethodInfo(
        file_name="cloudformation",
        name="cfn_admin_policy_attached",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_BUCKET_ALLOWS_PUBLIC = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_allows_public_access",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_MISSING_SECURITY = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_user_missing_role_based_security",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_NEGATIVE_STATEMENT = MethodInfo(
        file_name="cloudformation",
        name="cfn_negative_statement",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_OPEN_PASSROLE = MethodInfo(
        file_name="cloudformation",
        name="cfn_open_passrole",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_PERMISSIVE_POLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_permissive_policy",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_NO_IAM = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_not_an_iam_instance_profile",
        module="lib_path",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_FULL_ACCESS_SSM = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_has_full_access_to_ssm",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_ADMIN_POLICY = MethodInfo(
        file_name="terraform",
        name="terraform_admin_policy_attached",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_NEGATIVE_STATEMENT = MethodInfo(
        file_name="terraform",
        name="terraform_negative_statement",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_OPEN_PASSROLE = MethodInfo(
        file_name="terraform",
        name="terraform_open_passrole",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_PERMISSIVE_POLICY = MethodInfo(
        file_name="terraform",
        name="terraform_permissive_policy",
        module="lib_path",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EC2_NO_IAM = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_not_an_iam_instance_profile",
        module="lib_path",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JS_WEAK_RANDOM = MethodInfo(
        file_name="javascript",
        name="javascript_weak_random",
        module="lib_root",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    QUERY_F034 = MethodInfo(
        file_name="query",
        name="query_f034",
        module="sast",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CS_WEAK_CREDENTIAL = MethodInfo(
        file_name="c_sharp",
        name="csharp_weak_credential_policy",
        module="lib_root",
        finding=FindingEnum.F035,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CS_NO_PASSWORD = MethodInfo(
        file_name="c_sharp",
        name="csharp_no_password",
        module="lib_root",
        finding=FindingEnum.F035,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    VIEW_STATE = MethodInfo(
        file_name="analyze_content",
        name="view_state",
        module="lib_http",
        finding=FindingEnum.F036,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    CS_INSEC_COOKIES = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecurely_generated_cookies",
        module="lib_root",
        finding=FindingEnum.F042,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F042 = MethodInfo(
        file_name="query",
        name="query_f042",
        module="sast",
        finding=FindingEnum.F042,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CONTENT_SECURITY_POLICY = MethodInfo(
        file_name="analyze_headers",
        name="content_security_policy",
        module="lib_http",
        finding=FindingEnum.F043,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    UPGRADE_INSEC_REQ = MethodInfo(
        file_name="analyze_headers",
        name="upgrade_insecure_requests",
        module="lib_http",
        finding=FindingEnum.F043,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    NO_OBFUSCATION = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_obfuscation",
        module="lib_apk",
        finding=FindingEnum.F046,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    NO_ROOT_CHECK = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_root_check",
        module="lib_apk",
        finding=FindingEnum.F048,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.APK,
    )
    JAVA_PROP_MISSING_SSL = MethodInfo(
        file_name="java",
        name="java_properties_missing_ssl",
        module="lib_path",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_PROP_WEAK_CIPHER = MethodInfo(
        file_name="java",
        name="java_properties_weak_cipher_suite",
        module="lib_path",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_INSECURE_HASH = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_hash",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_INSECURE_CIPHER = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_cipher",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_AES_SECURE_MODE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_aesmanaged_secure_mode",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_RSA_SECURE_MODE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_rsa_secure_mode",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_INSECURE_KEYS = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_keys",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    GO_INSECURE_CIPHER = MethodInfo(
        file_name="go",
        name="go_insecure_cipher",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    GO_INSECURE_HASH = MethodInfo(
        file_name="go",
        name="go_insecure_hash",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_INSECURE_CIPHER = MethodInfo(
        file_name="java",
        name="java_insecure_cipher",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_INSECURE_HASH = MethodInfo(
        file_name="java",
        name="java_insecure_hash",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_INSECURE_KEY = MethodInfo(
        file_name="java",
        name="java_insecure_key",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_INSECURE_PASS = MethodInfo(
        file_name="java",
        name="java_insecure_pass",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JS_INSECURE_CIPHER = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_cipher",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    JS_INSECURE_KEY = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_key",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    JS_INSECURE_HASH = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_hash",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    KT_INSECURE_CIPHER = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_cipher",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    KT_INSECURE_HASH = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_hash",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    KT_INSECURE_KEY = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_key",
        module="lib_root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F052 = MethodInfo(
        file_name="query",
        name="query_f052",
        module="sast",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    WEAK_CIPHERS_ALLOWED = MethodInfo(
        file_name="analyze_protocol",
        name="weak_ciphers_allowed",
        module="lib_ssl",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    APK_BACKUPS_ENABLED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_backups_enabled",
        module="lib_apk",
        finding=FindingEnum.F055,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
    )
    PATH_APK_BACKUPS_ENABLED = MethodInfo(
        file_name="android",
        name="apk_backups_enabled",
        module="lib_path",
        finding=FindingEnum.F055,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JSON_ANON_CONNECTION_CONFIG = MethodInfo(
        file_name="conf_files",
        name="json_anon_connection_config",
        module="lib_path",
        finding=FindingEnum.F056,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    APK_DEBUGGING_ENABLED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_debugging_enabled",
        module="lib_apk",
        finding=FindingEnum.F058,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
    )
    PATH_APK_DEBUGGING_ENABLED = MethodInfo(
        file_name="android",
        name="apk_debugging_enabled",
        module="lib_path",
        finding=FindingEnum.F058,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    NOT_VERIFIES_SSL_HOSTNAME = MethodInfo(
        file_name="analyze_bytecodes",
        name="not_verifies_ssl_hostname",
        module="lib_apk",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    QUERY_F063 = MethodInfo(
        file_name="query",
        name="query_f063",
        module="sast",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    DATE = MethodInfo(
        file_name="analyze_headers",
        name="date",
        module="lib_http",
        finding=FindingEnum.F064,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.DAST,
    )
    CFN_ELB2_INSECURE_SEC_POLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_security_policy",
        module="lib_path",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_LB_TARGET_INSECURE_PORT = MethodInfo(
        file_name="terraform",
        name="tfm_lb_target_group_insecure_port",
        module="lib_path",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    REFERRER_POLICY = MethodInfo(
        file_name="analyze_headers",
        name="referrer_policy",
        module="lib_http",
        finding=FindingEnum.F071,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    CFN_RDS_PUB_ACCESSIBLE = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_is_publicly_accessible",
        module="lib_path",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_CLUSTER_PUB_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_db_cluster_publicly_accessible",
        module="lib_path",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_PUB_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_db_instance_publicly_accessible",
        module="lib_path",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    APK_EXPORTED_CP = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_exported_cp",
        module="lib_apk",
        finding=FindingEnum.F075,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
    )
    PATH_APK_EXPORTED_CP = MethodInfo(
        file_name="android",
        name="apk_exported_cp",
        module="lib_path",
        finding=FindingEnum.F075,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    NON_UPGRADEABLE_DEPS = MethodInfo(
        file_name="generic",
        name="non_upgradeable_deps",
        module="lib_path",
        finding=FindingEnum.F079,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    USES_INSECURE_DELETE = MethodInfo(
        file_name="analyze_bytecodes",
        name="uses_insecure_delete",
        module="lib_apk",
        finding=FindingEnum.F082,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    SOCKET_GET_INSECURE = MethodInfo(
        file_name="analyze_bytecodes",
        name="socket_uses_get_insecure",
        module="lib_apk",
        finding=FindingEnum.F082,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    JS_CLIENT_STORAGE = MethodInfo(
        file_name="javascript",
        name="javascript_client_storage",
        module="lib_root",
        finding=FindingEnum.F085,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    SUB_RESOURCE_INTEGRITY = MethodInfo(
        file_name="analyze_content",
        name="sub_resource_integrity",
        module="lib_http",
        finding=FindingEnum.F086,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    QUERY_F089 = MethodInfo(
        file_name="query",
        name="query_f089",
        module="sast",
        finding=FindingEnum.F089,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CS_INSECURE_LOGGING = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_logging",
        module="lib_root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CBC_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="cbc_enabled",
        module="lib_ssl",
        finding=FindingEnum.F094,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    CS_INSECURE_DESERIAL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_deserialization",
        module="lib_root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_XML_SERIAL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_check_xml_serializer",
        module="lib_root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_POLICY_SERVER_ENCRYP_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_has_server_side_encryption_disabled",
        module="lib_path",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_UNENCRYPTED_BUCKETS = MethodInfo(
        file_name="cloudformation",
        name="cfn_unencrypted_buckets",
        module="lib_path",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_UNENCRYPTED_BUCKETS = MethodInfo(
        file_name="terraform",
        name="tfm_unencrypted_buckets",
        module="lib_path",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F100 = MethodInfo(
        file_name="query",
        name="query_f100",
        module="sast",
        finding=FindingEnum.F100,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    SYMB_INSEC_CREATE = MethodInfo(
        file_name="c_sharp",
        name="insec_create",
        module="lib_root",
        finding=FindingEnum.F100,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    APK_UNSIGNED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_unsigned",
        module="lib_apk",
        finding=FindingEnum.F103,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.APK,
    )
    QUERY_F107 = MethodInfo(
        file_name="query",
        name="query_f107",
        module="sast",
        finding=FindingEnum.F107,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CFN_RDS_NOT_INSIDE_DB_SUBNET = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_is_not_inside_a_db_subnet_group",
        module="lib_path",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_INSIDE_SUBNET = MethodInfo(
        file_name="terraform",
        name="tfm_db_cluster_inside_subnet",
        module="lib_path",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_RDS_INSIDE_SUBNET = MethodInfo(
        file_name="terraform",
        name="tfm_rds_instance_inside_subnet",
        module="lib_path",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F112 = MethodInfo(
        file_name="query",
        name="query_f112",
        module="sast",
        finding=FindingEnum.F112,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    UNVERIFIABLE_FILES = MethodInfo(
        file_name="generic",
        name="unverifiable_files",
        module="lib_path",
        finding=FindingEnum.F117,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F127 = MethodInfo(
        file_name="query",
        name="query_f127",
        module="sast",
        finding=FindingEnum.F127,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    SET_COOKIE_HTTPONLY = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_httponly",
        module="lib_http",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    SET_COOKIE_SAMESITE = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_samesite",
        module="lib_http",
        finding=FindingEnum.F129,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    SET_COOKIE_SECURE = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_secure",
        module="lib_http",
        finding=FindingEnum.F130,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    STRICT_TRANSPORT_SECURITY = MethodInfo(
        file_name="analyze_headers",
        name="strict_transport_security",
        module="lib_http",
        finding=FindingEnum.F131,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    X_CONTENT_TYPE_OPTIONS = MethodInfo(
        file_name="analyze_headers",
        name="x_content_type_options",
        module="lib_http",
        finding=FindingEnum.F132,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.DAST,
    )
    PFS_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="pfs_disabled",
        module="lib_ssl",
        finding=FindingEnum.F133,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
    )
    CS_INSECURE_CORS = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecure_cors",
        module="lib_root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_UNRESTRICTED_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_unrestricted_access_network_segments",
        module="lib_path",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_SA_DEFAULT_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sa_default_network_access",
        module="lib_path",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_KV_DEFAULT_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_default_network_access",
        module="lib_path",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_KV_DANGER_BYPASS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_danger_bypass",
        module="lib_path",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_CREATE_TEMP_FILE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_file_create_temp_file",
        module="lib_root",
        finding=FindingEnum.F160,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_CREATE_TEMP_FILE = MethodInfo(
        file_name="java",
        name="java_file_create_temp_file",
        module="lib_root",
        finding=FindingEnum.F160,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    EC2_DEFAULT_SEC_GROUP = MethodInfo(
        file_name="terraform",
        name="ec2_use_default_security_group",
        module="lib_path",
        finding=FindingEnum.F177,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_PUBLIC_BUCKETS = MethodInfo(
        file_name="cloudformation",
        name="cfn_public_buckets",
        module="lib_path",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_PUBLIC_BUCKETS = MethodInfo(
        file_name="terraform",
        name="tfm_public_buckets",
        module="lib_path",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    HAS_FRIDA = MethodInfo(
        file_name="analyze_bytecodes",
        name="has_frida",
        module="lib_apk",
        finding=FindingEnum.F206,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    NO_CERTS_PINNING = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_certs_pinning",
        module="lib_apk",
        finding=FindingEnum.F207,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.APK,
    )
    CS_VULN_REGEX = MethodInfo(
        file_name="c_sharp",
        name="csharp_vuln_regular_expression",
        module="lib_root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    JAVA_LEAK_STACKTRACE = MethodInfo(
        file_name="java",
        name="java_info_leak_stacktrace",
        module="lib_root",
        finding=FindingEnum.F237,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_RDS_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_unencrypted_storage",
        module="lib_path",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_RDS_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="terraform",
        name="tfm_rds_has_unencrypted_storage",
        module="lib_path",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="terraform",
        name="tfm_db_has_unencrypted_storage",
        module="lib_path",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_FSX_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="terraform",
        name="tfm_fsx_unencrypted_volumes",
        module="lib_path",
        finding=FindingEnum.F247,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EBS_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="terraform",
        name="tfm_ebs_unencrypted_volumes",
        module="lib_path",
        finding=FindingEnum.F247,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EC2_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_unencrypted_volumes",
        module="lib_path",
        finding=FindingEnum.F247,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EBS_UNENCRYPTED_DEFAULT = MethodInfo(
        file_name="terraform",
        name="tfm_ebs_unencrypted_by_default",
        module="lib_path",
        finding=FindingEnum.F247,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_FSX_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="cloudformation",
        name="cfn_fsx_has_unencrypted_volumes",
        module="lib_path",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unencrypted_volumes",
        module="lib_path",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_RDS_NOT_AUTO_BACKUPS = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_not_automated_backups",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_RDS_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_not_termination_protection",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_NO_DELETION_PROTEC = MethodInfo(
        file_name="terraform",
        name="tfm_db_no_deletion_protection",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_RDS_NO_DELETION_PROTEC = MethodInfo(
        file_name="terraform",
        name="tfm_rds_no_deletion_protection",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_NOT_AUTO_BACKUPS = MethodInfo(
        file_name="terraform",
        name="tfm_db_has_not_automated_backups",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_RDS_NOT_AUTO_BACKUPS = MethodInfo(
        file_name="terraform",
        name="tfm_rds_has_not_automated_backups",
        module="lib_path",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_EC2_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_not_termination_protection",
        module="lib_path",
        finding=FindingEnum.F257,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    EC2_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="terraform",
        name="ec2_has_not_termination_protection",
        module="lib_path",
        finding=FindingEnum.F257,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ELB2_NOT_DELETION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_has_not_deletion_protection",
        module="lib_path",
        finding=FindingEnum.F258,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_NOT_POINT_TIME_RECOVERY = MethodInfo(
        file_name="cloudformation",
        name="cfn_has_not_point_in_time_recovery",
        module="lib_path",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_DB_NO_POINT_TIME_RECOVERY = MethodInfo(
        file_name="terraform",
        name="tfm_db_no_point_in_time_recovery",
        module="lib_path",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CONTAINER_WHITOUR_USER = MethodInfo(
        file_name="docker",
        name="container_whitout_user",
        module="lib_path",
        finding=FindingEnum.F266,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    K8S_SYS_ADMIN_LINUX_CAP_USED = MethodInfo(
        file_name="kubernetes",
        name="k8s_sys_admin_linux_cap_used",
        module="lib_path",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    K8S_PRIVILEGE_ESCALATION_ENABLED = MethodInfo(
        file_name="kubernetes",
        name="k8s_allow_privilege_escalation_enabled",
        module="lib_path",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_BUCKET_POLICY_SEC_TRANSPORT = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_has_secure_transport",
        module="lib_path",
        finding=FindingEnum.F281,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ELB2_USES_INSEC_PORT = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_port",
        module="lib_path",
        finding=FindingEnum.F281,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_APP_AUTH_OFF = MethodInfo(
        file_name="terraform",
        name="tfm_azure_app_authentication_off",
        module="lib_path",
        finding=FindingEnum.F300,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_CLIENT_CERT_ENABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_as_client_certificates_enabled",
        module="lib_path",
        finding=FindingEnum.F300,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    IMPROPER_CERTIFICATE_VALIDATION = MethodInfo(
        file_name="analyze_bytecodes",
        name="improper_certificate_validation",
        module="lib_apk",
        finding=FindingEnum.F313,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    CS_LDAP_CONN_AUTH = MethodInfo(
        file_name="c_sharp",
        name="csharp_ldap_connections_authenticated",
        module="lib_root",
        finding=FindingEnum.F320,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    QUERY_F320 = MethodInfo(
        file_name="query",
        name="query_f320",
        module="sast",
        finding=FindingEnum.F320,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
    )
    CFN_KMS_MASTER_KEYS_EXPOSED = MethodInfo(
        file_name="cloudformation",
        name="cfn_kms_key_has_master_keys_exposed_to_everyone",
        module="lib_path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_WILDCARD_WRITE = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_has_wildcard_resource_on_write_action",
        module="lib_path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_POLICY_MISS_CONFIG = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_is_policy_miss_configured",
        module="lib_path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_PRIVILEGES_OVER_IAM = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_has_privileges_over_iam",
        module="lib_path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_IAM_ROLE_OVER_PRIVILEGED = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_is_role_over_privileged",
        module="lib_path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    WEBVIEW_VULNS = MethodInfo(
        file_name="analyze_bytecodes",
        name="webview_vulnerabilities",
        module="lib_apk",
        finding=FindingEnum.F268,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    EC2_TERMINATE_SHUTDOWN_BEHAVIOR = MethodInfo(
        file_name="terraform",
        name="ec2_has_terminate_shutdown_behavior",
        module="lib_path",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EC2_ASSOC_PUB_IP = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_associate_public_ip_address",
        module="lib_path",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_S3_VERSIONING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_s3_versioning_disabled",
        module="lib_path",
        finding=FindingEnum.F335,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_CHECK_HASHES_SALT = MethodInfo(
        file_name="c_sharp",
        name="csharp_check_hashes_salt",
        module="lib_root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    DANGEROUS_PERMISSIONS = MethodInfo(
        file_name="android",
        name="has_dangerous_permissions",
        module="lib_path",
        finding=FindingEnum.F346,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_INSEC_GEN_SECRET = MethodInfo(
        file_name="cloudformation",
        name="cfn_insecure_generate_secret_string",
        module="lib_path",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CS_CONFLICTING_ANNOTATIONS = MethodInfo(
        file_name="c_sharp",
        name="csharp_conflicting_annotations",
        module="lib_root",
        finding=FindingEnum.F366,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_CONTENT_HTTP = MethodInfo(
        file_name="cloudformation",
        name="cfn_serves_content_over_http",
        module="lib_path",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ELB2_INSEC_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_protocol",
        module="lib_path",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_CONTENT_HTTP = MethodInfo(
        file_name="terraform",
        name="tfm_serves_content_over_http",
        module="lib_path",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_KV_ONLY_ACCESS_HTTPS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_only_accessible_over_https",
        module="lib_path",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_SA_INSEC_TRANSFER = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sa_insecure_transfer",
        module="lib_path",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    UNPINNED_DOCKER_IMAGE = MethodInfo(
        file_name="docker",
        name="unpinned_docker_image",
        module="lib_path",
        finding=FindingEnum.F380,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    USES_HTTP_RESOURCES = MethodInfo(
        file_name="analyze_bytecodes",
        name="uses_http_resources",
        module="lib_apk",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    NPM_PKG_JSON = MethodInfo(
        file_name="npm",
        name="npm_pkg_json",
        module="lib_path",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    NPM_PKG_LOCK_JSON = MethodInfo(
        file_name="npm",
        name="npm_pkg_lock_json",
        module="lib_path",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.JUAN_RESTREPO,
        technique=TechniqueEnum.SCA,
    )
    CFN_LOG_NOT_VALIDATED = MethodInfo(
        file_name="cloudformation",
        name="cfn_log_files_not_validated",
        module="lib_path",
        finding=FindingEnum.F394,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_KMS_KEY_ROTATION_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_kms_key_is_key_rotation_absent_or_disabled",
        module="lib_path",
        finding=FindingEnum.F396,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    FRAGMENT_INJECTION = MethodInfo(
        file_name="analyze_bytecodes",
        name="has_fragment_injection",
        module="lib_apk",
        finding=FindingEnum.F398,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
    )
    CFN_LOG_CONF_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_has_logging_conf_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ELB_ACCESS_LOG_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb_has_access_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_CF_DISTR_LOG_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_cf_distribution_has_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_TRAILS_NOT_MULTIREGION = MethodInfo(
        file_name="cloudformation",
        name="cfn_trails_not_multiregion",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    CFN_ELB2_LOGS_S3_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_has_access_logs_s3_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_ELB_LOGGING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_elb_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_S3_LOGGING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_s3_bucket_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_EC2_MONITORING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_monitoring_disabled",
        module="lib_path",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_KV_SECRET_NO_EXPIRATION = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_secret_no_expiration_date",
        module="lib_path",
        finding=FindingEnum.F401,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_STORAGE_LOG_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_storage_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_APP_LOG_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_app_service_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_SQL_LOG_RETENT = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sql_server_audit_log_retention",
        module="lib_path",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_EFS_UNENCRYPTED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_efs_unencrypted",
        module="lib_path",
        finding=FindingEnum.F406,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_EBS_VOLUMES_UNENCRYPTED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ebs_volumes_unencrypted",
        module="lib_path",
        finding=FindingEnum.F407,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_API_GATEWAY_LOGGING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_api_gateway_access_logging_disabled",
        module="lib_path",
        finding=FindingEnum.F408,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_DYNAMODB_TABLE_UNENCRYPTED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_dynamodb_table_unencrypted",
        module="lib_path",
        finding=FindingEnum.F409,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AWS_SECRET_WHITOUTH_KMS_CMK = MethodInfo(
        file_name="terraform",
        name="tfm_aws_secret_encrypted_whitouth_kms_cmk",
        module="lib_path",
        finding=FindingEnum.F411,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
    TFM_AZURE_KEY_VAULT_NOT_RECOVER = MethodInfo(
        file_name="terraform",
        name="tfm_azure_key_vault_not_recoverable",
        module="lib_path",
        finding=FindingEnum.F412,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
    )
