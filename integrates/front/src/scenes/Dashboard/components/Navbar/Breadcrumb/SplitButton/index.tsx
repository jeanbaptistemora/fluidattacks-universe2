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
