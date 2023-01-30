import { faPen, faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IActionButtonsProps } from "./types";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Tooltip } from "components/Tooltip";
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

  const openLabUrl = useCallback((): void => {
    openUrl(labUrl, false);
  }, [labUrl]);

  const openHubUrl = useCallback((): void => {
    openUrl(hubUrl, false);
  }, [hubUrl]);

  const openKetUrl = useCallback((): void => {
    openUrl(ketUrl, false);
  }, [ketUrl]);

  const handleClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm(onRemove);
      },
    [onRemove]
  );

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
            id={"editCredentials"}
            onClick={onEdit}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faPen} />
            &nbsp;
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
                  id={"removeCredentials"}
                  onClick={handleClick(confirm)}
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
      {shouldDisplayGithubButton ? (
        <Can do={"api_mutations_add_credentials_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={
              "organization.tabs.credentials.actionButtons.githubButton.tooltip.id"
            }
            tip={t(
              "organization.tabs.credentials.actionButtons.githubButton.tooltip"
            )}
          >
            <Button
              disabled={disabled}
              id={"githubButtonCredentials"}
              onClick={openHubUrl}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faPlus} />
              &nbsp;
              {t(
                "organization.tabs.credentials.actionButtons.githubButton.text"
              )}
            </Button>
          </Tooltip>
        </Can>
      ) : undefined}
      {shouldDisplayGitlabButton ? (
        <Can do={"api_mutations_add_credentials_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={
              "organization.tabs.credentials.actionButtons.gitlabButton.tooltip.id"
            }
            tip={t(
              "organization.tabs.credentials.actionButtons.gitlabButton.tooltip"
            )}
          >
            <Button
              disabled={disabled}
              id={"gitlabButtonCredentials"}
              onClick={openLabUrl}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faPlus} />
              &nbsp;
              {t(
                "organization.tabs.credentials.actionButtons.gitlabButton.text"
              )}
            </Button>
          </Tooltip>
        </Can>
      ) : undefined}
      {shouldDisplayBitbucketButton ? (
        <Can do={"api_mutations_add_credentials_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={
              "organization.tabs.credentials.actionButtons.bitbucketButton.tooltip.id"
            }
            tip={t(
              "organization.tabs.credentials.actionButtons.bitbucketButton.tooltip"
            )}
          >
            <Button
              disabled={disabled}
              id={"bitbucketButtonCredentials"}
              onClick={openKetUrl}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faPlus} />
              &nbsp;
              {t(
                "organization.tabs.credentials.actionButtons.bitbucketButton.text"
              )}
            </Button>
          </Tooltip>
        </Can>
      ) : undefined}
    </React.StrictMode>
  );
};

export { ActionButtons };
