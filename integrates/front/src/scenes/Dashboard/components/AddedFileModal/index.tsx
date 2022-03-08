import React from "react";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { IAddedFileModalProps } from "scenes/Dashboard/components/AddedFileModal/types";
import { translate } from "utils/translations/translate";

const addedFileModal: React.FC<IAddedFileModalProps> = (
  props: IAddedFileModalProps
): JSX.Element => {
  const { isOpen, onClose } = props;

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={translate.t("searchFindings.tabResources.modalFileIsPending")}
      >
        <div>
          <p>
            {translate.t("searchFindings.tabResources.files.fileIsPending")}
          </p>
        </div>
        <ModalFooter>
          <Button
            id={"file-added-close"}
            onClick={onClose}
            variant={"secondary"}
          >
            {translate.t("configuration.close")}
          </Button>
        </ModalFooter>
      </Modal>
    </React.StrictMode>
  );
};

export { IAddedFileModalProps, addedFileModal as AddedFileModal };
