import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { translate } from "utils/translations/translate";

interface ICompulsoryNoticeProps {
  open: boolean;
  onAccept: (remember: boolean) => void;
}

export const CompulsoryNotice: React.FC<ICompulsoryNoticeProps> = (
  props: ICompulsoryNoticeProps
): JSX.Element => {
  const { open, onAccept } = props;

  const currentYear: number = new Date().getFullYear();

  const handleSubmit: (values: { remember: boolean }) => void = useCallback(
    (values: { remember: boolean }): void => {
      onAccept(values.remember);
    },
    [onAccept]
  );

  return (
    <Modal headerTitle={translate.t("legalNotice.title")} open={open}>
      <Formik
        initialValues={{ remember: false }}
        name={"acceptLegal"}
        onSubmit={handleSubmit}
      >
        <Form>
          <p>{translate.t("legalNotice.description.legal", { currentYear })}</p>
          <p>
            {translate.t("legalNotice.description.privacy")}
            <a
              href={"https://fluidattacks.com/privacy/"}
              rel={"noopener noreferrer"}
              target={"_blank"}
            >
              {translate.t("legalNotice.description.privacyLinkText")}
            </a>
          </p>
          <Field
            component={FormikCheckbox}
            label={translate.t("legalNotice.rememberCbo.text")}
            name={"remember"}
            title={translate.t("legalNotice.rememberCbo.tooltip")}
          />
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
        </Form>
      </Formik>
    </Modal>
  );
};
