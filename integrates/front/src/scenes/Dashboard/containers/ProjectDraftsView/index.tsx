import { useMutation, useQuery } from "@apollo/react-hooks";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory, useParams } from "react-router-dom";
import { Field, InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { CREATE_DRAFT_MUTATION, GET_DRAFTS } from "scenes/Dashboard/containers/ProjectDraftsView/queries";
import { IProjectDraftsAttr } from "scenes/Dashboard/containers/ProjectDraftsView/types";
import { formatDrafts } from "scenes/Dashboard/containers/ProjectDraftsView/utils";
import { ButtonToolbar, ButtonToolbarCenter, Col100, Row } from "styles/styledComponents";
import { AutoCompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required, validDraftTitle } from "utils/validations";

const projectDraftsView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const { push } = useHistory();

  const goToFinding: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string },
  ): void => {
    push(`/groups/${projectName}/drafts/${rowInfo.id}/locations`);
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
    { align: "center", dataField: "reportDate", header: "Date", onSort: onSortState, width: "9%" },
    { align: "center", dataField: "title", header: "Type", onSort: onSortState, wrapped: true, width: "28%" },
    {
      align: "center", dataField: "description", header: "Description", onSort: onSortState, width: "28%",
      wrapped: true,
    },
    { align: "center", dataField: "severityScore", header: "Severity", onSort: onSortState, width: "10%" },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", onSort: onSortState, width: "10%",
    },
    {
      align: "center", dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "draftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter, header: "State", onSort: onSortState, width: "15%",
      wrapped: true,
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
      .then((sData: { feed: { entry: IRowStructure[] } }): void => {
        setSuggestions(sData.feed.entry.map((row: IRowStructure) => {
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
      .catch((error: Error) => {
        Logger.error("An error occurred getting draft suggestions", error);
      });
  };
  React.useEffect(onMount, []);

  const handleQryError: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred getting project drafts", error);
    });
  };

  const { data, refetch } = useQuery<IProjectDraftsAttr>(GET_DRAFTS, {
    onError: handleQryError,
    variables: { projectName },
  });

  const handleMutationResult: ((result: { createDraft: { success: boolean } }) => void) = (
    result: { createDraft: { success: boolean } },
  ): void => {
    if (result.createDraft.success) {
      closeNewDraftModal();
      msgSuccess(
        translate.t("group.drafts.successCreate"),
        translate.t("group.drafts.titleSuccess"),
      );
      void refetch();
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
          Logger.warning(
            "An error occurred getting project drafts",
            error,
          );
      }
    });
  };

  const [createDraft, { loading: submitting }] = useMutation(CREATE_DRAFT_MUTATION, {
    onCompleted: handleMutationResult,
    onError: handleMutationError,
  });

  const handleSubmit: ((values: { title: string }) => void) = (values: { title: string }): void => {
    const matchingSuggestion: ISuggestion = suggestions.filter((
      suggestion: ISuggestion): boolean => suggestion.title === values.title)[0];

    void createDraft({ variables: { ...matchingSuggestion, title: values.title, projectName } });
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Row>
        <Col100>
          <ButtonToolbarCenter>
            <TooltipWrapper
              id={"group.drafts.btn.tooltip"}
              message={translate.t("group.drafts.btn.tooltip")}
            >
              <Button onClick={openNewDraftModal}>
                <FontAwesomeIcon icon={faPlus} />&nbsp;{translate.t("group.drafts.btn.text")}
              </Button>
            </TooltipWrapper>
          </ButtonToolbarCenter>
        </Col100>
      </Row>
      <Modal
        headerTitle={translate.t("group.drafts.new")}
        open={isDraftModalOpen}
      >
        <GenericForm name="newDraft" onSubmit={handleSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <Row>
                <Col100>
                  <label>{translate.t("group.drafts.title")}</label>
                  <Field
                    component={AutoCompleteText}
                    name="title"
                    suggestions={titleSuggestions}
                    type="text"
                    validate={[required, validDraftTitle]}
                  />
                </Col100>
              </Row>
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={closeNewDraftModal}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button type="submit" disabled={pristine || submitting}>
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
      <p>{translate.t("group.findings.helpLabel")}</p>
      <DataTableNext
        bordered={true}
        dataset={formatDrafts(data.project.drafts)}
        defaultSorted={JSON.parse(_.get(sessionStorage, "draftSort", "{}"))}
        exportCsv={true}
        headers={tableHeaders}
        id="tblDrafts"
        pageSize={15}
        rowEvents={{ onClick: goToFinding }}
        search={true}
        striped={true}
      />
    </React.StrictMode>
  );
};

export { projectDraftsView as ProjectDraftsView };
