/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { useMutation } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, FormGroup, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal/index";
import { authzContext } from "../../../../utils/authz/config";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { textField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { required, sameValue } from "../../../../utils/validations";
import { PROJECTS_QUERY } from "../../containers/HomeView/queries";
import { GenericForm } from "../GenericForm";
import { REQUEST_REMOVE_PROJECT_MUTATION } from "./queries";
import { IRemoveProject, IRemoveProjectModal } from "./types";

const removeProjectModal: ((props: IRemoveProjectModal) => JSX.Element) =
  (props: IRemoveProjectModal): JSX.Element => {
    const { push } = useHistory();
    const { onClose } = props;
    const projectName: string = props.projectName.toLowerCase();
    const permissions: PureAbility<string> = useAbility(authzContext);

    const sameProjectName: ConfigurableValidator = sameValue(projectName);
    const selector: (state: {}, ...fields: string[]) => string = formValueSelector("removeProject");
    const projectNameInput: string = useSelector((state: {}) => selector(state, "projectName"));
    const disableButton: boolean = sameProjectName(projectNameInput);

    const [removeProject, { loading: submitting }] = useMutation(REQUEST_REMOVE_PROJECT_MUTATION, {
      onCompleted: (mtResult: IRemoveProject): void => {
        if (mtResult.requestRemoveProject.success) {
          push("/home");
          msgSuccess(
            translate.t("proj_alerts.request_remove"),
            translate.t("proj_alerts.title_success"),
          );
        }
      },
      onError: (error: ApolloError): void => {
        onClose();
        handleGraphQLErrors("An error occurred removing project", error);
      },
      refetchQueries: [
        {
          query: PROJECTS_QUERY,
          variables: { tagsField: permissions.can("backend_api_resolvers_me__get_tags") },
        },
      ],
    });

    const handleSubmit: ((values: { projectName: string }) => void) = async (
      values: { projectName: string },
    ): Promise<void> => {
      await removeProject({
        variables: {
          projectName: values.projectName,
        },
      });
    };

    return (
      <React.StrictMode>
        <Modal
          footer={<div />}
          headerTitle={translate.t("search_findings.tab_resources.removeProject")}
          onClose={onClose}
          open={props.isOpen}
        >
          <React.Fragment>
            <React.Fragment>
              <React.Fragment>
                <GenericForm name="removeProject" onSubmit={handleSubmit}>
                  {({ pristine }: InjectedFormProps): JSX.Element => (
                    <React.Fragment>
                      <Row>
                        <Col md={12} sm={12}>
                          <FormGroup>
                            <Trans>
                              <p>{translate.t("search_findings.tab_resources.projectToRemove")}</p>
                            </Trans>
                            <Field
                              component={textField}
                              name="projectName"
                              type="text"
                              validate={[required, sameProjectName]}
                            />
                          </FormGroup>
                        </Col>
                      </Row>
                      <br />
                      <ButtonToolbar className="pull-right">
                        <Button bsStyle="success" onClick={onClose}>
                          {translate.t("confirmmodal.cancel")}
                        </Button>
                        <Button bsStyle="success" type="submit" disabled={pristine || submitting || disableButton}>
                          {translate.t("confirmmodal.proceed")}
                        </Button>
                      </ButtonToolbar>
                    </React.Fragment>
                  )}
                </GenericForm>
              </React.Fragment>
            </React.Fragment>
          </React.Fragment>
        </Modal>
      </React.StrictMode>
    );
  };

export { removeProjectModal as RemoveProjectModal };
