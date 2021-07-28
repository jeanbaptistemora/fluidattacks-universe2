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
  id?: string;
  isSelected?: boolean;
  nolabel: string;
  onApprove?: (checked: boolean) => void;
  onDelete?: (checked: boolean) => void;
  yeslabel: string;
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
    yeslabel,
    onApprove = undefined,
    onDelete = undefined,
    nolabel,
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
          onClick={handleClickYes}
          theme={{ selected: isSelected, type: "yes" }}
        >
          {yeslabel}
        </CheckBoxOption>
      ) : undefined}
      {isNoEnabled ? (
        <CheckBoxOption
          onClick={handleClickNo}
          theme={{ selected: isSelected, type: "no" }}
        >
          {nolabel}
        </CheckBoxOption>
      ) : undefined}
    </CheckBox>
  );
};

export { MixedCheckBoxButton, ICheckBoxProps };
