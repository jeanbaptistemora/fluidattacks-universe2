import React, { useCallback } from "react";

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

  const onClick1 = useCallback((): void => {
    onClick(eventKey);
  }, [eventKey, onClick]);

  return <StyledMenuItem onClick={onClick1}>{itemContent}</StyledMenuItem>;
};

export { MenuItem };
