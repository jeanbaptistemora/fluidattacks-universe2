import { faAngleDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { SplitButtonContainer } from "./styles";

interface ISplitButtonProps {
  content: React.ReactNode;
  id: string;
  isOpen: boolean;
  onHover: () => void;
  onLeave: () => void;
  title: React.ReactNode;
}

const SplitButton: React.FC<ISplitButtonProps> = ({
  content,
  id,
  isOpen,
  onHover,
  onLeave,
  title,
}: Readonly<ISplitButtonProps>): JSX.Element => (
  <SplitButtonContainer id={id} onMouseLeave={onLeave} onMouseOver={onHover}>
    {title}
    &nbsp;
    <FontAwesomeIcon icon={faAngleDown} />
    {isOpen ? content : undefined}
  </SplitButtonContainer>
);

export { SplitButton };
