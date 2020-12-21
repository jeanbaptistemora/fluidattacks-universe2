import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { FluidIcon } from "components/FluidIcon";
import type { IHandleAcceptationButtonProps } from "./types";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useTranslation } from "react-i18next";

const HandleAcceptationButton: React.FC<IHandleAcceptationButtonProps> = ({
  isConfirmingZeroRisk,
  isEditing,
  isRequestingReattack,
  isVerifying,
  isRejectingZeroRisk,
  openHandleAcceptation,
}: IHandleAcceptationButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderHandleAcceptationBtn: boolean = !(
    isConfirmingZeroRisk ||
    isEditing ||
    isRequestingReattack ||
    isVerifying ||
    isRejectingZeroRisk
  );

  return (
    <Can do={"backend_api_mutations_handle_vulns_acceptation_mutate"}>
      {shouldRenderHandleAcceptationBtn ? (
        <TooltipWrapper
          message={t(
            "search_findings.tab_vuln.buttons_tooltip.handle_acceptation"
          )}
          placement={"top"}
        >
          <Button onClick={openHandleAcceptation}>
            <React.Fragment>
              <FluidIcon icon={"verified"} />
              &nbsp;
              {t("search_findings.tab_vuln.buttons.handle_acceptation")}
            </React.Fragment>
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { HandleAcceptationButton };
