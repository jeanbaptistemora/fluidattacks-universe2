import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IEditSecretsButtonProps } from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

const EditSecretsButton: React.FC<IEditSecretsButtonProps> = ({
  isHided,
  onEditSecrets,
}: IEditSecretsButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canEditSecretsInBulk: boolean = permissions.can(
    "front_can_edit_credentials_secrets_in_bulk"
  );

  return (
    <React.StrictMode>
      {isHided || !canEditSecretsInBulk ? undefined : (
        <Tooltip
          disp={"inline-block"}
          id={
            "profile.credentialsModal.actionButtons.editSecretsButton.tooltip.id"
          }
          tip={t(
            "profile.credentialsModal.actionButtons.editSecretsButton.tooltip"
          )}
        >
          <Button
            id={"editCredentialsSecrets"}
            onClick={onEditSecrets}
            variant={"primary"}
          >
            <FontAwesomeIcon icon={faPen} />
            &nbsp;
            {t("profile.credentialsModal.actionButtons.editSecretsButton.text")}
          </Button>
        </Tooltip>
      )}
    </React.StrictMode>
  );
};

export { EditSecretsButton };
