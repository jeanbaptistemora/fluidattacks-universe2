import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";

interface IModalConfirmProps {
  disabled?: boolean;
  onCancel?: () => void;
  onConfirm?: "submit" | (() => void);
}

const ModalConfirm: React.FC<IModalConfirmProps> = ({
  disabled,
  onCancel,
  onConfirm,
}: Readonly<IModalConfirmProps>): JSX.Element | null => {
  const { t } = useTranslation();
  const isSubmit = onConfirm === "submit";

  return onConfirm === undefined ? null : (
    <div className={"mt3"}>
      <Button
        disabled={disabled}
        id={"modal-confirm"}
        onClick={isSubmit ? undefined : onConfirm}
        type={isSubmit ? "submit" : "button"}
        variant={"primary"}
      >
        {t("components.modal.confirm")}
      </Button>
      {onCancel ? (
        <Button id={"modal-cancel"} onClick={onCancel} variant={"secondary"}>
          {t("components.modal.cancel")}
        </Button>
      ) : undefined}
    </div>
  );
};

export { ModalConfirm };
