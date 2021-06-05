from lib_apk.types import (
    APKContext,
)
from model import (
    core_model,
)
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
)
from zone import (
    t,
)


class APKCheckCtx(NamedTuple):
    apk_ctx: APKContext


class Location(NamedTuple):
    description: str


class Locations(NamedTuple):
    locations: List[Location]

    def append(
        self,
        desc: str,
        desc_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_apk.analyze_bytecodes.{desc}",
                    **(desc_kwargs or {}),
                ),
            )
        )


def _apk_unsigned(ctx: APKCheckCtx) -> core_model.Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None:
        signatures: List[str] = ctx.apk_ctx.apk_obj.get_signature_names()

        if not signatures:
            locations.append("apk_unsigned.not_signed")

    return ()


def get_check_ctx(apk_ctx: APKContext) -> APKCheckCtx:
    return APKCheckCtx(
        apk_ctx=apk_ctx,
    )


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[APKCheckCtx], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F103_APK_UNSIGNED: _apk_unsigned,
}
