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
import { translate } from "utils/translations/translate";

export interface IEditButtonProps {
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isRequestingZeroRisk: boolean;
  isVerifying: boolean;
  onEdit(): void;
}

const editButton: React.FC<IEditButtonProps> = (props: IEditButtonProps): JSX.Element => {

  const { onEdit} = props;

  const shouldRenderEditBtn: boolean = !(
    props.isRequestingReattack
    || props.isVerifying
    || props.isConfirmingZeroRisk
    || props.isRejectingZeroRisk
    || props.isRequestingZeroRisk
  );

  return (
    <React.Fragment>
      {shouldRenderEditBtn ? (
        <TooltipWrapper
          message={props.isEditing
            ? translate.t("search_findings.tab_description.editable.cancel_tooltip")
            : translate.t("search_findings.tab_vuln.buttons_tooltip.edit")
          }
        >
          <Button onClick={onEdit} disabled={props.isRequestingReattack || props.isVerifying}>
            {props.isEditing ? (
              <React.Fragment>
                <Glyphicon glyph="remove" />&nbsp;{translate.t("search_findings.tab_description.editable.cancel")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_description.editable.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
        ) : undefined}
    </React.Fragment>
  );
};

export { editButton as EditButton };
