import { Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { ExternalLink } from "components/ExternalLink";
import { Checkbox } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";

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
          <Checkbox
            label={t("legalNotice.rememberCbo.text")}
            name={"remember"}
            tooltip={t("legalNotice.rememberCbo.tooltip")}
          />
          <ModalConfirm txtConfirm={t("legalNotice.accept")} />
        </Form>
      </Formik>
    </Modal>
  );
};
