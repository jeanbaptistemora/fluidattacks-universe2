import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IActionButtonsProps } from "./types";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Tooltip } from "components/Tooltip";
import { Can } from "utils/authz/Can";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  isRemoving,
  onAdd,
  onRemove,
  selectedCredentials,
}: IActionButtonsProps): JSX.Element | null => {
  const { t } = useTranslation();

  const disabled = isAdding || isRemoving;

  return (
    <React.StrictMode>
      <Can do={"api_mutations_add_credentials_mutate"}>
        <Tooltip
          disp={"inline-block"}
          id={
            "organization.tabs.credentials.actionButtons.addButton.tooltip.id"
          }
          tip={t(
            "organization.tabs.credentials.actionButtons.addButton.tooltip"
          )}
        >
          <Button
            disabled={disabled}
            id={"addCredentials"}
            onClick={onAdd}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faPlus} />
            &nbsp;
            {t("organization.tabs.credentials.actionButtons.addButton.text")}
          </Button>
        </Tooltip>
      </Can>
      <Can do={"api_mutations_remove_credentials_mutate"}>
        <ConfirmDialog
          message={t(
            "organization.tabs.credentials.actionButtons.removeButton.confirmMessage",
            { credentialName: selectedCredentials?.name }
          )}
          title={t(
            "organization.tabs.credentials.actionButtons.removeButton.confirmTitle"
          )}
        >
          {(confirm): React.ReactNode => {
            function handleClick(): void {
              confirm(onRemove);
            }

            return (
              <Tooltip
                disp={"inline-block"}
                id={
                  "organization.tabs.credentials.actionButtons.removeButton.tooltip.btn"
                }
                tip={t(
                  "organization.tabs.credentials.actionButtons.removeButton.tooltip"
                )}
              >
                <Button
                  disabled={disabled}
                  id={"removeCredentials"}
                  onClick={handleClick}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;
                  {t(
                    "organization.tabs.credentials.actionButtons.removeButton.text"
                  )}
                </Button>
              </Tooltip>
            );
          }}
        </ConfirmDialog>
      </Can>
    </React.StrictMode>
  );
};

export { ActionButtons };
