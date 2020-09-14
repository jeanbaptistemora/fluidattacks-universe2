import { Notification } from "components/Notification";
import React from "react";
import style from "components/Notification/index.css";
import { Slide, toast } from "react-toastify";

const msgSuccess: (text: string, title: string) => void = (
  text: string,
  title: string
): void => {
  toast.success(<Notification text={text} title={title} />, {
    className: style.success,
    transition: Slide,
  });
};

const msgError: (text: string, title?: string) => void = (
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

const msgErrorStick: (text: string, title?: string) => void = (
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

export { msgSuccess, msgError, msgErrorStick };
