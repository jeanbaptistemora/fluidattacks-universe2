import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { useTranslation } from "react-i18next";

interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
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
    isContinuous && state === "open" && !(isEditing || isVerifying);

  return (
    <Can do={"backend_api_mutations_request_verification_vulnerability_mutate"}>
      {isRequestingReattack ? (
        <Button
          disabled={!areVulnsSelected}
          id={"confirm-reattack"}
          onClick={openModal}
        >
          <FluidIcon icon={"verified"} />
          &nbsp;
          {t("search_findings.tab_vuln.buttons.reattack")}
        </Button>
      ) : undefined}
      {shouldRenderRequestVerifyBtn ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"search_findings.tab_vuln.buttons_tooltip.cancel_reattack.id"}
          message={
            isRequestingReattack
              ? t("search_findings.tab_vuln.buttons_tooltip.cancel")
              : t("search_findings.tab_description.request_verify.tooltip")
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
                {t("search_findings.tab_description.cancel_verify")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"verified"} />
                &nbsp;
                {t("search_findings.tab_description.request_verify.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { IReattackVulnButtonProps, ReattackVulnButton };
