import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IHandleAcceptationButtonProps } from "./types";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authzPermissionsContext } from "utils/authz/config";

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
          displayClass={"dib"}
          id={"searchFindings.tabVuln.buttonsTooltip.handleAcceptation.id"}
          message={t("searchFindings.tabVuln.buttonsTooltip.handleAcceptation")}
          placement={"top"}
        >
          <Button
            id={"handleAcceptationButton"}
            onClick={openHandleAcceptation}
          >
            <React.Fragment>
              <FluidIcon icon={"verified"} />
              &nbsp;
              {t("searchFindings.tabVuln.buttons.handleAcceptation")}
            </React.Fragment>
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { HandleAcceptationButton };
