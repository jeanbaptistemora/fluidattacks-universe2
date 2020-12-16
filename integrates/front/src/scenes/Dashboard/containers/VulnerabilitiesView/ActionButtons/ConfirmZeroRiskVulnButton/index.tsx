import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useTranslation } from "react-i18next";

interface IConfirmZeroRiskVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  onConfirmZeroRisk: () => void;
  openUpdateZeroRiskModal: () => void;
}

const ConfirmZeroRiskVulnButton: React.FC<IConfirmZeroRiskVulnButtonProps> = ({
  areVulnsSelected,
  isConfirmingZeroRisk,
  isEditing,
  isRejectingZeroRisk,
  isRequestingReattack,
  isVerifying,
  onConfirmZeroRisk,
  openUpdateZeroRiskModal,
}: IConfirmZeroRiskVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderConfirmZeroRiskBtn: boolean = !(
    isEditing ||
    isRequestingReattack ||
    isVerifying ||
    isRejectingZeroRisk
  );

  return (
    <Can do={"backend_api_mutations_confirm_zero_risk_vuln_mutate"}>
      {isConfirmingZeroRisk ? (
        <Button disabled={!areVulnsSelected} onClick={openUpdateZeroRiskModal}>
          <FluidIcon icon={"verified"} />
          &nbsp;{t("search_findings.tab_description.confirm_zero_risk.text")}
        </Button>
      ) : undefined}
      {shouldRenderConfirmZeroRiskBtn ? (
        <TooltipWrapper
          message={
            isConfirmingZeroRisk
              ? t("search_findings.tab_vuln.buttons_tooltip.cancel")
              : t("search_findings.tab_description.confirm_zero_risk.tooltip")
          }
          placement={"top"}
        >
          <Button onClick={onConfirmZeroRisk}>
            {isConfirmingZeroRisk ? (
              <React.Fragment>
                <Glyphicon glyph={"remove"} />
                &nbsp;
                {t(
                  "search_findings.tab_description.cancel_confirming_zero_risk"
                )}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"verified"} />
                &nbsp;
                {t("search_findings.tab_description.confirm_zero_risk.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { ConfirmZeroRiskVulnButton, IConfirmZeroRiskVulnButtonProps };
