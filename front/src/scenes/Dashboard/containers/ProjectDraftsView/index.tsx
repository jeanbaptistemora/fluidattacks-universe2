/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { Modal } from "../../../../components/Modal";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatDrafts, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { textField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { CREATE_DRAFT_MUTATION, GET_DRAFTS } from "./queries";
import { IProjectDraftsAttr, IProjectDraftsBaseProps } from "./types";

const tableHeaders: IHeader[] = [
  { align: "center", dataField: "reportDate", header: "Date", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "type", header: "Type", isDate: false, isStatus: false, width: "8%" },
  { align: "center", dataField: "title", header: "Title", isDate: false, isStatus: false, wrapped: true, width: "18%" },
  {
    align: "center", dataField: "description", header: "Description", isDate: false, isStatus: false, width: "30%",
    wrapped: true,
  },
  { align: "center", dataField: "severityScore", header: "Severity", isDate: false, isStatus: false, width: "8%" },
  {
    align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", isDate: false, isStatus: false,
    width: "6%",
  },
  { align: "center", dataField: "isExploitable", header: "Exploitable", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "isReleased", header: "Released", isDate: false, isStatus: false, width: "10%" },
];

const projectDraftsView: React.FC<IProjectDraftsBaseProps> = (props: IProjectDraftsBaseProps): JSX.Element => {
  const { projectName } = props.match.params;

  const goToFinding: ((rowInfo: { id: string }) => void) = (rowInfo: { id: string }): void => {
    mixpanel.track("ReadDraft", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
    location.hash = `#!/project/${projectName}/drafts/${rowInfo.id}/description`;
  };

  const handleQryResult: ((qrResult: IProjectDraftsAttr) => void) = (): void => {
    mixpanel.track("ProjectDrafts", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
    hidePreloader();
  };

  const [isDraftModalOpen, setDraftModalOpen] = React.useState(false);

  const openNewDraftModal: (() => void) = (): void => {
    setDraftModalOpen(true);
  };

  const closeNewDraftModal: (() => void) = (): void => {
    setDraftModalOpen(false);
  };

  return (
    <Query query={GET_DRAFTS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({ data, error, loading, refetch }: QueryResult<IProjectDraftsAttr>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting project drafts", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const handleMutationResult: ((result: { createDraft: { success: boolean } }) => void) = (
              result: { createDraft: { success: boolean } },
            ): void => {
              if (result.createDraft.success) {
                closeNewDraftModal();
                msgSuccess(
                  translate.t("project.drafts.success_create"),
                  translate.t("project.drafts.title_success"),
                );
                refetch()
                  .catch();
              }
            };

            return (
              <React.StrictMode>
                {(window as typeof window & { userRole: string }).userRole === "admin"
                  ? <Row>
                    <Col md={2} mdOffset={5}>
                      <ButtonToolbar>
                        <Button onClick={openNewDraftModal}>
                          <Glyphicon glyph="plus" />&nbsp;{translate.t("project.drafts.new")}
                        </Button>
                      </ButtonToolbar>
                    </Col>
                  </Row>
                  : undefined}
                <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.drafts.new")}
                  onClose={closeNewDraftModal}
                  open={isDraftModalOpen}
                >
                  <Mutation mutation={CREATE_DRAFT_MUTATION} onCompleted={handleMutationResult}>
                    {(createDraft: MutationFn): React.ReactNode => {
                      const handleSubmit: ((values: {}) => void) = (values: {}): void => {
                        createDraft({ variables: { ...values, projectName } })
                          .catch();
                      };

                      return (
                        <GenericForm name="newDraft" onSubmit={handleSubmit}>
                          {({ pristine, submitting }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row>
                                <Col md={12}>
                                  <label>{translate.t("project.drafts.title")}</label>
                                  <Field component={textField} name="title" type="text" validate={[required]} />
                                </Col>
                              </Row>
                              <br />
                              <ButtonToolbar className="pull-right">
                                <Button bsStyle="success" block={true} type="submit" disabled={pristine || submitting}>
                                  {translate.t("confirmmodal.proceed")}
                                </Button>
                              </ButtonToolbar>
                            </React.Fragment>
                          )}
                        </GenericForm>
                      );
                    }}
                  </Mutation>
                </Modal>
                <p>{translate.t("project.findings.help_label")}</p>
                <DataTable
                  dataset={formatDrafts(data.project.drafts)}
                  enableRowSelection={false}
                  exportCsv={true}
                  headers={tableHeaders}
                  id="tblDrafts"
                  onClickRow={goToFinding}
                  pageSize={15}
                  search={true}
                  selectionMode="none"
                />
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

export { projectDraftsView as ProjectDraftsView };
