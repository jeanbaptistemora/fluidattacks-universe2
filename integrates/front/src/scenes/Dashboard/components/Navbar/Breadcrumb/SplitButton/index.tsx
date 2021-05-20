/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import { faCaretDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { IconButton, LastOrg } from "./styles";

import { ButtonGroup } from "styles/styledComponents";

interface ISplitButtonProps {
  content: React.ReactNode;
  id: string;
  onClick: () => void;
  onClickIcon: () => void;
  title: React.ReactNode;
}

const SplitButton: React.FC<ISplitButtonProps> = (
  props: Readonly<ISplitButtonProps>
): JSX.Element => {
  const { content, id, onClick, onClickIcon, title } = props;

  return (
    <ButtonGroup>
      <LastOrg id={id} onClick={onClick}>
        {title}
      </LastOrg>
      <IconButton onClick={onClickIcon}>
        <FontAwesomeIcon icon={faCaretDown} />
      </IconButton>
      {content}
    </ButtonGroup>
  );
};

export { SplitButton };
