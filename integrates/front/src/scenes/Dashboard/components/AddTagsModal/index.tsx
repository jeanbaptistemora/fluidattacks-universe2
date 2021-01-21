import { Button } from "components/Button";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Glyphicon } from "react-bootstrap";
import { Modal } from "components/NewModal";
import React from "react";
import { Text } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbar,
  Col100,
  Col80,
  ControlLabel,
  RemoveTag,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Field, FieldArray } from "redux-form";
import type { InjectedFormProps, WrappedFieldArrayProps } from "redux-form";
import { required, validTag } from "utils/validations";

interface IAddTagsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { tags: string[] }) => void;
}

const renderTagsFields: React.FC<WrappedFieldArrayProps> = (
  props: WrappedFieldArrayProps
): JSX.Element => {
  function addItem(): void {
    // eslint-disable-next-line fp/no-mutating-methods
    props.fields.push("");
  }

  return (
    <React.Fragment>
      {props.fields.map(
        (fieldName: string, index: number): JSX.Element => {
          function removeItem(): void {
            props.fields.remove(index);
          }

          return (
            <React.Fragment key={fieldName + String(index)}>
              {index > 0 ? (
                <React.Fragment>
                  <br />
                  <hr />
                </React.Fragment>
              ) : undefined}
              <Row>
                <Col80>
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {"Tag"}
                  </ControlLabel>
                  <Field
                    component={Text}
                    name={fieldName}
                    type={"text"}
                    validate={[required, validTag]}
                  />
                </Col80>
                {index > 0 ? (
                  <RemoveTag>
                    <Button onClick={removeItem}>
                      <Glyphicon glyph={"trash"} />
                    </Button>
                  </RemoveTag>
                ) : undefined}
              </Row>
            </React.Fragment>
          );
        }
      )}
      <br />
      <Button onClick={addItem}>
        <Glyphicon glyph={"plus"} />
      </Button>
    </React.Fragment>
  );
};

const AddTagsModal: React.FC<IAddTagsModalProps> = (
  props: IAddTagsModalProps
): JSX.Element => {
  const { isOpen, onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "search_findings.tab_indicators.tags.modal_title"
        )}
        open={isOpen}
      >
        <GenericForm
          initialValues={{ tags: [""] }}
          name={"addTags"}
          onSubmit={onSubmit}
        >
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray component={renderTagsFields} name={"tags"} />
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"portfolio-add-cancel"} onClick={onClose}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={pristine}
                      id={"portfolio-add-proceed"}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { AddTagsModal, IAddTagsModalProps };
