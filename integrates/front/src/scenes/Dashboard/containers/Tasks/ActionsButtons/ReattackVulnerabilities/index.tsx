import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";
import { msgSuccess } from "utils/notifications";

interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  areVulnerabilitiesReattacked: boolean;
  isEditing: boolean;
  isOpen: boolean;
  isRequestingReattack: boolean;
  onRequestReattack: () => void;
  openModal: () => void;
}

export const ReattackVulnerabilities: React.FC<IReattackVulnButtonProps> = ({
  areVulnsSelected,
  isEditing,
  areVulnerabilitiesReattacked,
  isOpen,
  isRequestingReattack,
  onRequestReattack,
  openModal,
}: IReattackVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderRequestVerifyBtn: boolean = !isEditing;
  const tooltipMessage = useMemo((): string => {
    if (isRequestingReattack) {
      return t("searchFindings.tabVuln.buttonsTooltip.cancel");
    }

    return t("searchFindings.tabDescription.requestVerify.tooltip");
  }, [isRequestingReattack, t]);

  const displayMessage = (): void => {
    if (isRequestingReattack && !isOpen) {
      msgSuccess(
        t("searchFindings.tabVuln.info.text"),
        t("searchFindings.tabVuln.info.title")
      );
    }
  };
  useEffect(displayMessage, [isRequestingReattack, isOpen, t]);

  return (
    <Have I={"is_continuous"}>
      <Can do={"api_mutations_request_vulnerabilities_verification_mutate"}>
        {isRequestingReattack ? (
          <Button
            disabled={!areVulnsSelected}
            id={"confirm-reattack"}
            onClick={openModal}
          >
            <FluidIcon icon={"verified"} />
            &nbsp;
            {t("searchFindings.tabVuln.buttons.reattack")}
          </Button>
        ) : undefined}
        {shouldRenderRequestVerifyBtn ? (
          <TooltipWrapper
            displayClass={"dib"}
            id={"searchFindings.tabVuln.buttonsTooltip.cancelReattack.id"}
            message={tooltipMessage}
          >
            <Button
              disabled={areVulnerabilitiesReattacked}
              id={"start-reattack"}
              onClick={onRequestReattack}
            >
              {isRequestingReattack ? (
                <React.Fragment>
                  <FontAwesomeIcon icon={faTimes} />
                  &nbsp;
                  {t("searchFindings.tabDescription.cancelVerify")}
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <FluidIcon icon={"verified"} />
                  &nbsp;
                  {t("searchFindings.tabDescription.requestVerify.text")}
                </React.Fragment>
              )}
            </Button>
          </TooltipWrapper>
        ) : undefined}
      </Can>
    </Have>
  );
};
