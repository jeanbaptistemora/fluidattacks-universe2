import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

interface INotifyButtonProps {
  isDisabled: boolean;
  isFindingReleased: boolean;
  onNotify: () => void;
}

const NotifyButton: React.FC<INotifyButtonProps> = ({
  isDisabled,
  isFindingReleased,
  onNotify,
}: INotifyButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canNotifyVulnerability: boolean = permissions.can(
    "api_mutations_send_vulnerability_notification_mutate"
  );
  const shouldRenderNotifyBtn: boolean =
    isFindingReleased && canNotifyVulnerability;

  return (
    <React.StrictMode>
      {shouldRenderNotifyBtn && (
        <Container pr={"8px"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabDescription.notify.tooltip.id"}
            tip={t("searchFindings.tabDescription.notify.tooltip")}
          >
            <Button
              disabled={isDisabled}
              id={"vulnerabilities-edit"}
              onClick={onNotify}
              variant={"ghost"}
            >
              <React.Fragment>
                <FontAwesomeIcon icon={faPaperPlane} />
                &nbsp;{t("searchFindings.tabDescription.notify.text")}
              </React.Fragment>
            </Button>
          </Tooltip>
        </Container>
      )}
    </React.StrictMode>
  );
};

export type { INotifyButtonProps };
export { NotifyButton };
