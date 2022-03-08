import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IManagementModalProps {
  onClose: () => void;
  onSubmit: (values: { nickname: string; url: string }) => Promise<void>;
}

const validations = object().shape({
  nickname: string()
    .required()
    .matches(/^[a-zA-Z_0-9-]{1,128}$/u),
  url: string().required(),
});

const ManagementModal: React.FC<IManagementModalProps> = ({
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal onClose={onClose} open={true} title={t(`group.scope.common.add`)}>
      <Formik
        initialValues={{ nickname: "", url: "" }}
        name={"urlRoot"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.url.url")}
              </ControlLabel>
              <Field component={FormikText} name={"url"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.url.nickname")}
              </ControlLabel>
              <Field component={FormikText} name={"nickname"} type={"text"} />
            </div>
            <div>
              <div>
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("confirmmodal.cancel")}
                  </Button>
                  <Button
                    disabled={!dirty || isSubmitting}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ModalFooter>
              </div>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { ManagementModal };
