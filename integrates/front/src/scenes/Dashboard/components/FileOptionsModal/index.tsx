/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for conditional rendering
 */
import { faDownload, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Col33,
  Row,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";

export interface IFileOptionsModalProps {
  canRemove: boolean;
  fileName: string;
  isOpen: boolean;
  onClose(): void;
  onDelete(): void;
  onDownload(): void;
}

const fileOptionsModal: React.FC<IFileOptionsModalProps> = (props: IFileOptionsModalProps): JSX.Element => {
  const { onClose, onDelete, onDownload } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_resources.modal_options_title")}
      >
        <Row>
          <Col100>
            <label>
              {translate.t("search_findings.tab_resources.modal_options_content")}
              <b>{props.fileName}</b>?
            </label>
          </Col100>
          <ButtonToolbarCenter>
            <br />
            {props.canRemove ? (
              <Col33>
                <Button onClick={onDelete}>
                  <FontAwesomeIcon icon={faMinus} />&nbsp;
                    {translate.t("search_findings.tab_resources.remove_repository")}
                </Button>
              </Col33>
            ) : undefined}
            <Col33>
              <Button onClick={onDownload}>
                <FontAwesomeIcon icon={faDownload} />&nbsp;
                  {translate.t("search_findings.tab_resources.download")}
              </Button>
            </Col33>
          </ButtonToolbarCenter>
        </Row>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClose}>{translate.t("confirmmodal.cancel")}</Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { fileOptionsModal as FileOptionsModal };
