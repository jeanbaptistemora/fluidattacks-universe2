import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Input } from "components/Input";
import { ModalConfirm } from "components/Modal";
import type { IURLRootAttr } from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeInputsView/HandleAdditionModal/types";

interface IManagementModalProps {
  initialValues: IURLRootAttr;
  isEditing: boolean;
  onClose: () => void;
  onSubmit: (values: {
    id: string;
    nickname: string;
    url: string;
  }) => Promise<void>;
}

const validations = object().shape({
  nickname: string()
    .required()
    .matches(/^[a-zA-Z_0-9-]{1,128}$/u),
  url: string().required(),
});

const ManagementModal: React.FC<IManagementModalProps> = ({
  initialValues,
  isEditing,
  onClose,
  onSubmit,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Formik
        initialValues={{
          id: initialValues.id,
          nickname: initialValues.nickname,
          url: initialValues.host,
        }}
        name={"urlRoot"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <Input
                disabled={isEditing}
                label={t("group.scope.url.url")}
                name={"url"}
                type={"text"}
              />
            </div>
            <div>
              <Input
                label={t("group.scope.url.nickname")}
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
    </React.StrictMode>
  );
};

export { ManagementModal };
