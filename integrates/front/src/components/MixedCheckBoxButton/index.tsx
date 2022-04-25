/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import React from "react";

import { CheckBox, CheckBoxOption } from "styles/styledComponents";

interface ICheckBoxProps {
  name?: string;
  isYesEnabled?: boolean;
  isNoEnabled?: boolean;
  fontSize?: string;
  id: string;
  isSelected?: boolean;
  noLabel: string;
  onApprove?: (checked: boolean) => void;
  onDelete?: (checked: boolean) => void;
  yesLabel: string;
  checkBoxColor?: string;
}

const MixedCheckBoxButton: React.FC<ICheckBoxProps> = (
  props: Readonly<ICheckBoxProps>
): JSX.Element => {
  const {
    isYesEnabled = true,
    isNoEnabled = true,
    fontSize,
    id,
    isSelected = false,
    yesLabel,
    onApprove = undefined,
    onDelete = undefined,
    noLabel,
  } = props;

  function handleClickYes(event: React.MouseEvent<HTMLDivElement>): void {
    event.stopPropagation();
    if (onApprove) {
      onApprove(!isYesEnabled);
    }
  }

  function handleClickNo(event: React.MouseEvent<HTMLDivElement>): void {
    event.stopPropagation();
    if (onDelete) {
      onDelete(!isNoEnabled);
    }
  }

  return (
    <CheckBox className={fontSize} id={id}>
      {isYesEnabled ? (
        <CheckBoxOption
          id={`${id}_yes`}
          onClick={handleClickYes}
          theme={{ selected: isSelected, type: "yes" }}
        >
          {yesLabel}
        </CheckBoxOption>
      ) : undefined}
      {isNoEnabled ? (
        <CheckBoxOption
          id={`${id}_no`}
          onClick={handleClickNo}
          theme={{ selected: isSelected, type: "no" }}
        >
          {noLabel}
        </CheckBoxOption>
      ) : undefined}
    </CheckBox>
  );
};

export type { ICheckBoxProps };
export { MixedCheckBoxButton };
