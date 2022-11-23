import { toast as toastify } from "react-toastify";

import { toast } from "components/Alert";

const msgSuccess: (text: string, title: string) => void = (
  text: string,
  title: string
): void => {
  toast({
    msg: text,
    title,
    variant: "success",
  });
};

const msgError: (text: string, title?: string) => void = (
  text: string,
  title: string = "Oops!"
): void => {
  if (!toastify.isActive(text)) {
    toast({
      msg: text,
      title,
      variant: "error",
    });
  }
};

const msgErrorStick: (text: string, title?: string) => void = (
  text: string,
  title: string = "Oops!"
): void => {
  toast({
    autoClose: false,
    draggable: false,
    msg: text,
    title,
    variant: "error",
  });
};

const msgInfo: (text: string, title: string, hideMessage?: boolean) => void = (
  text: string,
  title: string,
  hideMessage: boolean = false
): void => {
  const toastId: string = title.toLocaleLowerCase() + text.toLocaleLowerCase();
  if (hideMessage) {
    toastify.dismiss(toastId);

    return;
  }
  toast({
    autoClose: false,
    closeButton: true,
    delay: 0,
    draggable: false,
    msg: text,
    title,
    variant: "info",
  });
};

export { msgSuccess, msgError, msgErrorStick, msgInfo };
