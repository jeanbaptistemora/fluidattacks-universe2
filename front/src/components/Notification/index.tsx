import React from "react";
import style from "./index.css";

interface INotificationProps {
    text: string;
    title: string;
}

const notification: React.SFC<INotificationProps> = (props: INotificationProps): JSX.Element => (
    <React.StrictMode>
        <div className={style.container}>
            <p><small>{props.title}</small></p>
            <p>{props.text}</p>
        </div>
    </React.StrictMode>
);

export { notification as Notification };
