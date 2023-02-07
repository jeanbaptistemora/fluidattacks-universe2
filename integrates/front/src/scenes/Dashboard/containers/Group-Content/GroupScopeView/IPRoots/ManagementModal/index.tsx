import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IIPRootAttr } from "../../types";
import { Input } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";

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
              <Input
                disabled={isEditing}
                label={t("group.scope.ip.address")}
                name={"address"}
                type={"text"}
              />
            </div>
            <div>
              <Input
                label={t("group.scope.ip.nickname")}
                name={"nickname"}
                type={"text"}
              />
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
