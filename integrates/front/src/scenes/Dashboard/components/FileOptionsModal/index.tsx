import { faDownload, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { Modal, ModalFooter } from "components/Modal";
import {
  ButtonToolbarCenter,
  Col100,
  Col33,
  Row,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IFileOptionsModalProps {
  canRemove: boolean;
  fileName: string;
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  onDownload: () => void;
}

const fileOptionsModal: React.FC<IFileOptionsModalProps> = (
  props: IFileOptionsModalProps
): JSX.Element => {
  const { canRemove, fileName, isOpen, onClose, onDelete, onDownload } = props;

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={translate.t("searchFindings.tabResources.modalOptionsTitle")}
      >
        <ConfirmDialog
          title={translate.t("searchFindings.tabResources.files.confirm.title")}
        >
          {(confirm: IConfirmFn): JSX.Element => {
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
                      {translate.t(
                        "searchFindings.tabResources.modalOptionsContent"
                      )}
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
                          {translate.t(
                            "searchFindings.tabResources.removeRepository"
                          )}
                        </Button>
                      </Col33>
                    ) : undefined}
                    <Col33>
                      <Button onClick={onDownload} variant={"secondary"}>
                        <FontAwesomeIcon icon={faDownload} />
                        &nbsp;
                        {translate.t("searchFindings.tabResources.download")}
                      </Button>
                    </Col33>
                  </ButtonToolbarCenter>
                </Row>
                <div>
                  <div>
                    <ModalFooter>
                      <Button onClick={onClose} variant={"secondary"}>
                        {translate.t("confirmmodal.cancel")}
                      </Button>
                    </ModalFooter>
                  </div>
                </div>
              </React.Fragment>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { fileOptionsModal as FileOptionsModal, IFileOptionsModalProps };
