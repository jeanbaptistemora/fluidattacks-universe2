/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { object, string } from "yup";

import { Input } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ADD_NEW_ORGANIZATION } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";
import type {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const tPath = "sidebar.newOrganization.modal.";

const AddOrganizationModal: React.FC<IAddOrganizationModalProps> = ({
  open,
  onClose,
}: IAddOrganizationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const { push } = useHistory();

  // GraphQL Operations
  const [addOrganization, { loading: submitting }] = useMutation(
    ADD_NEW_ORGANIZATION,
    {
      onCompleted: (result: IAddOrganizationMtProps): void => {
        if (result.addOrganization.success) {
          onClose();
          const { id, name } = result.addOrganization.organization;
          mixpanel.track("NewOrganization", {
            OrganizationId: id,
            OrganizationName: name,
          });
          msgSuccess(t(`${tPath}success`, { name }), t(`${tPath}successTitle`));
          push(`/orgs/${name.toLowerCase()}/`);
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (message === "Invalid name") {
            msgError(t(`${tPath}invalidName`));
          } else if (message === "Name taken") {
            msgError(t(`${tPath}nameTaken`));
          } else if (
            message ===
            "Exception - The action is not allowed during the free trial"
          ) {
            msgError(t(`${tPath}trial`));
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
    }
  );

  function handleSubmit(values: { name: string }): void {
    mixpanel.track("AddOrganization");
    void addOrganization({ variables: { name: values.name.toUpperCase() } });
  }

  const minLenth = 4;
  const maxLength = 10;
  const validations = object().shape({
    name: string()
      .required()
      .min(minLenth)
      .max(maxLength)
      .matches(/^[a-zA-Z]+$/u),
  });

  // Render Elements
  return (
    <React.StrictMode>
      <Modal onClose={onClose} open={open} title={t(`${tPath}title`)}>
        <Formik
          enableReinitialize={true}
          initialValues={{ name: "" }}
          name={"newOrganization"}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          <Form>
            <Input name={"name"} placeholder={t(`${tPath}name`)} />
            <ModalConfirm
              disabled={submitting}
              onCancel={onClose}
              onConfirm={"submit"}
            />
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddOrganizationModal };
