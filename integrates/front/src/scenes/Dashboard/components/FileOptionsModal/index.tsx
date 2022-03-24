import { faDownload, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal, ModalFooter } from "components/Modal";
import {
  ButtonToolbarCenter,
  Col100,
  Col33,
  Row,
} from "styles/styledComponents";

interface IFileOptionsModalProps {
  canRemove: boolean;
  fileName: string;
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  onDownload: () => void;
}

const FileOptionsModal: React.FC<IFileOptionsModalProps> = ({
  canRemove,
  fileName,
  isOpen,
  onClose,
  onDelete,
  onDownload,
}: IFileOptionsModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabResources.modalOptionsTitle")}
      >
        <ConfirmDialog
          title={t("searchFindings.tabResources.files.confirm.title")}
        >
          {(confirm): JSX.Element => {
            function onConfirmDelete(): void {
              confirm((): void => {
                onDelete();
              });
            }

            return (
              <React.Fragment>
                <Row>
                  <Col100>
                    <label>
                      {t("searchFindings.tabResources.modalOptionsContent")}
                      <b>{fileName}</b>
                      {"?"}
                    </label>
                  </Col100>
                  <ButtonToolbarCenter>
                    <br />
                    {canRemove ? (
                      <Col33>
                        <Button onClick={onConfirmDelete} variant={"secondary"}>
                          <FontAwesomeIcon icon={faMinus} />
                          &nbsp;
                          {t("searchFindings.tabResources.removeRepository")}
                        </Button>
                      </Col33>
                    ) : undefined}
                    <Col33>
                      <Button onClick={onDownload} variant={"secondary"}>
                        <FontAwesomeIcon icon={faDownload} />
                        &nbsp;
                        {t("searchFindings.tabResources.download")}
                      </Button>
                    </Col33>
                  </ButtonToolbarCenter>
                </Row>
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("confirmmodal.cancel")}
                  </Button>
                </ModalFooter>
              </React.Fragment>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { FileOptionsModal, IFileOptionsModalProps };
