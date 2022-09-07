/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { number, object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import type { IIPRootAttr } from "scenes/Dashboard/containers/GroupToeInputsView/HandleAdditionModal/types";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IManagementModalProps {
  initialValues: IIPRootAttr | undefined;
  onClose: () => void;
  onSubmit: (values: {
    address: string;
    id: string;
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
  initialValues = {
    __typename: "IPRoot",
    address: "",
    id: "",
    nickname: "",
    port: 0,
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
            <div className={"flex"}>
              <div className={"w-70 mr3"}>
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
              <div className={"w-30"}>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t("group.scope.ip.port")}
                </ControlLabel>
                <Field
                  component={FormikText}
                  disabled={isEditing}
                  name={"port"}
                  type={"number"}
                />
              </div>
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
