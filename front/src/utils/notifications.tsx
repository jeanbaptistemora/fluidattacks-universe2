import { Notification } from "../components/Notification";
import React from "react";
import { default as style } from "../components/Notification/index.css";
import { Slide, toast } from "react-toastify";

export const msgSuccess: (text: string, title: string) => void = (
  text: string,
  title: string
): void => {
  toast.success(<Notification text={text} title={title} />, {
    className: style.success,
    transition: Slide,
  });
};

export const msgError: (text: string, title?: string) => void = (
  text: string,
  title: string = "Oops!"
): void => {
  if (!toast.isActive(text)) {
    toast.error(<Notification text={text} title={title} />, {
      className: style.error,
      toastId: text,
      transition: Slide,
    });
  }
};

export const msgErrorStick: (text: string, title?: string) => void = (
  text: string,
  title: string = "Oops!"
): void => {
  toast.error(<Notification text={text} title={title} />, {
    autoClose: false,
    className: style.error,
    draggable: false,
    transition: Slide,
  });
};
