import { Notification } from "components/Notification";
import React from "react";
import { Slide, toast } from "react-toastify";

const msgSuccess: (text: string, title: string) => void = (
  text: string,
  title: string
): void => {
  toast.success(<Notification text={text} title={title} />, {
    className: "bg-ns",
    transition: Slide,
  });
};

const msgError: (text: string, title?: string) => void = (
  text: string,
  title: string = "Oops!"
): void => {
  if (!toast.isActive(text)) {
    toast.error(<Notification text={text} title={title} />, {
      className: "bg-ne",
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
    className: "bg-ne",
    draggable: false,
    transition: Slide,
  });
};

const msgInfo: (text: string, title: string, hideMessage?: boolean) => void = (
  text: string,
  title: string,
  hideMessage: boolean = false
): void => {
  const toastId: string = title.toLocaleLowerCase() + text.toLocaleLowerCase();
  if (hideMessage) {
    toast.dismiss(toastId);

    return;
  }
  toast.info(<Notification text={text} title={title} />, {
    autoClose: false,
    className: "bg-ns",
    closeButton: false,
    delay: 0,
    draggable: false,
    toastId: toastId,
    transition: Slide,
  });
};

export { msgSuccess, msgError, msgErrorStick, msgInfo };
