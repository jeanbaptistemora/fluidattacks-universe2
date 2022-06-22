import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";

interface IModalConfirmProps {
  disabled?: boolean;
  id?: string;
  onCancel?: () => void;
  onConfirm?: "submit" | (() => void);
  txtCancel?: string;
  txtConfirm?: string;
}

const ModalConfirm: React.FC<IModalConfirmProps> = ({
  disabled,
  id = "modal-confirm",
  onCancel,
  onConfirm = "submit",
  txtCancel,
  txtConfirm,
}: Readonly<IModalConfirmProps>): JSX.Element => {
  const { t } = useTranslation();
  const isSubmit = onConfirm === "submit";

  return (
    <div className={"mt3"}>
      <Button
        disabled={disabled}
        id={id}
        onClick={isSubmit ? undefined : onConfirm}
        type={isSubmit ? "submit" : "button"}
        variant={"primary"}
      >
        {txtConfirm ?? t("components.modal.confirm")}
      </Button>
      {onCancel ? (
        <Button id={`${id}-cancel`} onClick={onCancel} variant={"secondary"}>
          {txtCancel ?? t("components.modal.cancel")}
        </Button>
      ) : undefined}
    </div>
  );
};

export { ModalConfirm };
