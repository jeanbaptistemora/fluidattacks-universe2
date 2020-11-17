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

export interface IConfirmZeroRiskVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerifying: boolean;
  onConfirmZeroRisk(): void;
  openUpdateZeroRiskModal(): void;
}

const confirmZeroRiskVulnButton: React.FC<IConfirmZeroRiskVulnButtonProps> =
    (props: IConfirmZeroRiskVulnButtonProps): JSX.Element => {

  const { onConfirmZeroRisk, openUpdateZeroRiskModal } = props;

  const shouldRenderConfirmZeroRiskBtn: boolean =
    !(
      props.isEditing
      || props.isRequestingReattack
      || props.isVerifying
      || props.isRequestingZeroRisk
      || props.isRejectingZeroRisk
    );

  return (
    <Can do="backend_api_mutations_confirm_zero_risk_vuln_mutate">
      {props.isConfirmingZeroRisk ? (
        <Button onClick={openUpdateZeroRiskModal} disabled={!props.areVulnsSelected}>
          <FluidIcon icon="verified" />&nbsp;
          {translate.t("search_findings.tab_description.confirm_zero_risk.text")}
        </Button>
      ) : undefined}
      {shouldRenderConfirmZeroRiskBtn ? (
        <TooltipWrapper
          message={props.isConfirmingZeroRisk
            ? translate.t("search_findings.tab_vuln.buttons_tooltip.cancel")
            : translate.t("search_findings.tab_description.confirm_zero_risk.tooltip")
          }
          placement="top"
        >
          <Button onClick={onConfirmZeroRisk}>
            {props.isConfirmingZeroRisk ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.cancel_confirming_zero_risk")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="verified" />&nbsp;
                {translate.t("search_findings.tab_description.confirm_zero_risk.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { confirmZeroRiskVulnButton as ConfirmZeroRiskVulnButton };
