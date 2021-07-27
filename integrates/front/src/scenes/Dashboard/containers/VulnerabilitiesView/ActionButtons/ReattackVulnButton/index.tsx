import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";

interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isFindingReleased: boolean;
  isReattackRequestedInAllVuln: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  state: "closed" | "open";
  subscription: string;
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
  subscription,
  onRequestReattack,
  openModal,
}: IReattackVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const isContinuous: boolean = _.includes(
    ["continuous", "continua", "concurrente", "si"],
    subscription.toLowerCase()
  );

  const shouldRenderRequestVerifyBtn: boolean =
    isContinuous &&
    isFindingReleased &&
    state === "open" &&
    !(isEditing || isVerifying);

  return (
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
          message={
            isRequestingReattack
              ? t("searchFindings.tabVuln.buttonsTooltip.cancel")
              : t("searchFindings.tabDescription.requestVerify.tooltip")
          }
        >
          <Button
            disabled={isReattackRequestedInAllVuln}
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
  );
};

export { IReattackVulnButtonProps, ReattackVulnButton };
