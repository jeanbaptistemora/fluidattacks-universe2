/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory } from "react-router-dom";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { formatDrafts } from "../../../../utils/formatHelpers";
import { autocompleteTextField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required, validDraftTitle } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { CREATE_DRAFT_MUTATION, GET_DRAFTS } from "./queries";
import { IProjectDraftsAttr, IProjectDraftsBaseProps } from "./types";

const projectDraftsView: React.FC<IProjectDraftsBaseProps> = (props: IProjectDraftsBaseProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { push } = useHistory();

  const goToFinding: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string },
  ): void => {
    mixpanel.track("ReadDraft", {
      User: (window as typeof window & { userName: string }).userName,
    });
    push(`/groups/${projectName}/drafts/${rowInfo.id}/description`);
  };

  const handleQryResult: ((qrResult: IProjectDraftsAttr) => void) = (): void => {
    mixpanel.track("ProjectDrafts", {
      User: (window as typeof window & { userName: string }).userName,
    });
  };

  const [isDraftModalOpen, setDraftModalOpen] = React.useState(false);

  const openNewDraftModal: (() => void) = (): void => {
    setDraftModalOpen(true);
  };

  const closeNewDraftModal: (() => void) = (): void => {
    setDraftModalOpen(false);
  };
  const onSortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("draftSort", JSON.stringify(newSorted));
  };
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Created", label: "Created" },
    { value: "Submitted", label: "Submitted" },
    { value: "Rejected", label: "Rejected" },
  ];
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("draftStatusFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    { align: "center", dataField: "reportDate", header: "Date", onSort: onSortState, width: "10%" },
    { align: "center", dataField: "type", header: "Type", onSort: onSortState, width: "8%" },
    { align: "center", dataField: "title", header: "Title", onSort: onSortState, wrapped: true, width: "18%" },
    {
      align: "center", dataField: "description", header: "Description", onSort: onSortState, width: "30%",
      wrapped: true,
    },
    { align: "center", dataField: "severityScore", header: "Severity", onSort: onSortState, width: "8%" },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", onSort: onSortState, width: "6%",
    },
    {
      align: "center", dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "draftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter, header: "State", onSort: onSortState, width: "10%",
    },
  ];

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

  const handleQryError: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred getting project drafts", error);
    });
  };

  return (
    <Query
      query={GET_DRAFTS}
      variables={{ projectName }}
      onCompleted={handleQryResult}
      onError={handleQryError}
    >
      {
        ({ data, refetch }: QueryResult<IProjectDraftsAttr>): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }

          const handleMutationResult: ((result: { createDraft: { success: boolean } }) => void) = (
              result: { createDraft: { success: boolean } },
            ): void => {
              if (result.createDraft.success) {
                closeNewDraftModal();
                msgSuccess(
                  translate.t("group.drafts.success_create"),
                  translate.t("group.drafts.title_success"),
                );
                refetch()
                  .catch();
              }
            };

          const handleMutationError: ((error: ApolloError) => void) = (
            { graphQLErrors }: ApolloError,
          ): void => {
            graphQLErrors.forEach((error: GraphQLError): void => {
              switch (error.message) {
                case "Exception - The inserted title is invalid":
                  msgError(translate.t("validations.draftTitle"));
                  break;
                default:
                  msgError(translate.t("group_alerts.error_textsad"));
                  rollbar.error(
                    "An error occurred getting project drafts",
                    error,
                  );
              }
            });
          };

          return (
              <React.StrictMode>
                <Row>
                  <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      <TooltipWrapper message={translate.t("group.drafts.btn.tooltip")}>
                        <Button onClick={openNewDraftModal}>
                          <Glyphicon glyph="plus" />&nbsp;{translate.t("group.drafts.btn.text")}
                        </Button>
                      </TooltipWrapper>
                    </ButtonToolbar>
                  </Col>
                </Row>
                <Modal
                  footer={<div />}
                  headerTitle={translate.t("group.drafts.new")}
                  open={isDraftModalOpen}
                >
                  <Mutation
                    mutation={CREATE_DRAFT_MUTATION}
                    onCompleted={handleMutationResult}
                    onError={handleMutationError}
                  >
                    {(createDraft: MutationFunction, { loading: submitting }: MutationResult): JSX.Element => {
                      const handleSubmit: ((values: { title: string }) => void) = (values: { title: string }): void => {
                        const matchingSuggestion: ISuggestion = suggestions.filter((
                          suggestion: ISuggestion): boolean => suggestion.title === values.title)[0];

                        createDraft({ variables: { ...matchingSuggestion, title: values.title, projectName } })
                          .catch();
                      };

                      return (
                        <GenericForm name="newDraft" onSubmit={handleSubmit}>
                          {({ pristine }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row>
                                <Col md={12}>
                                  <label>{translate.t("group.drafts.title")}</label>
                                  <Field
                                    component={autocompleteTextField}
                                    name="title"
                                    suggestions={titleSuggestions}
                                    type="text"
                                    validate={[required, validDraftTitle]}
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
                <p>{translate.t("group.findings.help_label")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={formatDrafts(data.project.drafts)}
                  defaultSorted={JSON.parse(_.get(sessionStorage, "draftSort", "{}"))}
                  exportCsv={true}
                  headers={tableHeaders}
                  id="tblDrafts"
                  pageSize={15}
                  remote={false}
                  rowEvents={{ onClick: goToFinding }}
                  search={true}
                  striped={true}
                />
              </React.StrictMode>
            );
        }}
    </Query>
  );
};

export { projectDraftsView as ProjectDraftsView };
