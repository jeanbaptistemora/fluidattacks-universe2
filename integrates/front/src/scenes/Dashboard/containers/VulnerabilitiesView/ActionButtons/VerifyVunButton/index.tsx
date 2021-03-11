import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import { useTranslation } from "react-i18next";

interface IVerifyVunButtonProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  onVerify: () => void;
  openModal: () => void;
}

const VerifyVunButton: React.FC<IVerifyVunButtonProps> = ({
  areVulnsSelected,
  isEditing,
  isRequestingReattack,
  isVerified,
  isVerifying,
  onVerify,
  openModal,
}: IVerifyVunButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderVerifyBtn: boolean =
    !isVerified && !(isEditing || isRequestingReattack);

  return (
    <Can do={"backend_api_mutations_verify_request_vulnerability_mutate"}>
      {isVerifying ? (
        <Button disabled={!areVulnsSelected} onClick={openModal}>
          <FluidIcon icon={"verified"} />
          &nbsp;{t("search_findings.tabDescription.markVerified.text")}
        </Button>
      ) : undefined}
      {shouldRenderVerifyBtn ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"search_findings.tab_vuln.buttons_tooltip.cancelVerify.id"}
          message={
            isVerifying
              ? t("search_findings.tab_vuln.buttons_tooltip.cancel")
              : t("search_findings.tabDescription.markVerified.tooltip")
          }
          placement={"top"}
        >
          <Button onClick={onVerify}>
            {isVerifying ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;{t("search_findings.tabDescription.cancelVerified")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"verified"} />
                &nbsp;{t("search_findings.tabDescription.markVerified.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { IVerifyVunButtonProps, VerifyVunButton };
