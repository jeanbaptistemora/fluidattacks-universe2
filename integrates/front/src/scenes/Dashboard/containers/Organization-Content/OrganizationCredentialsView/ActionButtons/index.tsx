import { faPen, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import _ from "lodash";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IActionButtonsProps } from "./types";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Tooltip } from "components/Tooltip";
import { RepositoriesDropdown } from "scenes/Dashboard/components/RepositoriesDropdown";
import { Can } from "utils/authz/Can";
import { openUrl } from "utils/resourceHelpers";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  isEditing,
  isRemoving,
  onAdd,
  onEdit,
  onRemove,
  organizationId,
  selectedCredentials,
  shouldDisplayAzureButton,
  shouldDisplayBitbucketButton,
  shouldDisplayGithubButton,
  shouldDisplayGitlabButton,
}: IActionButtonsProps): JSX.Element | null => {
  const { t } = useTranslation();

  const disabled = isAdding || isEditing || isRemoving;

  const labUrl = useMemo((): string => {
    const oauthUrl: URL = new URL("/dgitlab", window.location.origin);
    oauthUrl.searchParams.set("subject", organizationId);

    return oauthUrl.toString();
  }, [organizationId]);

  const hubUrl = useMemo((): string => {
    const oauthUrl: URL = new URL("/dgithub", window.location.origin);
    oauthUrl.searchParams.set("subject", organizationId);

    return oauthUrl.toString();
  }, [organizationId]);

  const ketUrl = useMemo((): string => {
    const oauthUrl: URL = new URL("/dbitbucket", window.location.origin);
    oauthUrl.searchParams.set("subject", organizationId);

    return oauthUrl.toString();
  }, [organizationId]);

  const azureUrl = useMemo((): string => {
    const oauthUrl: URL = new URL("/dazure", window.location.origin);
    oauthUrl.searchParams.set("subject", organizationId);

    return oauthUrl.toString();
  }, [organizationId]);

  const openLabUrl = useCallback((): void => {
    openUrl(labUrl, false);
  }, [labUrl]);

  const openHubUrl = useCallback((): void => {
    openUrl(hubUrl, false);
  }, [hubUrl]);

  const openKetUrl = useCallback((): void => {
    openUrl(ketUrl, false);
  }, [ketUrl]);

  const openAzureUrl = useCallback((): void => {
    openUrl(azureUrl, false);
  }, [azureUrl]);

  const handleClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm(onRemove);
      },
    [onRemove]
  );

  const repositories = {
    azure: {
      isVisible: shouldDisplayAzureButton,
      onClick: openAzureUrl,
    },
    bitbucket: {
      isVisible: shouldDisplayBitbucketButton,
      onClick: openKetUrl,
    },
    gitHub: {
      isVisible: shouldDisplayGithubButton,
      onClick: openHubUrl,
    },
    gitLab: {
      isVisible: shouldDisplayGitlabButton,
      onClick: openLabUrl,
    },
    other: {
      isVisible: true,
      onClick: onAdd,
    },
  };

  return (
    <React.StrictMode>
      <Can do={"api_mutations_update_credentials_mutate"}>
        <Tooltip
          disp={"inline-block"}
          id={
            "organization.tabs.credentials.actionButtons.editButton.tooltip.id"
          }
          tip={t(
            "organization.tabs.credentials.actionButtons.editButton.tooltip"
          )}
        >
          <Button
            disabled={
              disabled ||
              _.isUndefined(selectedCredentials) ||
              selectedCredentials.type === "OAUTH"
            }
            icon={faPen}
            id={"editCredentials"}
            onClick={onEdit}
          >
            {t("organization.tabs.credentials.actionButtons.editButton.text")}
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
                  disabled={disabled || _.isUndefined(selectedCredentials)}
                  icon={faTrashAlt}
                  id={"removeCredentials"}
                  onClick={handleClick(confirm)}
                >
                  {t(
                    "organization.tabs.credentials.actionButtons.removeButton.text"
                  )}
                </Button>
              </Tooltip>
            );
          }}
        </ConfirmDialog>
      </Can>
      <Can do={"api_mutations_add_credentials_mutate"}>
        <RepositoriesDropdown
          availableRepositories={repositories}
          dropDownText={t(
            "organization.tabs.credentials.actionButtons.addButton.text"
          )}
        />
      </Can>
    </React.StrictMode>
  );
};

export { ActionButtons };
