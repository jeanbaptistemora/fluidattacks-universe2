import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useTranslation } from "react-i18next";

interface IVerifyVunButtonProps {
  areVulnsSelected: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  onVerify: () => void;
  openModal: () => void;
}

const VerifyVunButton: React.FC<IVerifyVunButtonProps> = ({
  areVulnsSelected,
  isEditing,
  isRejectingZeroRisk,
  isRequestingReattack,
  isVerified,
  isVerifying,
  onVerify,
  openModal,
}: IVerifyVunButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderVerifyBtn: boolean =
    !isVerified && !(isEditing || isRequestingReattack || isRejectingZeroRisk);

  return (
    <Can do={"backend_api_resolvers_vulnerability__do_verify_request_vuln"}>
      {isVerifying ? (
        <Button disabled={!areVulnsSelected} onClick={openModal}>
          <FluidIcon icon={"verified"} />
          &nbsp;{t("search_findings.tab_description.mark_verified.text")}
        </Button>
      ) : undefined}
      {shouldRenderVerifyBtn ? (
        <TooltipWrapper
          message={
            isVerifying
              ? t("search_findings.tab_vuln.buttons_tooltip.cancel")
              : t("search_findings.tab_description.mark_verified.tooltip")
          }
          placement={"top"}
        >
          <Button onClick={onVerify}>
            {isVerifying ? (
              <React.Fragment>
                <Glyphicon glyph={"remove"} />
                &nbsp;{t("search_findings.tab_description.cancel_verified")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"verified"} />
                &nbsp;{t("search_findings.tab_description.mark_verified.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { IVerifyVunButtonProps, VerifyVunButton };
