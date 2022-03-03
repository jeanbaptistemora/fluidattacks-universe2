import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React from "react";
import { useHistory } from "react-router-dom";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import {
  ADD_NEW_ORGANIZATION,
  GET_AVAILABLE_ORGANIZATION_NAME,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/queries";
import type {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
  IAddOrganizationQryProps,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/AddOrganizationModal/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikText } from "utils/forms/fields/";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const AddOrganizationModal: React.FC<IAddOrganizationModalProps> = (
  props: IAddOrganizationModalProps
): JSX.Element => {
  const { open, onClose } = props;

  const { push } = useHistory();

  // GraphQL Operations
  const { data, loading } = useQuery<IAddOrganizationQryProps>(
    GET_AVAILABLE_ORGANIZATION_NAME,
    {
      onError: (error: ApolloError): void => {
        onClose();
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (
            message ===
            "Exception - There are no organization names available at the moment"
          ) {
            msgError(
              translate.t("sidebar.newOrganization.modal.namesUnavailable")
            );
          } else {
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred creating an organization",
              message
            );
          }
        });
      },
    }
  );

  const [addOrganization, { loading: submitting }] = useMutation(
    ADD_NEW_ORGANIZATION,
    {
      onCompleted: (result: IAddOrganizationMtProps): void => {
        if (result.addOrganization.success) {
          onClose();
          track("NewOrganization", {
            OrganizationId: result.addOrganization.organization.id,
            OrganizationName: result.addOrganization.organization.name,
          });
          msgSuccess(
            translate.t("sidebar.newOrganization.modal.success", {
              name: result.addOrganization.organization.name,
            }),
            translate.t("sidebar.newOrganization.modal.successTitle")
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
            msgError(translate.t("sidebar.newOrganization.modal.invalidName"));
          } else {
            msgError(translate.t("groupAlerts.errorTextsad"));
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
    track("AddOrganization");
    void addOrganization({ variables: { name: values.name } });
  }

  const organizationName: string =
    _.isUndefined(data) || _.isEmpty(data) ? "" : data.internalNames.name;

  // Render Elements
  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("sidebar.newOrganization.modal.title")}
        onEsc={onClose}
        open={open}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{ name: organizationName.toUpperCase() }}
          name={"newOrganization"}
          onSubmit={handleSubmit}
        >
          <Form>
            <Row>
              <FormGroup>
                <ControlLabel>
                  {translate.t("sidebar.newOrganization.modal.name")}
                </ControlLabel>
                <TooltipWrapper
                  id={"addOrgTooltip"}
                  message={translate.t(
                    "sidebar.newOrganization.modal.nameTooltip"
                  )}
                  placement={"top"}
                >
                  <Field
                    component={FormikText}
                    disabled={true}
                    name={"name"}
                    type={"text"}
                  />
                </TooltipWrapper>
              </FormGroup>
            </Row>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose} variant={"secondary"}>
                    {translate.t("confirmmodal.cancel")}
                  </Button>
                  <Button
                    disabled={loading || submitting}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {translate.t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddOrganizationModal };
