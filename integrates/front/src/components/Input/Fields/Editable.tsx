import React from "react";

import { Label } from "../Label";
import { ExternalLink } from "components/ExternalLink";

interface IEditableProps {
  children: JSX.Element;
  currentValue: string;
  isEditing: boolean;
  label: string;
  tooltip?: string;
}

const Editable: React.FC<Readonly<IEditableProps>> = ({
  children,
  currentValue,
  isEditing,
  label,
  tooltip,
}): JSX.Element => {
  if (isEditing) {
    return children;
  }

  return (
    <React.Fragment>
      <Label tooltip={tooltip}>
        <b>{label}</b>
      </Label>
      {currentValue.startsWith("https://") ? (
        <ExternalLink href={currentValue}>{currentValue}</ExternalLink>
      ) : (
        <p className={"f5 w-fit-content ws-pre-wrap ma0"}>{currentValue}</p>
      )}
    </React.Fragment>
  );
};

export type { IEditableProps };
export { Editable };
