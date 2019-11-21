/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { Modal } from "../../../../components/Modal";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatDrafts, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { autocompleteTextField } from "../../../../utils/forms/fields";
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
  { align: "center", dataField: "currentState", header: "State", isDate: false, isStatus: true, width: "10%" },
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

  interface ISuggestion {
    cwe: string;
    description: string;
    recommendation: string;
    requirements: string;
    title: string;
    type: string;
  }
  const [suggestions, setSuggestions] = React.useState<ISuggestion[]>([]);
  const titleSuggestions: string[] = suggestions.map((suggestion: ISuggestion): string => suggestion.title);

  const onMount: (() => void) = (): void => {
    const baseUrl: string = "https://spreadsheets.google.com/feeds/list";
    const spreadsheetId: string = "1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc";
    const rowOffset: number = 2;
    const extraParams: string = `&min-row=${rowOffset}`;

    interface IRowStructure {
      gsx$cwe: { $t: string };
      gsx$descripcion: { $t: string };
      gsx$fin: { $t: string };
      gsx$recomendacion: { $t: string };
      gsx$requisito: { $t: string };
      gsx$tipo: { $t: string };
    }
    fetch(`${baseUrl}/${spreadsheetId}/1/public/values?alt=json${extraParams}`)
      .then(async (httpResponse: Response) => httpResponse.json())
      .then((data: { feed: { entry: IRowStructure[] } }): void => {
        setSuggestions(data.feed.entry.map((row: IRowStructure) => {
          const cwe: RegExpMatchArray | null = row.gsx$cwe.$t.match(/\d+/g);

          return {
            cwe: cwe === null ? "" : cwe[0],
            description: row.gsx$descripcion.$t,
            recommendation: row.gsx$recomendacion.$t,
            requirements: row.gsx$requisito.$t,
            title: row.gsx$fin.$t,
            type: row.gsx$tipo.$t === "Seguridad" ? "SECURITY" : "HYGIENE",
          };
        }));
      })
      .catch();
  };
  React.useEffect(onMount, []);

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
                <Row>
                  <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      <Button onClick={openNewDraftModal}>
                        <Glyphicon glyph="plus" />&nbsp;{translate.t("project.drafts.new")}
                      </Button>
                    </ButtonToolbar>
                  </Col>
                </Row>
                <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.drafts.new")}
                  onClose={closeNewDraftModal}
                  open={isDraftModalOpen}
                >
                  <Mutation mutation={CREATE_DRAFT_MUTATION} onCompleted={handleMutationResult}>
                    {(createDraft: MutationFn, { loading: submitting }: MutationResult): React.ReactNode => {
                      const handleSubmit: ((values: { title: string }) => void) = (values: { title: string }): void => {
                        const matchingSuggestion: ISuggestion = suggestions.filter((
                          suggestion: ISuggestion): boolean => suggestion.title === values.title)[0];

                        createDraft({ variables: { title: values.title, projectName, ...matchingSuggestion } })
                          .catch();
                      };

                      return (
                        <GenericForm name="newDraft" onSubmit={handleSubmit}>
                          {({ pristine }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row>
                                <Col md={12}>
                                  <label>{translate.t("project.drafts.title")}</label>
                                  <Field
                                    component={autocompleteTextField}
                                    name="title"
                                    suggestions={titleSuggestions}
                                    type="text"
                                    validate={[required]}
                                  />
                                </Col>
                              </Row>
                              <br />
                              <ButtonToolbar className="pull-right">
                                <Button bsStyle="success" onClick={closeNewDraftModal}>
                                  {translate.t("confirmmodal.cancel")}
                                </Button>
                                <Button bsStyle="success" type="submit" disabled={pristine || submitting}>
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
