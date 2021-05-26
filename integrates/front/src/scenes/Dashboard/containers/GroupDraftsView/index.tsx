import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import { Field } from "redux-form";
import type { InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { ISuggestion } from "scenes/Dashboard/containers/GroupDraftsView/findingNames";
import { getFindingNames } from "scenes/Dashboard/containers/GroupDraftsView/findingNames";
import {
  CREATE_DRAFT_MUTATION,
  GET_DRAFTS,
} from "scenes/Dashboard/containers/GroupDraftsView/queries";
import type { IGroupDraftsAttr } from "scenes/Dashboard/containers/GroupDraftsView/types";
import { formatDrafts } from "scenes/Dashboard/containers/GroupDraftsView/utils";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Row,
} from "styles/styledComponents";
import { AutoCompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required, validDraftTitle } from "utils/validations";

const GroupDraftsView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const { push } = useHistory();
  const { url } = useRouteMatch();

  const goToFinding: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    push(`${url}/${rowInfo.id}/locations`);
  };

  const [isDraftModalOpen, setDraftModalOpen] = useState(false);

  const openNewDraftModal: () => void = useCallback((): void => {
    setDraftModalOpen(true);
  }, []);

  const closeNewDraftModal: () => void = useCallback((): void => {
    setDraftModalOpen(false);
  }, []);

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("draftSort", JSON.stringify(newSorted));
  };
  const selectOptionsStatus = {
    Created: "Created",
    Rejected: "Rejected",
    Submitted: "Submitted",
  };
  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("draftStatusFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "reportDate",
      header: "Date",
      onSort: onSortState,
      width: "9%",
    },
    {
      align: "center",
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "28%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "description",
      header: "Description",
      onSort: onSortState,
      width: "28%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "severityScore",
      header: "Severity",
      onSort: onSortState,
      width: "10%",
    },
    {
      align: "center",
      dataField: "openVulnerabilities",
      header: "Open Vulns.",
      onSort: onSortState,
      width: "10%",
    },
    {
      align: "center",
      dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "draftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: "State",
      onSort: onSortState,
      width: "15%",
      wrapped: true,
    },
  ];

  const [suggestions, setSuggestions] = useState<ISuggestion[]>([]);
  const titleSuggestions: string[] = suggestions.map(
    (suggestion: ISuggestion): string => suggestion.title
  );

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const findingNames: ISuggestion[] = await getFindingNames().catch(
        (error: Error): ISuggestion[] => {
          Logger.error("An error occurred getting draft suggestions", error);

          return [];
        }
      );
      setSuggestions(findingNames);
    }
    void fetchData();
  }, []);

  const handleQryError: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred getting group drafts", error);
    });
  };

  const { data, refetch } = useQuery<IGroupDraftsAttr>(GET_DRAFTS, {
    onError: handleQryError,
    variables: { projectName },
  });

  const handleMutationResult: (result: {
    createDraft: { success: boolean };
  }) => void = (result: { createDraft: { success: boolean } }): void => {
    if (result.createDraft.success) {
      closeNewDraftModal();
      msgSuccess(
        translate.t("group.drafts.successCreate"),
        translate.t("group.drafts.titleSuccess")
      );
      void refetch();
    }
  };

  const handleMutationError: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - The inserted title is invalid":
          msgError(translate.t("validations.draftTitle"));
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred getting group drafts", error);
      }
    });
  };

  const [createDraft, { loading: submitting }] = useMutation(
    CREATE_DRAFT_MUTATION,
    {
      onCompleted: handleMutationResult,
      onError: handleMutationError,
    }
  );

  const handleSubmit: (values: { title: string }) => void = useCallback(
    (values: { title: string }): void => {
      const [matchingSuggestion] = suggestions.filter(
        (suggestion: ISuggestion): boolean => suggestion.title === values.title
      );

      void createDraft({
        variables: { ...matchingSuggestion, projectName, title: values.title },
      });
    },
    [createDraft, projectName, suggestions]
  );

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
                <FontAwesomeIcon icon={faPlus} />
                &nbsp;{translate.t("group.drafts.btn.text")}
              </Button>
            </TooltipWrapper>
          </ButtonToolbarCenter>
        </Col100>
      </Row>
      <Modal
        headerTitle={translate.t("group.drafts.new")}
        open={isDraftModalOpen}
      >
        <GenericForm name={"newDraft"} onSubmit={handleSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <Row>
                <Col100>
                  <label>{translate.t("group.drafts.title")}</label>
                  <Field
                    component={AutoCompleteText}
                    name={"title"}
                    suggestions={titleSuggestions}
                    type={"text"}
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
                    <Button disabled={pristine || submitting} type={"submit"}>
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
        id={"tblDrafts"}
        pageSize={10}
        rowEvents={{ onClick: goToFinding }}
        search={true}
        striped={true}
      />
    </React.StrictMode>
  );
};

export { GroupDraftsView };
