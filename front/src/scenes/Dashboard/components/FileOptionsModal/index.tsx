/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for conditional rendering
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import translate from "../../../../utils/translations/translate";

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
        footer={<div />}
      >
        <Row>
          <Col md={12}>
            <label>
              {translate.t("search_findings.tab_resources.modal_options_content")}
              <b>{props.fileName}</b>?
            </label>
          </Col>
          <Col md={12}>
            <br />
            {props.canRemove ? (
              <Col md={4} mdOffset={2} sm={6}>
                <Button block={true} onClick={onDelete}>
                  <Glyphicon glyph="minus" />&nbsp;
                    {translate.t("search_findings.tab_resources.remove_repository")}
                </Button>
              </Col>
            ) : undefined}
            <Col md={4} sm={6}>
              <Button block={true} onClick={onDownload}>
                <Glyphicon glyph="download-alt" />&nbsp;
                  {translate.t("search_findings.tab_resources.download")}
              </Button>
            </Col>
          </Col>
        </Row>
        <ButtonToolbar className="pull-right">
          <Button onClick={onClose}>{translate.t("confirmmodal.cancel")}</Button>
        </ButtonToolbar>
      </Modal>
    </React.StrictMode>
  );
};

export { fileOptionsModal as FileOptionsModal };
