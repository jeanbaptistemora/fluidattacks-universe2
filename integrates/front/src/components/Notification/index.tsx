import type { FC } from "react";
import React from "react";
import styled from "styled-components";

import { Text } from "components/Text";

interface INotificationProps {
  text: string;
  title: string;
}

const NotificationBox = styled.div.attrs({
  className: "pa2",
})``;

const Notification: FC<INotificationProps> = ({
  text,
  title,
}: Readonly<INotificationProps>): JSX.Element => (
  <NotificationBox>
    <Text mb={1} size={"small"} tone={"light"}>
      {title}
    </Text>
    <Text size={"small"} tone={"light"}>
      {text}
    </Text>
  </NotificationBox>
);

export { Notification };
