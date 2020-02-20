import React from "react";
import { Slide, toast } from "react-toastify";
import { Notification } from "../components/Notification";
import { default as style } from "../components/Notification/index.css";

export const msgSuccess: ((text: string, title: string) => void) = (text: string, title: string): void => {
  toast.success(<Notification title={title} text={text} />, { transition: Slide, className: style.success });
};

export const msgError: ((text: string, title?: string) => void) = (text: string, title: string = "Oops!"): void => {
  if (!toast.isActive(text)) {
    toast.error(<Notification title={title} text={text} />, {
      className: style.error,
      toastId: text,
      transition: Slide,
    });
  }
};

export const msgErrorStick: ((text: string, title?: string) => void) =
(text: string, title: string = "Oops!"): void => {
  toast.error(<Notification title={title} text={text} />, {
    autoClose: false, className: style.error, draggable: false, transition: Slide });
};
