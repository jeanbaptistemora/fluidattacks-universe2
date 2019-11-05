/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for conditional rendering
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";

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

  const userRole: string = (window as typeof window & { userRole: string }).userRole;
  const canApprove: boolean = props.hasVulns && props.hasSubmission;

  return (
    <ButtonToolbar className="pull-right">
      {!props.isDraft ? false : (props.hasSubmission ?
        false : <Button disabled={props.loading} onClick={onSubmit}>Submit</Button>)}
      {_.includes(["admin"], userRole) && props.isDraft ? (
        <React.Fragment>
          <Button onClick={onApprove} disabled={!canApprove}>
            <FluidIcon icon="verified" />&nbsp;Approve
          </Button>
          <Button onClick={onReject} disabled={!props.hasSubmission}>
            Reject
          </Button>
          <Button onClick={onDelete}>
            <FluidIcon icon="delete" />&nbsp;Delete
          </Button>
        </React.Fragment>
      ) : _.includes(["admin", "analyst"], userRole) ? (
        <Button onClick={onDelete}>
          <FluidIcon icon="delete" />&nbsp;Delete
        </Button>
      ) : undefined}
    </ButtonToolbar>
  );
};

export { findingActions as FindingActions };
