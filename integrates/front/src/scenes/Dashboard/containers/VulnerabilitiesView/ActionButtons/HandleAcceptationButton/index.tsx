
/* tslint:disable:jsx-no-multiline-js
 *
 * jsx-no-multiline-js: Necessary for using conditional rendering
 */

import _ from "lodash";
import React from "react";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";

import type {
  IHandleAcceptationButtonProps,
} from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons/HandleAcceptationButton/types";

import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

const handleAcceptationButton: React.FC<IHandleAcceptationButtonProps> = (
  props: IHandleAcceptationButtonProps,
): JSX.Element => {

  const { openHandleAcceptation } = props;

  const shouldRenderHandleAcceptationBtn: boolean =
    !(
      props.isEditing
      || props.isRequestingReattack
      || props.isVerifying
      || props.isRequestingZeroRisk
      || props.isRejectingZeroRisk
    )
    && props.canHandleAcceptation;

  return (
    <Can do="backend_api_mutations_handle_vulns_acceptation_mutate">
      {shouldRenderHandleAcceptationBtn ? (
        <TooltipWrapper
          message={translate.t("search_findings.tab_vuln.buttons_tooltip.handle_acceptation")}
          placement="top"
        >
          <Button onClick={openHandleAcceptation}>
            <React.Fragment>
              <FluidIcon icon="verified" />&nbsp;
              {translate.t("search_findings.tab_vuln.buttons.handle_acceptation")}
            </React.Fragment>
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { handleAcceptationButton as HandleAcceptationButton };
