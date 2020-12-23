import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import type { IHandleAcceptationButtonProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";
import { useAbility } from "@casl/react";
import { useTranslation } from "react-i18next";

const HandleAcceptationButton: React.FC<IHandleAcceptationButtonProps> = ({
  isEditing,
  isRequestingReattack,
  isVerifying,
  openHandleAcceptation,
}: IHandleAcceptationButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canHandleVulnsAcceptation: boolean = permissions.can(
    "backend_api_mutations_handle_vulns_acceptation_mutate"
  );
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_confirm_zero_risk_vuln_mutate"
  );
  const canRejectZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_reject_zero_risk_vuln_mutate"
  );

  const shouldRenderHandleAcceptationBtn: boolean =
    (canHandleVulnsAcceptation ||
      canConfirmZeroRiskVuln ||
      canRejectZeroRiskVuln) &&
    !(isEditing || isRequestingReattack || isVerifying);

  return (
    <React.StrictMode>
      {shouldRenderHandleAcceptationBtn ? (
        <TooltipWrapper
          message={t(
            "search_findings.tab_vuln.buttons_tooltip.handle_acceptation"
          )}
          placement={"top"}
        >
          <Button onClick={openHandleAcceptation}>
            <React.Fragment>
              <FluidIcon icon={"verified"} />
              &nbsp;
              {t("search_findings.tab_vuln.buttons.handle_acceptation")}
            </React.Fragment>
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { HandleAcceptationButton };
