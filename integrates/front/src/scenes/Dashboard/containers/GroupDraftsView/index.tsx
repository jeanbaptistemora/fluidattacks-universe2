import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { getFindingNames } from "scenes/Dashboard/containers/GroupDraftsView/findingNames";
import {
  ADD_DRAFT_MUTATION,
  GET_DRAFTS,
} from "scenes/Dashboard/containers/GroupDraftsView/queries";
import type {
  IAddDraftMutationResult,
  IAddDraftMutationVariables,
  IDraftVariables,
  IGroupDraftsAttr,
  ISuggestion,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import { formatDrafts } from "scenes/Dashboard/containers/GroupDraftsView/utils";
import {
  ButtonToolbar,
  Col100,
  HintFieldText,
  Row,
} from "styles/styledComponents";
import { FormikAutocompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  required,
  validDraftTitle,
  validFindingTypology,
} from "utils/validations";

const GroupDraftsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
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
  const [searchTextFilter, setSearchTextFilter] = useState("");

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
      width: "10%",
    },
    {
      align: "center",
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "30%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "description",
      header: "Description",
      onSort: onSortState,
      width: "38%",
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
      align: "left",
      dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "draftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: pointStatusFormatter,
      header: "State",
      onSort: onSortState,
      width: "95px",
      wrapped: true,
    },
  ];

  const [suggestions, setSuggestions] = useState<ISuggestion[]>([]);
  const titleSuggestions: string[] = _.sortBy(
    suggestions.map(
      (suggestion: ISuggestion): string =>
        `${suggestion.key}. ${suggestion.title}`
    )
  );

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
    variables: { groupName },
  });

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const findingNames: ISuggestion[] = await getFindingNames(
        data?.group.language
      ).catch((error: Error): ISuggestion[] => {
        Logger.error("An error occurred getting draft suggestions", error);

        return [];
      });
      setSuggestions(findingNames);
    }
    void fetchData();
  }, [data?.group.language]);

  async function handleMutationResult(
    result: IAddDraftMutationResult
  ): Promise<void> {
    if (result.addDraft.success) {
      closeNewDraftModal();
      msgSuccess(
        translate.t("group.drafts.successCreate"),
        translate.t("group.drafts.titleSuccess")
      );
      await refetch();
    }
  }

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  const handleMutationError: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      if (
        error.message ===
        "Exception - The inserted Draft/Finding title is invalid"
      ) {
        msgError(translate.t("validations.draftTitle"));
      } else {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting group drafts", error);
      }
    });
  };

  const [addDraft, { loading: submitting }] = useMutation<
    IAddDraftMutationResult,
    IAddDraftMutationVariables
  >(ADD_DRAFT_MUTATION, {
    onCompleted: handleMutationResult,
    onError: handleMutationError,
  });

  const handleSubmit: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      const [matchingSuggestion]: IDraftVariables[] = suggestions.filter(
        (suggestion: ISuggestion): boolean =>
          `${suggestion.key}. ${suggestion.title}` === values.title
      );

      void addDraft({
        variables: {
          ...matchingSuggestion,
          groupName,
          title: values.title as string,
        },
      });
    },
    [addDraft, groupName, suggestions]
  );

  const getFindingDescription: (findingName: string) => string = (
    findingName: string
  ): string => {
    const [matchingSuggestion]: IDraftVariables[] = suggestions.filter(
      (suggestion: ISuggestion): boolean =>
        `${suggestion.key}. ${suggestion.title}` === findingName
    );

    if (
      _.isUndefined(matchingSuggestion) ||
      !matchingSuggestion.description ||
      matchingSuggestion.description.includes("__empty__")
    ) {
      return translate.t("group.drafts.hint.empty");
    }

    return matchingSuggestion.description;
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }
  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(titleSuggestions);

  const dataset: IGroupDraftsAttr["group"]["drafts"][0][] = formatDrafts(
    data.group.drafts
  );
  const filterSearchtextResult: IGroupDraftsAttr["group"]["drafts"][0][] =
    filterSearchText(dataset, searchTextFilter);

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("group.drafts.new")}
        onEsc={closeNewDraftModal}
        open={isDraftModalOpen}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{ title: "" }}
          name={"newDraft"}
          onSubmit={handleSubmit}
        >
          {({ dirty, isValid, values }): JSX.Element => (
            <Form>
              <Row>
                <Col100>
                  <Field
                    alignField={"horizontal"}
                    component={FormikAutocompleteText}
                    focus={true}
                    id={"title"}
                    name={"title"}
                    renderAsEditable={true}
                    suggestions={titleSuggestions}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validDraftTitle,
                      validateFindingTypology,
                    ])}
                  />
                </Col100>
              </Row>
              {dirty && isValid ? (
                <React.Fragment>
                  <hr />
                  <HintFieldText>
                    {translate.t("group.drafts.hint.description")}
                  </HintFieldText>
                  <HintFieldText>
                    {getFindingDescription(values.title)}
                  </HintFieldText>
                </React.Fragment>
              ) : undefined}
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={closeNewDraftModal}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty || !isValid || submitting}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
      <TooltipWrapper
        id={"group.drafts.help"}
        message={translate.t("group.findings.helpLabel")}
      >
        <DataTableNext
          bordered={true}
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
          }}
          dataset={filterSearchtextResult}
          defaultSorted={JSON.parse(_.get(sessionStorage, "draftSort", "{}"))}
          exportCsv={true}
          extraButtons={
            <Row>
              <ButtonToolbar>
                <TooltipWrapper
                  id={"group.drafts.btn.tooltip"}
                  message={translate.t("group.drafts.btn.tooltip")}
                >
                  <Button onClick={openNewDraftModal}>
                    <FontAwesomeIcon icon={faPlus} />
                    &nbsp;{translate.t("group.drafts.btn.text")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbar>
            </Row>
          }
          headers={tableHeaders}
          id={"tblDrafts"}
          pageSize={10}
          rowEvents={{ onClick: goToFinding }}
          search={false}
          striped={true}
        />
      </TooltipWrapper>
    </React.StrictMode>
  );
};

export { GroupDraftsView };
