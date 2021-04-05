import React, { useCallback } from "react";
import { Field } from "redux-form";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Checkbox } from "utils/forms/fields";
import { translate } from "utils/translations/translate";

interface ICompulsoryNoticeProps {
  content: string;
  open: boolean;
  onAccept: (remember: boolean) => void;
}

export const CompulsoryNotice: React.FC<ICompulsoryNoticeProps> = (
  props: ICompulsoryNoticeProps
): JSX.Element => {
  const { open, content, onAccept } = props;

  const handleSubmit: (values: { remember: boolean }) => void = useCallback(
    (values: { remember: boolean }): void => {
      onAccept(values.remember);
    },
    [onAccept]
  );

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
