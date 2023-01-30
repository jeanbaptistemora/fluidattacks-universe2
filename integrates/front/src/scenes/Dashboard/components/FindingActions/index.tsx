import { faCheck, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Tooltip } from "components/Tooltip";
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

  const handleClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm((): void => {
          onApprove();
        });
      },
    [onApprove]
  );

  return (
    <div className={"fr"}>
      {isDraft ? (
        <React.Fragment>
          <Can do={"api_mutations_submit_draft_mutate"}>
            {hasSubmission ? undefined : (
              <Tooltip
                disp={"inline-block"}
                id={"group.drafts.submit.text"}
                tip={t("group.drafts.submit.tooltip")}
              >
                <Button
                  disabled={loading}
                  onClick={onSubmit}
                  variant={"secondary"}
                >
                  {t("group.drafts.submit.text")}
                </Button>
              </Tooltip>
            )}
          </Can>
          <Can do={"api_mutations_approve_draft_mutate"}>
            <ConfirmDialog title={t("group.drafts.approve.title")}>
              {(confirm): React.ReactNode => {
                return (
                  <Tooltip
                    disp={"inline-block"}
                    id={"group.drafts.approve.text"}
                    tip={t("group.drafts.approve.tooltip")}
                  >
                    <Button
                      disabled={!canApprove || loading}
                      onClick={handleClick(confirm)}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faCheck} />
                      &nbsp;{t("group.drafts.approve.text")}
                    </Button>
                  </Tooltip>
                );
              }}
            </ConfirmDialog>
          </Can>
          <Can do={"api_mutations_reject_draft_mutate"}>
            <Tooltip
              id={"group.drafts.reject.tooltip"}
              tip={t("group.drafts.reject.tooltip")}
            >
              <Button
                disabled={!hasSubmission || loading}
                onClick={onReject}
                variant={"secondary"}
              >
                {t("group.drafts.reject.text")}
              </Button>
            </Tooltip>
          </Can>
          <Can do={"api_mutations_remove_finding_mutate"}>
            <Tooltip
              disp={"inline-block"}
              id={"searchFindings.delete.btn.tooltip"}
              tip={t("searchFindings.delete.btn.tooltip")}
            >
              <Button onClick={onDelete} variant={"secondary"}>
                <FontAwesomeIcon icon={faTrashAlt} />
                &nbsp;{t("searchFindings.delete.btn.text")}
              </Button>
            </Tooltip>
          </Can>
        </React.Fragment>
      ) : undefined}
    </div>
  );
};

export { FindingActions };
