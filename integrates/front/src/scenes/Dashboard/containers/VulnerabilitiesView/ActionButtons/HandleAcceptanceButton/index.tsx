import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IHandleAcceptanceButtonProps } from "./types";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

const HandleAcceptanceButton: React.FC<IHandleAcceptanceButtonProps> = ({
  areVulnerabilitiesPendingToAcceptance,
  isEditing,
  isRequestingReattack,
  isVerifying,
  openHandleAcceptance,
}: IHandleAcceptanceButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canHandleVulnsAcceptance: boolean = permissions.can(
    "api_mutations_handle_vulnerabilities_acceptance_mutate"
  );
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "api_mutations_confirm_vulnerabilities_zero_risk_mutate"
  );
  const canRejectZeroRiskVuln: boolean = permissions.can(
    "api_mutations_reject_vulnerabilities_zero_risk_mutate"
  );

  const shouldRenderHandleAcceptanceBtn: boolean =
    (canHandleVulnsAcceptance ||
      canConfirmZeroRiskVuln ||
      canRejectZeroRiskVuln) &&
    !(isEditing || isRequestingReattack || isVerifying) &&
    areVulnerabilitiesPendingToAcceptance;

  return (
    <React.StrictMode>
      {shouldRenderHandleAcceptanceBtn ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"searchFindings.tabVuln.buttonsTooltip.handleAcceptance.id"}
          message={t("searchFindings.tabVuln.buttonsTooltip.handleAcceptance")}
          placement={"top"}
        >
          <Button id={"handleAcceptanceButton"} onClick={openHandleAcceptance}>
            <React.Fragment>
              <FluidIcon icon={"verified"} />
              &nbsp;
              {t("searchFindings.tabVuln.buttons.handleAcceptance")}
            </React.Fragment>
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { HandleAcceptanceButton };
