import React from "react";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ButtonToolbar } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { translate } from "utils/translations/translate";

interface IFindingActionsProps {
  hasSubmission: boolean;
  hasVulns: boolean;
  isDraft: boolean;
  loading: boolean;
  onApprove: () => void;
  onDelete: () => void;
  onReject: () => void;
  onSubmit: () => void;
}

const findingActions: React.FC<IFindingActionsProps> = (
  props: IFindingActionsProps
): JSX.Element => {
  const {
    hasSubmission,
    hasVulns,
    isDraft,
    loading,
    onApprove,
    onDelete,
    onReject,
    onSubmit,
  } = props;

  const canApprove: boolean = hasVulns && hasSubmission;

  return (
    <ButtonToolbar>
      {isDraft ? (
        <React.Fragment>
          <Can do={"api_mutations_submit_draft_mutate"}>
            {hasSubmission ? undefined : (
              <TooltipWrapper
                displayClass={"dib"}
                id={"group.drafts.submit.text"}
                message={translate.t("group.drafts.submit.tooltip")}
              >
                <Button disabled={loading} onClick={onSubmit}>
                  {translate.t("group.drafts.submit.text")}
                </Button>
              </TooltipWrapper>
            )}
          </Can>
          <Can do={"api_mutations_approve_draft_mutate"}>
            <ConfirmDialog title={translate.t("group.drafts.approve.title")}>
              {(confirm: IConfirmFn): React.ReactNode => {
                const handleClick: () => void = (): void => {
                  confirm((): void => {
                    onApprove();
                  });
                };

                return (
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"group.drafts.approve.text"}
                    message={translate.t("group.drafts.approve.tooltip")}
                  >
                    <Button
                      disabled={!canApprove || loading}
                      // eslint-disable-next-line react/jsx-no-bind
                      onClick={handleClick}
                    >
                      <FluidIcon icon={"verified"} />
                      &nbsp;{translate.t("group.drafts.approve.text")}
                    </Button>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do={"api_mutations_reject_draft_mutate"}>
            <ConfirmDialog title={translate.t("group.drafts.reject.title")}>
              {(confirm: IConfirmFn): React.ReactNode => {
                const handleClick: () => void = (): void => {
                  confirm((): void => {
                    onReject();
                  });
                };

                return (
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"group.drafts.reject.tooltip"}
                    message={translate.t("group.drafts.reject.tooltip")}
                  >
                    <Button
                      disabled={!hasSubmission || loading}
                      // eslint-disable-next-line react/jsx-no-bind
                      onClick={handleClick}
                    >
                      {translate.t("group.drafts.reject.text")}
                    </Button>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do={"api_mutations_remove_finding_mutate"}>
            <TooltipWrapper
              displayClass={"dib"}
              id={"searchFindings.delete.btn.tooltip"}
              message={translate.t("searchFindings.delete.btn.tooltip")}
            >
              <Button onClick={onDelete}>
                <FluidIcon icon={"delete"} />
                &nbsp;{translate.t("searchFindings.delete.btn.text")}
              </Button>
            </TooltipWrapper>
          </Can>
        </React.Fragment>
      ) : undefined}
    </ButtonToolbar>
  );
};

export { findingActions as FindingActions };
