import { faMinus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IRemoveButtonProps } from "./types";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Can } from "utils/authz/Can";

const RemoveButton: React.FC<IRemoveButtonProps> = ({
  areInputsSelected,
  isEnumerating,
  isRemoving,
  onRemove,
  onRemoveMode,
}: IRemoveButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderRemovingBtns: boolean = !isEnumerating;

  const tooltipMessage = useMemo((): string => {
    if (isRemoving) {
      return t("group.toe.inputs.actionButtons.cancelButton.tooltip");
    }

    return t("group.toe.inputs.actionButtons.removeButton.tooltip");
  }, [isRemoving, t]);

  return (
    <Can do={"api_mutations_remove_toe_input_mutate"}>
      {isRemoving ? (
        <Button disabled={!areInputsSelected} onClick={onRemove}>
          <FontAwesomeIcon icon={faMinus} />
          &nbsp;{t("group.toe.inputs.actionButtons.removeButton.text")}
        </Button>
      ) : undefined}
      {shouldRenderRemovingBtns ? (
        <TooltipWrapper
          displayClass={"dib"}
          id={"group.toe.inputs.actionButtons.removeButton.tooltip.id"}
          message={tooltipMessage}
          placement={"top"}
        >
          <Button onClick={onRemoveMode}>
            {isRemoving ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;{t("group.toe.inputs.actionButtons.cancelButton.text")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FontAwesomeIcon icon={faMinus} />
                &nbsp;{t("group.toe.inputs.actionButtons.removeButton.text")}
              </React.Fragment>
            )}
          </Button>
        </TooltipWrapper>
      ) : undefined}
    </Can>
  );
};

export { RemoveButton };
