import React from "react";
import { default as style } from "./index.css";

interface INotificationProps {
  text: string;
  title: string;
}

export const Notification: React.FC<INotificationProps> = (
  props: Readonly<INotificationProps>
): JSX.Element => {
  const { title, text } = props;

  return (
    <div className={style.container}>
      <p>
        <small>{title}</small>
      </p>
      <p>{text}</p>
    </div>
  );
};
