import React from "react";
import styled, { StyledComponent } from "styled-components";

interface INotificationProps {
  text: string;
  title: string;
}

const NotificationContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "sans-pro pa1",
})``;

export const Notification: React.FC<INotificationProps> = (
  props: Readonly<INotificationProps>
): JSX.Element => {
  const { title, text } = props;

  return (
    <NotificationContainer>
      <p>
        <small>{title}</small>
      </p>
      <p>{text}</p>
    </NotificationContainer>
  );
};
