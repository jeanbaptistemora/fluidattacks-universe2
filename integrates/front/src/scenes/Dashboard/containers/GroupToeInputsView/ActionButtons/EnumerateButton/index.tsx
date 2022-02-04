import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IEnumerateButtonProps } from "./types";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";

const EnumerateButton: React.FC<IEnumerateButtonProps> = ({
  areInputsSelected,
  isEnumeratingMode,
  isRemovingMode,
  onEnumerate,
  onEnumerateMode,
}: IEnumerateButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderEnumerateBtns: boolean = !isRemovingMode;

  const tooltipMessage = useMemo((): string => {
    if (isEnumeratingMode) {
      return t("group.toe.inputs.actionButtons.cancelButton.tooltip");
    }

    return t("group.toe.inputs.actionButtons.enumerateButton.tooltip");
  }, [isEnumeratingMode, t]);

  return (
    <Can do={"api_mutations_remove_toe_input_mutate"}>
      {isEnumeratingMode ? (
        <Button disabled={!areInputsSelected} onClick={onEnumerate}>
          <FontAwesomeIcon icon={faCheck} />
          &nbsp;{t("group.toe.inputs.actionButtons.enumerateButton.text")}
        </Button>
      ) : undefined}
      {shouldRenderEnumerateBtns ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.inputs.actionButtons.enumerateButton.tooltip.id"}
          message={tooltipMessage}
          placement={"top"}
        >
          <Button onClick={onEnumerateMode}>
            {isEnumeratingMode ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;{t("group.toe.inputs.actionButtons.cancelButton.text")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FontAwesomeIcon icon={faCheck} />
                &nbsp;{t("group.toe.inputs.actionButtons.enumerateButton.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { EnumerateButton };
