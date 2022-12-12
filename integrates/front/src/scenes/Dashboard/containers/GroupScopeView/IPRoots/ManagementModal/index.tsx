import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IIPRootAttr } from "../../types";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IManagementModalProps {
  initialValues: IIPRootAttr | undefined;
  onClose: () => void;
  onSubmit: (values: {
    address: string;
    id: string;
    nickname: string;
  }) => Promise<void>;
}

const validations = object().shape({
  address: string().required(),
  nickname: string()
    .required()
    .matches(/^[a-zA-Z_0-9-]{1,128}$/u),
});

const ManagementModal: React.FC<IManagementModalProps> = ({
  initialValues = {
    __typename: "IPRoot",
    address: "",
    id: "",
    nickname: "",
    state: "ACTIVE",
  },
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();
  const isEditing: boolean = initialValues.address !== "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
    >
      <Formik
        initialValues={initialValues}
        name={"ipRoot"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.ip.address")}
              </ControlLabel>
              <Field
                component={FormikText}
                disabled={isEditing}
                name={"address"}
                type={"text"}
              />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.ip.nickname")}
              </ControlLabel>
              <Field component={FormikText} name={"nickname"} type={"text"} />
            </div>
            <ModalConfirm
              disabled={!dirty || isSubmitting}
              onCancel={onClose}
            />
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { ManagementModal };
