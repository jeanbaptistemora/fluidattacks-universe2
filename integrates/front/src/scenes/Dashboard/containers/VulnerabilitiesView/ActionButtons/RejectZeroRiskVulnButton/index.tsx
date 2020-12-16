import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useTranslation } from "react-i18next";

interface IRejectZeroRiskVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  onRejectZeroRisk: () => void;
  openUpdateZeroRiskModal: () => void;
}

const RejectZeroRiskVulnButton: React.FC<IRejectZeroRiskVulnButtonProps> = ({
  areVulnsSelected,
  isConfirmingZeroRisk,
  isEditing,
  isRejectingZeroRisk,
  isRequestingReattack,
  isVerifying,
  onRejectZeroRisk,
  openUpdateZeroRiskModal,
}: IRejectZeroRiskVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderRejectZeroRiskBtn: boolean = !(
    isEditing ||
    isRequestingReattack ||
    isVerifying ||
    isConfirmingZeroRisk
  );

  return (
    <Can do={"backend_api_mutations_reject_zero_risk_vuln_mutate"}>
      {isRejectingZeroRisk ? (
        <Button disabled={!areVulnsSelected} onClick={openUpdateZeroRiskModal}>
          <FluidIcon icon={"verified"} />
          &nbsp;{t("search_findings.tab_description.reject_zero_risk.text")}
        </Button>
      ) : undefined}
      {shouldRenderRejectZeroRiskBtn ? (
        <TooltipWrapper
          message={
            isRejectingZeroRisk
              ? t("search_findings.tab_vuln.buttons_tooltip.cancel")
              : t("search_findings.tab_description.reject_zero_risk.tooltip")
          }
          placement={"top"}
        >
          <Button onClick={onRejectZeroRisk}>
            {isRejectingZeroRisk ? (
              <React.Fragment>
                <Glyphicon glyph={"remove"} />
                &nbsp;
                {t(
                  "search_findings.tab_description.cancel_rejecting_zero_risk"
                )}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"verified"} />
                &nbsp;
                {t("search_findings.tab_description.reject_zero_risk.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { IRejectZeroRiskVulnButtonProps, RejectZeroRiskVulnButton };
