import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Tooltip } from "components/Tooltip";
import { translate } from "utils/translations/translate";

const PlusFormatter: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `b-sb bg-sb svg-box20 ${className ?? ""} pointer`,
    type: type ?? "button",
  })
)``;

export const plusFormatter = <T extends object>(
  row: T,
  plusFunction: (arg?: T) => void
): JSX.Element => {
  function handlePlusFormatter(
    event: React.FormEvent<HTMLButtonElement>
  ): void {
    event.stopPropagation();
    plusFunction(row);
  }

  return (
    <Tooltip
      disp={"inline-block"}
      id={"plus_button_formatter_tooltip"}
      tip={translate.t("organization.tabs.weakest.formatter.plus.tooltip")}
    >
      <PlusFormatter onClick={handlePlusFormatter} type={"button"}>
        <FontAwesomeIcon icon={faPlus} />
      </PlusFormatter>
    </Tooltip>
  );
};
