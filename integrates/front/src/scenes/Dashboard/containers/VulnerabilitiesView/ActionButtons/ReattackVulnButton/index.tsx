import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "utils/authz/Can";

interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isFindingReleased: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  state: "closed" | "open";
  onRequestReattack: () => void;
  openModal: () => void;
}

const ReattackVulnButton: React.FC<IReattackVulnButtonProps> = ({
  areVulnsSelected,
  isEditing,
  isFindingReleased,
  isReattackRequestedInAllVuln,
  isRequestingReattack,
  isVerifying,
  state,
  onRequestReattack,
  openModal,
}: IReattackVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderRequestVerifyBtn: boolean =
    isFindingReleased && state === "open" && !(isEditing || isVerifying);

  const tooltipMessage = useMemo((): string => {
    if (isRequestingReattack) {
      return t("searchFindings.tabVuln.buttonsTooltip.cancel");
    }

    return t("searchFindings.tabDescription.requestVerify.tooltip");
  }, [isRequestingReattack, t]);

  return (
    <Can do={"api_mutations_request_vulnerabilities_verification_mutate"}>
      {isRequestingReattack ? (
        <Container pr={"8px"}>
          <Button
            disabled={!areVulnsSelected}
            id={"confirm-reattack"}
            onClick={openModal}
            variant={"ghost"}
          >
            <FontAwesomeIcon icon={faCheck} />
            &nbsp;
            {t("searchFindings.tabVuln.buttons.reattack")}
          </Button>
        </Container>
      ) : undefined}
      {shouldRenderRequestVerifyBtn ? (
        <Container pr={"8px"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabVuln.buttonsTooltip.cancelReattack.id"}
            tip={tooltipMessage}
          >
            <Button
              disabled={isReattackRequestedInAllVuln}
              id={"start-reattack"}
              onClick={onRequestReattack}
              variant={"ghost"}
            >
              {isRequestingReattack ? (
                <React.Fragment>
                  <FontAwesomeIcon icon={faTimes} />
                  &nbsp;
                  {t("searchFindings.tabDescription.cancelVerify")}
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <FontAwesomeIcon icon={faCheck} />
                  &nbsp;
                  {t("searchFindings.tabDescription.requestVerify.text")}
                </React.Fragment>
              )}
            </Button>
          </Tooltip>
        </Container>
      ) : undefined}
    </Can>
  );
};

export type { IReattackVulnButtonProps };
export { ReattackVulnButton };
