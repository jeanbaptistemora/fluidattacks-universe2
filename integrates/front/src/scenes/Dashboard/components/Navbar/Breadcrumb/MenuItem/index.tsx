import React from "react";

import { StyledMenuItem } from "../styles";

interface IMenuItemsProps {
  eventKey: string;
  itemContent: React.ReactNode;
  onClick: (eventKey: string) => void;
}

const MenuItem: React.FC<IMenuItemsProps> = (
  props: Readonly<IMenuItemsProps>
): JSX.Element => {
  const { itemContent, eventKey, onClick } = props;

  function onClick1(): void {
    onClick(eventKey);
  }

  return <StyledMenuItem onClick={onClick1}>{itemContent}</StyledMenuItem>;
};

export { MenuItem };
