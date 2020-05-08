/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for using components with render props
 */

import React from "react";
import { ButtonToolbar, Col, ProgressBar, Row } from "react-bootstrap";
import { Field, InjectedFormProps, Validator } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { fileInputField, textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { isValidFileName, isValidFileSize, maxLength, required, validField } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";

export interface IAddFilesModalProps {
  isOpen: boolean;
  isUploading: boolean;
  uploadProgress: number;
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

const maxFileDescriptionLength: ConfigurableValidator = maxLength(200);
const addFilesModal: React.FC<IAddFilesModalProps> = (props: IAddFilesModalProps): JSX.Element => {
  const handleClose: (() => void) = (): void => { props.onClose(); };
  const handleSubmit: ((values: {}) => void) = (values: {}): void => { props.onSubmit(values); };

  const maxFileSize: Validator = isValidFileSize(100);

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
          {({ pristine }: InjectedFormProps): React.ReactNode => (
            <React.Fragment>
              <Row>
                <Col md={12}>
                  <label>
                    <label style={{ color: "#f22" }}>* </label>
                    {translate.t("validations.file_size", { count: 100 })}
                  </label>
                  <Field
                    component={fileInputField}
                    id="file"
                    name="file"
                    validate={[required, isValidFileName, maxFileSize]}
                  />
                </Col>
                <Col md={12}>
                  <label>
                    <label style={{ color: "#f22" }}>* </label>
                    {translate.t("search_findings.tab_resources.description")}
                  </label>
                  <Field
                    component={textAreaField}
                    name="description"
                    type="text"
                    validate={[required, validField, maxFileDescriptionLength]}
                  />
                </Col>
              </Row>
              {props.isUploading ? renderUploadBar(props) : undefined}
              <br />
              <ButtonToolbar className="pull-right">
                <Button onClick={handleClose} disabled={props.isUploading}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type="submit" disabled={pristine || props.isUploading}>
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
