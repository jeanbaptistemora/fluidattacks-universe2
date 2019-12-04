/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import {
  ConfigProps, DecoratedComponentClass, InjectedFormProps,
  reduxForm,
} from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import translate from "../../../../utils/translations/translate";

export interface IFileOptionsModalProps {
  canRemove: boolean;
  fileName: string;
  isOpen: boolean;
  onClose(): void;
  onDelete(): void;
  onDownload(): void;
  onSubmit(values: {}): void;
}

type formProps = IFileOptionsModalProps & InjectedFormProps<{}, IFileOptionsModalProps>;

const renderFilesFields: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
      <React.Fragment>
          <Row>
            <Col md={12}>
              <label>
                {translate.t("search_findings.tab_resources.modal_options_content")}
                <b>{props.fileName}</b>?
              </label>
            </Col>
            <Col md={12}>
              <br />
              <Col md={4} mdOffset={2} sm={6}>
                {props.canRemove ?
                <Button
                  id="removeFiles"
                  block={true}
                  bsStyle="primary"
                  onClick={(): void => {props.onDelete(); }}
                >
                  <Glyphicon glyph="minus"/>&nbsp;
                  {translate.t("search_findings.tab_resources.remove_repository")}
                </Button> : undefined}
              </Col>
              <Col md={4} sm={6}>
                <Button
                  id="downloadFile"
                  block={true}
                  bsStyle="primary"
                  onClick={(): void => { props.onDownload(); }}
                >
                  <Glyphicon glyph="download-alt"/>&nbsp;
                  {translate.t("search_findings.tab_resources.download")}
                </Button>
              </Col>
            </Col>
          </Row>
      </React.Fragment>
    );

const renderFooter: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <ButtonToolbar className="pull-right">
        <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
          {translate.t("confirmmodal.cancel")}
        </Button>
      </ButtonToolbar>
    </React.Fragment>
  );

const renderFilesForm: ((props: formProps) => JSX.Element) =
    (props: formProps): JSX.Element => (
      <React.Fragment>
        <form onSubmit={props.handleSubmit}>
          {renderFilesFields(props)}
          <br />
          {renderFooter(props)}
        </form>
        <br />
      </React.Fragment>
    );

type resourcesForm =
  DecoratedComponentClass<{}, IFileOptionsModalProps & Partial<ConfigProps<{}, IFileOptionsModalProps>>, string>;

/* tslint:disable:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const FilesForm: resourcesForm = reduxForm<{}, IFileOptionsModalProps>({
  enableReinitialize: true,
  form: "downloadFile",
  initialValues: {
    resources: [{ fileName: "", description: "" }],
  },
  onSubmitFail: focusError,
})(renderFilesForm);
// tslint:enable:variable-name

export const fileOptionsModal: React.FC<IFileOptionsModalProps> =
  (props: IFileOptionsModalProps): JSX.Element => {
    let title: string;
    let content: JSX.Element;
    title = "search_findings.tab_resources.modal_options_title";
    content = <FilesForm {...props} />;

    return (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={translate.t(title)}
          content={content}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  ); };
