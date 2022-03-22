import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Modal, ModalFooter } from "components/Modal";
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
    <Modal open={open} title={translate.t("legalNotice.title")}>
      <Formik
        initialValues={{ remember: false }}
        name={"acceptLegal"}
        onSubmit={handleSubmit}
      >
        <Form>
          <p>{translate.t("legalNotice.description.legal", { currentYear })}</p>
          <p>
            {translate.t("legalNotice.description.privacy")}
            <ExternalLink href={"https://fluidattacks.com/privacy/"}>
              {translate.t("legalNotice.description.privacyLinkText")}
            </ExternalLink>
          </p>
          <Field
            component={FormikCheckbox}
            label={translate.t("legalNotice.rememberCbo.text")}
            name={"remember"}
            title={translate.t("legalNotice.rememberCbo.tooltip")}
          />
          <ModalFooter>
            <Button
              title={translate.t("legalNotice.acceptBtn.tooltip")}
              type={"submit"}
              variant={"primary"}
            >
              {translate.t("legalNotice.acceptBtn.text")}
            </Button>
          </ModalFooter>
        </Form>
      </Formik>
    </Modal>
  );
};
