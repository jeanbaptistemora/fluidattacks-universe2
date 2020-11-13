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

export interface IRequestZeroRiskVulnButtonProps {
  areVulnsSelected: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerifying: boolean;
  onRequestZeroRisk(): void;
  openUpdateZeroRiskModal(): void;
}

const requestZeroRiskVulnButton: React.FC<IRequestZeroRiskVulnButtonProps> =
    (props: IRequestZeroRiskVulnButtonProps): JSX.Element => {

  const { onRequestZeroRisk, openUpdateZeroRiskModal } = props;

  const shouldRenderRequestZeroRiskBtn: boolean =
    !(
      props.isEditing
      || props.isRequestingReattack
      || props.isVerifying
      || props.isConfirmingZeroRisk
      || props.isRejectingZeroRisk
    );

  return (
    <Can do="backend_api_mutations_request_zero_risk_vuln_mutate">
      {props.isRequestingZeroRisk ? (
        <Button onClick={openUpdateZeroRiskModal} disabled={!props.areVulnsSelected}>
          <FluidIcon icon="verified" />&nbsp;
          {translate.t("search_findings.tab_description.request_zero_risk.text")}
        </Button>
      ) : undefined}
      {shouldRenderRequestZeroRiskBtn ? (
        <TooltipWrapper
          message={props.isRequestingZeroRisk
            ? translate.t("search_findings.tab_vuln.buttons_tooltip.cancel")
            : translate.t("search_findings.tab_description.request_zero_risk.tooltip")
          }
          placement="top"
        >
          <Button onClick={onRequestZeroRisk}>
            {props.isRequestingZeroRisk ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.cancel_requesting_zero_risk")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="verified" />&nbsp;
                {translate.t("search_findings.tab_description.request_zero_risk.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { requestZeroRiskVulnButton as RequestZeroRiskVulnButton };
