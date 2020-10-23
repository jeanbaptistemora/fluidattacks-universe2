/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for conditional rendering
 */

import React from "react";
import { Glyphicon } from "react-bootstrap";

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
                  <Glyphicon glyph="minus" />&nbsp;
                    {translate.t("search_findings.tab_resources.remove_repository")}
                </Button>
              </Col33>
            ) : undefined}
            <Col33>
              <Button onClick={onDownload}>
                <Glyphicon glyph="download-alt" />&nbsp;
                  {translate.t("search_findings.tab_resources.download")}
              </Button>
            </Col33>
          </ButtonToolbarCenter>
        </Row>
        <ButtonToolbar>
          <Button onClick={onClose}>{translate.t("confirmmodal.cancel")}</Button>
        </ButtonToolbar>
      </Modal>
    </React.StrictMode>
  );
};

export { fileOptionsModal as FileOptionsModal };
