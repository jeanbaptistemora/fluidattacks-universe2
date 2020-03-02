/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for using components with render props
 */

import React from "react";
import { ButtonToolbar, Col, ProgressBar, Row } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { fileInputField, textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";

export interface IAddFilesModalProps {
  isOpen: boolean;
  showUploadProgress?: boolean;
  uploadProgress?: number;
  onClose(): void;
  onSubmit(values: {}): void;
}

const renderUploadBar: ((props: IAddFilesModalProps) => JSX.Element) = (props: IAddFilesModalProps): JSX.Element => (
  <React.Fragment>
    <br />
    {translate.t("search_findings.tab_resources.uploading_progress")}
    <ProgressBar active={true} now={props.uploadProgress} label={`${props.uploadProgress}%`} />
  </React.Fragment>
);

const addFilesModal: React.FC<IAddFilesModalProps> = (props: IAddFilesModalProps): JSX.Element => {
  const handleClose: (() => void) = (): void => { props.onClose(); };
  const handleSubmit: ((values: {}) => void) = (values: {}): void => { props.onSubmit(values); };

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_resources.modal_file_title")}
        footer={<div />}
      >
        <GenericForm
          name="addFiles"
          onSubmit={handleSubmit}
        >
          {({ pristine, submitting }: InjectedFormProps): React.ReactNode => (
            <React.Fragment>
              <Row>
                <Col md={12}>
                  <label>
                    <label style={{ color: "#f22" }}>* </label>
                    {translate.t("validations.file_size", { count: 100 })}
                  </label>
                  <Field component={fileInputField} id="file" name="file" validate={required} />
                </Col>
                <Col md={12}>
                  <label>
                    <label style={{ color: "#f22" }}>* </label>
                    {translate.t("search_findings.tab_resources.description")}
                  </label>
                  <Field name="description" component={textAreaField} type="text" validate={[required]} />
                </Col>
              </Row>
              {props.showUploadProgress === true ? renderUploadBar(props) : undefined}
              <br />
              <ButtonToolbar className="pull-right">
                <Button bsStyle="default" onClick={handleClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button bsStyle="primary" type="submit" disabled={pristine || submitting}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { addFilesModal as AddFilesModal };
