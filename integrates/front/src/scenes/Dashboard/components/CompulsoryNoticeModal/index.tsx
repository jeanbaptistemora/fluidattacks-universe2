import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Modal, ModalFooter } from "components/Modal";
import { FormikCheckbox } from "utils/forms/fields";

interface ICompulsoryNoticeProps {
  open: boolean;
  onAccept: (remember: boolean) => void;
}

export const CompulsoryNotice: React.FC<ICompulsoryNoticeProps> = ({
  open,
  onAccept,
}: ICompulsoryNoticeProps): JSX.Element => {
  const { t } = useTranslation();
  const currentYear: number = new Date().getFullYear();

  const handleSubmit = useCallback(
    (values: { remember: boolean }): void => {
      onAccept(values.remember);
    },
    [onAccept]
  );

  return (
    <Modal open={open} title={t("legalNotice.title")}>
      <Formik
        initialValues={{ remember: false }}
        name={"acceptLegal"}
        onSubmit={handleSubmit}
      >
        <Form>
          <p>{t("legalNotice.description.legal", { currentYear })}</p>
          <p>
            {t("legalNotice.description.privacy")}
            <ExternalLink href={"https://fluidattacks.com/privacy/"}>
              {t("legalNotice.description.privacyLinkText")}
            </ExternalLink>
          </p>
          <Field
            component={FormikCheckbox}
            label={t("legalNotice.rememberCbo.text")}
            name={"remember"}
            title={t("legalNotice.rememberCbo.tooltip")}
          />
          <ModalFooter>
            <Button
              title={t("legalNotice.acceptBtn.tooltip")}
              type={"submit"}
              variant={"primary"}
            >
              {t("legalNotice.acceptBtn.text")}
            </Button>
          </ModalFooter>
        </Form>
      </Formik>
    </Modal>
  );
};
