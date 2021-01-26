import { Button } from "components/Button";
import { Checkbox } from "utils/forms/fields";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Modal } from "components/Modal";
import React from "react";
import { translate } from "utils/translations/translate";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface ICompulsoryNoticeProps {
  content: string;
  open: boolean;
  onAccept: (remember: boolean) => void;
}

export const CompulsoryNotice: React.FC<ICompulsoryNoticeProps> = (
  props: ICompulsoryNoticeProps
): JSX.Element => {
  const { open, content, onAccept } = props;

  function handleSubmit(values: { remember: boolean }): void {
    onAccept(values.remember);
  }

  return (
    <Modal headerTitle={translate.t("legalNotice.title")} open={open}>
      <GenericForm
        initialValues={{ remember: false }}
        name={"acceptLegal"}
        onSubmit={handleSubmit}
      >
        <React.Fragment>
          <p>{content}</p>
          <Field
            component={Checkbox}
            name={"remember"}
            title={translate.t("legalNotice.rememberCbo.tooltip")}
          >
            {translate.t("legalNotice.rememberCbo.text")}
          </Field>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button
                  title={translate.t("legalNotice.acceptBtn.tooltip")}
                  type={"submit"}
                >
                  {translate.t("legalNotice.acceptBtn.text")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </React.Fragment>
      </GenericForm>
    </Modal>
  );
};
