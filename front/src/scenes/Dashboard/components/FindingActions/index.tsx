/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { Button } from "../../../../components/Button";
import { ConfirmDialog, ConfirmFn } from "../../../../components/ConfirmDialog";
import { FluidIcon } from "../../../../components/FluidIcon";
import { Can } from "../../../../utils/authz/Can";
import translate from "../../../../utils/translations/translate";

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
    <ButtonToolbar className="pull-right">
      {props.isDraft ? (
        <React.Fragment>
          <Can do="backend_api_resolvers_finding__do_submit_draft">
            {props.hasSubmission ? undefined : (
              <Button disabled={props.loading} onClick={onSubmit}>
                Submit
              </Button>
            )}
          </Can>
          <Can do="backend_api_resolvers_finding__do_approve_draft">
            <ConfirmDialog title={translate.t("project.drafts.approve")}>
              {(confirm: ConfirmFn): React.ReactNode => {
                const handleClick: (() => void) = (): void => { confirm(() => { onApprove(); }); };

                return (
                  <Button onClick={handleClick} disabled={!canApprove || props.loading}>
                    <FluidIcon icon="verified" />&nbsp;Approve
                  </Button>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do="backend_api_resolvers_finding__do_reject_draft">
            <ConfirmDialog title={translate.t("project.drafts.reject")}>
              {(confirm: ConfirmFn): React.ReactNode => {
                const handleClick: (() => void) = (): void => { confirm(() => { onReject(); }); };

                return (
                  <Button onClick={handleClick} disabled={!props.hasSubmission || props.loading}>
                    Reject
                  </Button>
                );
              }}
            </ConfirmDialog>
          </Can>
        </React.Fragment>
      ) : undefined}
      <Can do="backend_api_resolvers_finding__do_delete_finding">
        <Button onClick={onDelete}>
          <FluidIcon icon="delete" />&nbsp;Delete
        </Button>
      </Can>
    </ButtonToolbar>
  );
};

export { findingActions as FindingActions };
