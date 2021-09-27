import React from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { IAddedFileModalProps } from "scenes/Dashboard/components/AddedFileModal/types";
import { translate } from "utils/translations/translate";

const addedFileModal: React.FC<IAddedFileModalProps> = (
  props: IAddedFileModalProps
): JSX.Element => {
  const { isOpen, onClose } = props;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "searchFindings.tabResources.modalFileIsPending"
        )}
        onEsc={onClose}
        open={isOpen}
      >
        <div>
          <p>
            {translate.t("searchFindings.tabResources.files.fileIsPending")}
          </p>
        </div>
        <Button id={"file-added-close"} onClick={onClose}>
          {translate.t("configuration.close")}
        </Button>
      </Modal>
    </React.StrictMode>
  );
};

export { IAddedFileModalProps, addedFileModal as AddedFileModal };
