/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { ButtonToolbar, Col, ProgressBar, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import {
  ConfigProps, DecoratedComponentClass, Field,
  FieldArray, GenericFieldArray, InjectedFormProps,
  reduxForm,
  WrappedFieldArrayProps,
} from "redux-form";
import { Button } from "../../../../components/Button/index";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import { textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { fileInput as FileInput } from "../../components/FileInput/index";

export interface IAddResourcesModalProps {
  isOpen: boolean;
  showUploadProgress?: boolean;
  type: "repository" | "file";
  uploadProgress?: number;
  onClose(): void;
  onSubmit(values: {}): void;
}

/* This is necessary because there is a problem with the type of FieldArray in redux-form library,
* this is the issue: https://github.com/DefinitelyTyped/DefinitelyTyped/issues/32858#issuecomment-461441222
*/
/* tslint:disable-next-line:variable-name
* Disabling here is necessary due a conflict
* between lowerCamelCase var naming rule from tslint
* and PascalCase rule for naming JSX elements
*/
const FieldArrayCustom: new () => GenericFieldArray<Field<React.InputHTMLAttributes<HTMLInputElement> |
  React.SelectHTMLAttributes<HTMLSelectElement> | React.TextareaHTMLAttributes<HTMLTextAreaElement>>,
  WrappedFieldArrayProps<undefined>> = FieldArray as new () =>
  GenericFieldArray<Field, WrappedFieldArrayProps<undefined>>;

type formProps = IAddResourcesModalProps & InjectedFormProps<{}, IAddResourcesModalProps>;

const renderFilesFields: ((props: WrappedFieldArrayProps<undefined>) => JSX.Element) =
    (props: WrappedFieldArrayProps<undefined>): JSX.Element => (
      <React.Fragment>
        {props.fields.map((fieldName: string) => (
          <Row>
            <Col md={12}>
              <div>
                <FileInput fileName="" fileSize={100} icon="search" id="file" type="" visible={true}/>
              </div>
            </Col>
            <Col md={12}>
              <label>
                <label style={{ color: "#f22" }}>* </label>
                {translate.t("search_findings.tab_resources.description")}
              </label>
              <Field name={`${fieldName}.description`} component={textAreaField} type="text" validate={[required]} />
            </Col>
          </Row>
        ))}
      </React.Fragment>
    );

const renderFooter: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <ButtonToolbar className="pull-right">
        <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
          {translate.t("confirmmodal.cancel")}
        </Button>
        <Button bsStyle="primary" type="submit" disabled={props.pristine || props.submitting}>
          {translate.t("confirmmodal.proceed")}
        </Button>
      </ButtonToolbar>
    </React.Fragment>
  );

const renderFilesForm: ((props: formProps) => JSX.Element) =
    (props: formProps): JSX.Element => (
      <React.Fragment>
        <form onSubmit={props.handleSubmit}>
          <FieldArrayCustom name="resources" component={renderFilesFields} />
          { props.showUploadProgress === true ?
            <React.Fragment>
              <br />
              {translate.t("search_findings.tab_resources.uploading_progress")}
              <ProgressBar active={true} now={props.uploadProgress} label={`${props.uploadProgress}%`} />
            </React.Fragment>
            : undefined
          }
          <br />
          {renderFooter(props)}
        </form>
        <br />
      </React.Fragment>
    );

type resourcesForm =
  DecoratedComponentClass<{}, IAddResourcesModalProps & Partial<ConfigProps<{}, IAddResourcesModalProps>>, string>;

/* tslint:disable:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */

const FilesForm: resourcesForm = reduxForm<{}, IAddResourcesModalProps>({
  enableReinitialize: true,
  form: "addFiles",
  initialValues: {
    resources: [{ fileName: "", description: ""}],
  },
  onSubmitFail: focusError,
})(renderFilesForm);
// tslint:enable:variable-name

export const addResourcesModal: React.FC<IAddResourcesModalProps> =
  (props: IAddResourcesModalProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={translate.t("search_findings.tab_resources.modal_file_title")}
          content={<FilesForm {...props} />}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
