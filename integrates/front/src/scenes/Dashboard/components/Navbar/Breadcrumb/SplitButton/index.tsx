import { faAngleDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";

import { SplitButtonContainer } from "./styles";

interface ISplitButtonProps {
  content: React.ReactNode;
  id: string;
  isOpen: boolean;
  onClick: (eventKey: string) => void;
  onHover: () => void;
  onLeave: () => void;
  title: string;
}

const SplitButton: React.FC<ISplitButtonProps> = ({
  content,
  id,
  isOpen,
  onClick,
  onHover,
  onLeave,
  title,
}: Readonly<ISplitButtonProps>): JSX.Element => {
  const handleClick = useCallback((): void => {
    onClick(title.toLocaleLowerCase());
  }, [onClick, title]);

  return (
    <SplitButtonContainer
      id={id}
      onClick={handleClick}
      onMouseLeave={onLeave}
      onMouseOver={onHover}
    >
      {title}
      &nbsp;
      <FontAwesomeIcon icon={faAngleDown} />
      {isOpen ? content : undefined}
    </SplitButtonContainer>
  );
};

export { SplitButton };
