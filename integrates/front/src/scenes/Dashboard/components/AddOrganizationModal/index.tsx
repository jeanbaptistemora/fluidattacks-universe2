import { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import { Text } from "utils/forms/fields";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import { translate } from "utils/translations/translate";
import { useHistory } from "react-router-dom";
import {
  ButtonToolbar,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import {
  CREATE_NEW_ORGANIZATION,
  GET_AVAILABLE_ORGANIZATION_NAME,
} from "scenes/Dashboard/components/AddOrganizationModal/queries";
import {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
  IAddOrganizationQryProps,
} from "scenes/Dashboard/components/AddOrganizationModal/types";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

const AddOrganizationModal: React.FC<IAddOrganizationModalProps> = (
  props: IAddOrganizationModalProps
): JSX.Element => {
  const { open, onClose } = props;

  const { userName } = window as typeof window & Dictionary<string>;
  const { push } = useHistory();

  // GraphQL Operations
  const { data, loading } = useQuery<IAddOrganizationQryProps>(
    GET_AVAILABLE_ORGANIZATION_NAME,
    {
      onError: (error: ApolloError): void => {
        onClose();
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - There are no organization names available at the moment":
              msgError(
                translate.t("sidebar.newOrganization.modal.namesUnavailable")
              );
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning(
                "An error occurred creating an organization",
                message
              );
          }
        });
      },
    }
  );

  const [createOrganization, { loading: submitting }] = useMutation(
    CREATE_NEW_ORGANIZATION,
    {
      onCompleted: (result: IAddOrganizationMtProps): void => {
        if (result.createOrganization.success) {
          onClose();
          mixpanel.track("NewOrganization", {
            OrganizationId: result.createOrganization.organization.id,
            OrganizationName: result.createOrganization.organization.name,
            User: userName,
          });
          msgSuccess(
            translate.t("sidebar.newOrganization.modal.success", {
              name: result.createOrganization.organization.name,
            }),
            translate.t("sidebar.newOrganization.modal.successTitle")
          );
          push(
            `/orgs/${result.createOrganization.organization.name.toLowerCase()}/`
          );
        }
      },
      onError: (error: ApolloError): void => {
        onClose();
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Organization name is invalid":
              msgError(
                translate.t("sidebar.newOrganization.modal.invalidName")
              );
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
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
    void createOrganization({ variables: { name: values.name } });
  }

  const organizationName: string =
    _.isUndefined(data) || _.isEmpty(data) ? "" : data.internalNames.name;

  // Render Elements
  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("sidebar.newOrganization.modal.title")}
        open={open}
      >
        <GenericForm
          initialValues={{ name: organizationName.toUpperCase() }}
          name={"newOrganization"}
          onSubmit={handleSubmit}
        >
          <Row>
            <FormGroup>
              <ControlLabel>
                {translate.t("sidebar.newOrganization.modal.name")}
              </ControlLabel>
              <TooltipWrapper
                message={translate.t(
                  "sidebar.newOrganization.modal.nameTooltip"
                )}
                placement={"top"}
              >
                <Field
                  component={Text}
                  disabled={true}
                  name={"name"}
                  type={"text"}
                />
              </TooltipWrapper>
            </FormGroup>
          </Row>
          <ButtonToolbar>
            <Button onClick={onClose}>
              {translate.t("confirmmodal.cancel")}
            </Button>
            <Button disabled={loading || submitting} type={"submit"}>
              {translate.t("confirmmodal.proceed")}
            </Button>
          </ButtonToolbar>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { AddOrganizationModal };
