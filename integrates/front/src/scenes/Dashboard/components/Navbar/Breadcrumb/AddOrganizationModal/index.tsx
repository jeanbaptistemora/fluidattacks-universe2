import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { ADD_NEW_ORGANIZATION } from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";
import type {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/types";
import { ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields/";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

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
          mixpanel.track("NewOrganization", {
            OrganizationId: result.addOrganization.organization.id,
            OrganizationName: result.addOrganization.organization.name,
          });
          msgSuccess(
            t("sidebar.newOrganization.modal.success", {
              name: result.addOrganization.organization.name,
            }),
            t("sidebar.newOrganization.modal.successTitle")
          );
          push(
            `/orgs/${result.addOrganization.organization.name.toLowerCase()}/`
          );
        }
      },
      onError: (error: ApolloError): void => {
        onClose();
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (message === "Access denied") {
            msgError(t("sidebar.newOrganization.modal.invalidName"));
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
      <Modal
        onClose={onClose}
        open={open}
        title={t("sidebar.newOrganization.modal.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{ name: "" }}
          name={"newOrganization"}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          <Form>
            <Row>
              <FormGroup>
                <ControlLabel>
                  {t("sidebar.newOrganization.modal.name")}
                </ControlLabel>
                <TooltipWrapper
                  id={"addOrgTooltip"}
                  message={t("sidebar.newOrganization.modal.nameTooltip")}
                  placement={"top"}
                >
                  <Field component={FormikText} name={"name"} type={"text"} />
                </TooltipWrapper>
              </FormGroup>
            </Row>
            <ModalFooter>
              <Button onClick={onClose} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Button disabled={submitting} type={"submit"} variant={"primary"}>
                {t("confirmmodal.proceed")}
              </Button>
            </ModalFooter>
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddOrganizationModal };
