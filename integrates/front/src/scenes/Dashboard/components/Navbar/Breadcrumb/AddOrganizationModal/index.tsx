import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { object, string } from "yup";

import { Input, Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ADD_NEW_ORGANIZATION } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";
import type {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/types";
import type { ICountry } from "utils/countries";
import { getCountries } from "utils/countries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const MAX_ORG_LENGTH = 10;
const MIN_ORG_LENGTH = 4;
const tPath = "sidebar.newOrganization.modal.";

const AddOrganizationModal: React.FC<IAddOrganizationModalProps> = ({
  open,
  onClose,
}: IAddOrganizationModalProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();
  const [countries, setCountries] = useState<ICountry[]>([]);

  useEffect((): void => {
    const loadCountries = async (): Promise<void> => {
      setCountries(await getCountries());
    };
    void loadCountries();
  }, [setCountries]);

  // GraphQL Operations
  const [addOrganization, { loading: submitting }] = useMutation(
    ADD_NEW_ORGANIZATION,
    {
      onCompleted: (result: IAddOrganizationMtProps): void => {
        if (result.addOrganization.success) {
          onClose();
          const { name } = result.addOrganization.organization;
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

  function handleSubmit(values: { country: string; name: string }): void {
    mixpanel.track("AddOrganization");
    void addOrganization({
      variables: { country: values.country, name: values.name.toUpperCase() },
    });
  }

  const validations = object().shape({
    country: string().required(t("validations.required")),
    name: string()
      .required(t("validations.required"))
      .min(
        MIN_ORG_LENGTH,
        t("validations.minLength", { count: MIN_ORG_LENGTH })
      )
      .max(
        MAX_ORG_LENGTH,
        t("validations.maxLength", { count: MAX_ORG_LENGTH })
      )
      .matches(/^[a-zA-Z]+$/u, t("validations.alphabetic")),
  });

  // Render Elements
  return (
    <React.StrictMode>
      <Modal onClose={onClose} open={open} title={t(`${tPath}title`)}>
        <Formik
          initialValues={{ country: "", name: "" }}
          name={"newOrganization"}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          <Form>
            <Input label={t(`${tPath}name`)} name={"name"} />
            <div style={{ padding: "7px" }} />
            <Select label={t(`${tPath}country`)} name={"country"}>
              <option value={""}>{""}</option>
              {countries.map(
                (country): JSX.Element => (
                  <option key={country.id} value={country.name}>
                    {country.name}
                  </option>
                )
              )}
            </Select>
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
