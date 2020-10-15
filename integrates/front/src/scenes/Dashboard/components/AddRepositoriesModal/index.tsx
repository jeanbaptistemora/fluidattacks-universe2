/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { Glyphicon } from "react-bootstrap";
import { Field, FieldArray, InjectedFormProps, WrappedFieldArrayProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button/index";
import { Modal } from "components/Modal/index";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col25,
  Col45,
  Col60,
  ControlLabel,
  RemoveItem,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Dropdown, Text } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { maxLength, required, validField } from "utils/validations";

export interface IAddRepositoriesModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

const maxRepoUrlLength: ConfigurableValidator = maxLength(300);
const maxRepoBranchLength: ConfigurableValidator = maxLength(30);
const renderReposFields: React.FC<WrappedFieldArrayProps> = (props: WrappedFieldArrayProps): JSX.Element => {
  const addItem: (() => void) = (): void => {
    props.fields.push({ urlRepo: "", branch: "" });
  };

  return (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => {
        const removeItem: (() => void) = (): void => { props.fields.remove(index); };

        return (
          <React.Fragment key={index}>
            {index > 0 ? <React.Fragment><br /><hr /></React.Fragment> : undefined}
            <Row>
              <Col25>
                <TooltipWrapper
                  message={translate.t("search_findings.tab_resources.protocol.tooltip")}
                  placement="top"
                >
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("search_findings.tab_resources.protocol.label")}
                  </ControlLabel>
                </TooltipWrapper>
                <Field name={`${fieldName}.protocol`} component={Dropdown} validate={[required]} >
                  <option value="" selected={true} />
                  <option value="HTTPS">{translate.t("search_findings.tab_resources.https")}</option>
                  <option value="SSH">{translate.t("search_findings.tab_resources.ssh")}</option>
                </Field>
              </Col25>
              <Col60>
                <TooltipWrapper
                  message={translate.t("search_findings.tab_resources.repository.tooltip")}
                  placement="top"
                >
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("search_findings.tab_resources.repository.label")}
                  </ControlLabel>
                </TooltipWrapper>
                <Field
                  name={`${fieldName}.urlRepo`}
                  component={Text}
                  placeholder={translate.t("search_findings.tab_resources.base_url_placeholder")}
                  type="text"
                  validate={[required, validField, maxRepoUrlLength]}
                />
              </Col60>
            </Row>
            <Row>
              <Col45>
                <TooltipWrapper
                  message={translate.t("search_findings.tab_resources.branch.tooltip")}
                  placement="top"
                >
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("search_findings.tab_resources.branch.label")}
                  </ControlLabel>
                </TooltipWrapper>
                <Field
                  name={`${fieldName}.branch`}
                  component={Text}
                  placeholder={translate.t("search_findings.tab_resources.branch_placeholder")}
                  type="text"
                  validate={[required, validField, maxRepoBranchLength]}
                />
              </Col45>
              {index > 0 ? (
                <RemoveItem>
                  <TooltipWrapper
                    message={translate.t("search_findings.tab_resources.modal_trash_btn.tooltip")}
                    placement="top"
                  >
                    <Button onClick={removeItem}>
                      <Glyphicon glyph="trash" />
                    </Button>
                  </TooltipWrapper>
                </RemoveItem>
              ) : undefined}
            </Row>
          </React.Fragment>
        );
      })}
      <br />
      <TooltipWrapper
        message={translate.t("search_findings.tab_resources.modal_plus_btn.tooltip")}
        placement="top"
      >
        <Button onClick={addItem}>
          <Glyphicon glyph="plus" />
        </Button>
      </TooltipWrapper>
    </React.Fragment>
  );
};

const addRepositoriesModal: React.FC<IAddRepositoriesModalProps> = (props: IAddRepositoriesModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_resources.modal_repo_title")}
        footer={<div />}
      >
        <GenericForm
          name="addRepos"
          initialValues={{ resources: [{ urlRepo: "", branch: "" }] }}
          onSubmit={onSubmit}
        >
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray name="resources" component={renderReposFields} />
              <ButtonToolbar>
                <Button onClick={onClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type="submit" disabled={pristine}>
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

export { addRepositoriesModal as AddRepositoriesModal };
