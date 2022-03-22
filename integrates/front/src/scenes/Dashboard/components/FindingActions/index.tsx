import { faCheck, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper";
import { ButtonToolbar } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

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

const FindingActions: React.FC<IFindingActionsProps> = ({
  hasSubmission,
  hasVulns,
  isDraft,
  loading,
  onApprove,
  onDelete,
  onReject,
  onSubmit,
}: IFindingActionsProps): JSX.Element => {
  const { t } = useTranslation();
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
                message={t("group.drafts.submit.tooltip")}
              >
                <Button
                  disabled={loading}
                  onClick={onSubmit}
                  variant={"secondary"}
                >
                  {t("group.drafts.submit.text")}
                </Button>
              </TooltipWrapper>
            )}
          </Can>
          <Can do={"api_mutations_approve_draft_mutate"}>
            <ConfirmDialog title={t("group.drafts.approve.title")}>
              {(confirm): React.ReactNode => {
                function handleClick(): void {
                  confirm((): void => {
                    onApprove();
                  });
                }

                return (
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"group.drafts.approve.text"}
                    message={t("group.drafts.approve.tooltip")}
                  >
                    <Button
                      disabled={!canApprove || loading}
                      onClick={handleClick}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faCheck} />
                      &nbsp;{t("group.drafts.approve.text")}
                    </Button>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do={"api_mutations_reject_draft_mutate"}>
            <ConfirmDialog title={t("group.drafts.reject.title")}>
              {(confirm): React.ReactNode => {
                function handleClick(): void {
                  confirm((): void => {
                    onReject();
                  });
                }

                return (
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"group.drafts.reject.tooltip"}
                    message={t("group.drafts.reject.tooltip")}
                  >
                    <Button
                      disabled={!hasSubmission || loading}
                      onClick={handleClick}
                      variant={"secondary"}
                    >
                      {t("group.drafts.reject.text")}
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
              message={t("searchFindings.delete.btn.tooltip")}
            >
              <Button onClick={onDelete} variant={"secondary"}>
                <FontAwesomeIcon icon={faTrashAlt} />
                &nbsp;{t("searchFindings.delete.btn.text")}
              </Button>
            </TooltipWrapper>
          </Can>
        </React.Fragment>
      ) : undefined}
    </ButtonToolbar>
  );
};

export { FindingActions };
