/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import { ButtonGroup } from "styles/styledComponents";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

interface ISplitButtonProps {
  content: React.ReactNode;
  id: string;
  onClick: () => void;
  onClickIcon: () => void;
  title: React.ReactNode;
}

const LastOrg: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "br0 outline-0",
})``;

const IconButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "br0 outline-0",
})``;

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
        <span className={"caret"} />
      </IconButton>
      {content}
    </ButtonGroup>
  );
};

export { SplitButton };
