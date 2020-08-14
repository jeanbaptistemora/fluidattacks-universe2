import { useLazyQuery, useMutation } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import { Field } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Text } from "../../../../utils/forms/fields";
import Logger from "../../../../utils/logger";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../GenericForm/index";
import { CREATE_NEW_ORGANIZATION, GET_AVAILABLE_ORGANIZATION_NAME } from "./queries";
import { IAddOrganizationModalProps, IAddOrganizationMtResult, IAddOrganizationQryResult } from "./types";

const addOrganizationModal: React.FC<IAddOrganizationModalProps> =
    (props: IAddOrganizationModalProps): JSX.Element => {
  const isModalOpen: boolean = props.open;
  const closeModal: () => void = (): void => { props.onClose(); };

  const { userName } = window as typeof window & Dictionary<string>;
  const { push } = useHistory();

  // GraphQL Operations
  const [getName, { data, loading }] = useLazyQuery(GET_AVAILABLE_ORGANIZATION_NAME, {
    onError: (error: ApolloError): void => {
      closeModal();
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - There are no organization names available at the moment":
            msgError(translate.t("sidebar.newOrganization.modal.namesUnavailable"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred creating an organization", message);
        }
      });
    },
  });

  const [createOrganization, { loading: submitting }] = useMutation(CREATE_NEW_ORGANIZATION, {
    onCompleted: (result: IAddOrganizationMtResult): void => {
      if (result.createOrganization.success) {
        closeModal();
        mixpanel.track("NewOrganization", {
          OrganizationId: result.createOrganization.organization.id,
          OrganizationName: result.createOrganization.organization.name,
          User: userName,
        });
        msgSuccess(
          translate.t("sidebar.newOrganization.modal.success", { name: result.createOrganization.organization.name }),
          translate.t("sidebar.newOrganization.modal.successTitle"),
        );
        push(`/orgs/${result.createOrganization.organization.name.toLowerCase()}/`);
      }
    },
    onError: (error: ApolloError): void => {
      closeModal();
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Organization name is invalid":
            msgError(translate.t("sidebar.newOrganization.modal.invalidName"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred creating new organization", message);
        }
      });
    },
  });

  // Auxiliary Functions
  const handleSubmit: (values: { name: string }) => void = (values: { name: string }): void => {
    createOrganization({ variables: { name: values.name }});
  };

  const organizationName: string = _.isUndefined(data) || _.isEmpty(data)
    ? ""
    : data.internalNames.name;

  // Render Elements
  return (
    <React.StrictMode>
      <React.Fragment>
        <Modal
          footer={<div />}
          headerTitle={translate.t("sidebar.newOrganization.modal.title")}
          open={isModalOpen}
          onOpen={getName}
        >
          <GenericForm
            initialValues={{ name: organizationName.toUpperCase() }}
            name="newOrganization"
            onSubmit={handleSubmit}
          >
            <Row>
              <Col md={12} sm={12}>
                <FormGroup>
                  <ControlLabel>
                    {translate.t("sidebar.newOrganization.modal.name")}
                  </ControlLabel>
                  <TooltipWrapper
                    message={translate.t("sidebar.newOrganization.modal.nameTooltip")}
                    placement="top"
                  >
                    <Field
                      component={Text}
                      disabled={true}
                      name="name"
                      type="text"
                    />
                  </TooltipWrapper>
                </FormGroup>
              </Col>
            </Row>
            <ButtonToolbar className="pull-right">
              <Button bsStyle="success" onClick={closeModal}>
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button bsStyle="success" type="submit" disabled={loading || submitting}>
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </GenericForm>
        </Modal>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { addOrganizationModal as AddOrganizationModal };
