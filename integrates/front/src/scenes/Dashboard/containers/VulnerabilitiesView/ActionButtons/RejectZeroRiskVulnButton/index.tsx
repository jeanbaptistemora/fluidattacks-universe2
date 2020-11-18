/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";
import { Glyphicon } from "react-bootstrap";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

export interface IRejectZeroRiskVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerifying: boolean;
  onRejectZeroRisk(): void;
  openUpdateZeroRiskModal(): void;
}

const rejectZeroRiskVulnButton: React.FC<IRejectZeroRiskVulnButtonProps> =
    (props: IRejectZeroRiskVulnButtonProps): JSX.Element => {

  const { onRejectZeroRisk, openUpdateZeroRiskModal } = props;

  const shouldRenderRejectZeroRiskBtn: boolean =
    !(
      props.isEditing
      || props.isRequestingReattack
      || props.isVerifying
      || props.isConfirmingZeroRisk
      || props.isRequestingZeroRisk
    );

  return (
    <Can do="backend_api_mutations_reject_zero_risk_vuln_mutate">
      {props.isRejectingZeroRisk ? (
        <Button onClick={openUpdateZeroRiskModal} disabled={!props.areVulnsSelected}>
          <FluidIcon icon="verified" />&nbsp;
          {translate.t("search_findings.tab_description.reject_zero_risk.text")}
        </Button>
      ) : undefined}
      {shouldRenderRejectZeroRiskBtn ? (
        <TooltipWrapper
          message={props.isRejectingZeroRisk
            ? translate.t("search_findings.tab_vuln.buttons_tooltip.cancel")
            : translate.t("search_findings.tab_description.reject_zero_risk.tooltip")
          }
          placement="top"
        >
          <Button onClick={onRejectZeroRisk}>
            {props.isRejectingZeroRisk ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.cancel_rejecting_zero_risk")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="verified" />&nbsp;
                {translate.t("search_findings.tab_description.reject_zero_risk.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { rejectZeroRiskVulnButton as RejectZeroRiskVulnButton };
