import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IManagementModalProps {
  onClose: () => void;
  onSubmit: (values: { url: string }) => Promise<void>;
}

const validations = object().shape({
  url: string().required(),
});

const ManagementModal: React.FC<IManagementModalProps> = ({
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal headerTitle={t(`group.scope.common.add`)} open={true}>
      <Formik
        initialValues={{ url: "" }}
        name={"urlRoot"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <React.Fragment>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.url.url")}
              </ControlLabel>
              <Field component={FormikText} name={"url"} type={"text"} />
            </React.Fragment>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
                  <Button disabled={!dirty || isSubmitting} type={"submit"}>
                    {t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { ManagementModal };
