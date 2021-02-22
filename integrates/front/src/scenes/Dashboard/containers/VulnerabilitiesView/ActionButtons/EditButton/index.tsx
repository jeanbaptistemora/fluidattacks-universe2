import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useTranslation } from "react-i18next";

interface IEditButtonProps {
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  onEdit: () => void;
}

const EditButton: React.FC<IEditButtonProps> = ({
  isEditing,
  isRequestingReattack,
  isVerifying,
  onEdit,
}: IEditButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderEditBtn: boolean = !(isRequestingReattack || isVerifying);

  return (
    <React.StrictMode>
      {shouldRenderEditBtn ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"search_findings.tab_description.save_edit.tooltip.id"}
          message={
            isEditing
              ? t("search_findings.tab_description.save.tooltip")
              : t("search_findings.tab_vuln.buttons_tooltip.edit")
          }
        >
          <Button
            disabled={isRequestingReattack || isVerifying}
            id={"vulnerabilities-edit"}
            onClick={onEdit}
          >
            {isEditing ? (
              <React.Fragment>
                <FluidIcon icon={"loading"} />
                &nbsp;{t("search_findings.tab_description.save.text")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FluidIcon icon={"edit"} />
                &nbsp;{t("search_findings.tab_vuln.buttons.edit")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </React.StrictMode>
  );
};

export { EditButton, IEditButtonProps };
