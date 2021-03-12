import { Button } from "components/Button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Modal } from "components/Modal";
import React from "react";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Col33,
  Row,
} from "styles/styledComponents";
import { faDownload, faMinus } from "@fortawesome/free-solid-svg-icons";

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
        headerTitle={translate.t(
          "search_findings.tabResources.modalOptionsTitle"
        )}
        open={isOpen}
      >
        <Row>
          <Col100>
            <label>
              {translate.t("search_findings.tabResources.modalOptionsContent")}
              <b>{fileName}</b>
              {"?"}
            </label>
          </Col100>
          <ButtonToolbarCenter>
            <br />
            {canRemove ? (
              <Col33>
                <Button onClick={onDelete}>
                  <FontAwesomeIcon icon={faMinus} />
                  &nbsp;
                  {translate.t("search_findings.tabResources.removeRepository")}
                </Button>
              </Col33>
            ) : undefined}
            <Col33>
              <Button onClick={onDownload}>
                <FontAwesomeIcon icon={faDownload} />
                &nbsp;
                {translate.t("search_findings.tabResources.download")}
              </Button>
            </Col33>
          </ButtonToolbarCenter>
        </Row>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClose}>
                {translate.t("confirmmodal.cancel")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { fileOptionsModal as FileOptionsModal, IFileOptionsModalProps };
