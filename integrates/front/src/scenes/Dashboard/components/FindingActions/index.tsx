/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */

import _ from "lodash";
import React from "react";

import { Button } from "components/Button";
import { ConfirmDialog, IConfirmFn } from "components/ConfirmDialog";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/NewTooltipWrapper";
import { ButtonToolbar } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

interface IFindingActionsProps {
  hasSubmission: boolean;
  hasVulns: boolean;
  isDraft: boolean;
  loading: boolean;
  onApprove(): void;
  onDelete(): void;
  onReject(): void;
  onSubmit(): void;
}

const findingActions: React.FC<IFindingActionsProps> = (props: IFindingActionsProps): JSX.Element => {
  const { onApprove, onDelete, onReject, onSubmit } = props;

  const canApprove: boolean = props.hasVulns && props.hasSubmission;

  return (
    <ButtonToolbar>
      {props.isDraft ? (
        <React.Fragment>
          <Can do="backend_api_mutations_submit_draft_mutate">
            {props.hasSubmission ? undefined : (
              <TooltipWrapper
                id={"group.drafts.submit.text"}
                displayClass={"dib"}
                message={translate.t("group.drafts.submit.tooltip")}
              >
                <Button disabled={props.loading} onClick={onSubmit}>
                  {translate.t("group.drafts.submit.text")}
                </Button>
              </TooltipWrapper>
            )}
          </Can>
          <Can do="backend_api_mutations_approve_draft_mutate">
            <ConfirmDialog title={translate.t("group.drafts.approve.title")}>
              {(confirm: IConfirmFn): React.ReactNode => {
                const handleClick: (() => void) = (): void => { confirm(() => { onApprove(); }); };

                return (
                  <TooltipWrapper
                    id={"group.drafts.approve.text"}
                    displayClass={"dib"}
                    message={translate.t("group.drafts.approve.tooltip")}
                  >
                    <Button onClick={handleClick} disabled={!canApprove || props.loading}>
                      <FluidIcon icon="verified" />&nbsp;{translate.t("group.drafts.approve.text")}
                    </Button>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do="backend_api_mutations_reject_draft_mutate">
            <ConfirmDialog title={translate.t("group.drafts.reject.title")}>
              {(confirm: IConfirmFn): React.ReactNode => {
                const handleClick: (() => void) = (): void => { confirm(() => { onReject(); }); };

                return (
                  <TooltipWrapper
                    id={"group.drafts.reject.tooltip"}
                    displayClass={"dib"}
                    message={translate.t("group.drafts.reject.tooltip")}
                  >
                    <Button onClick={handleClick} disabled={!props.hasSubmission || props.loading}>
                      {translate.t("group.drafts.reject.text")}
                    </Button>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </Can>
        </React.Fragment>
      ) : undefined}
      <Can do="backend_api_mutations_delete_finding_mutate">
        <TooltipWrapper
          id={"search_findings.delete.btn.tooltip"}
          displayClass={"dib"}
          message={translate.t("search_findings.delete.btn.tooltip")}
        >
          <Button onClick={onDelete}>
            <FluidIcon icon="delete" />&nbsp;{translate.t("search_findings.delete.btn.text")}
          </Button>
        </TooltipWrapper>
      </Can>
    </ButtonToolbar>
  );
};

export { findingActions as FindingActions };
