import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { number, object, string } from "yup";

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
  onSubmit: (values: {
    address: string;
    nickname: string;
    port: number;
  }) => Promise<void>;
}

const validations = object().shape({
  address: string().required(),
  nickname: string()
    .required()
    .matches(/^[a-zA-Z_0-9-]{1,128}$/u),
  port: number().required(),
});

const ManagementModal: React.FC<IManagementModalProps> = ({
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal
      headerTitle={t(`group.scope.common.add`)}
      onClose={onClose}
      open={true}
    >
      <Formik
        initialValues={{ address: "", nickname: "", port: 0 }}
        name={"ipRoot"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div className={"flex"}>
              <div className={"w-70 mr3"}>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t("group.scope.ip.address")}
                </ControlLabel>
                <Field component={FormikText} name={"address"} type={"text"} />
              </div>
              <div className={"w-30"}>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t("group.scope.ip.port")}
                </ControlLabel>
                <Field component={FormikText} name={"port"} type={"number"} />
              </div>
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.ip.nickname")}
              </ControlLabel>
              <Field component={FormikText} name={"nickname"} type={"text"} />
            </div>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
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
