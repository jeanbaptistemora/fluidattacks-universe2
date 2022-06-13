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
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { getFindingNames } from "scenes/Dashboard/containers/GroupDraftsView/findingNames";
import {
  ADD_DRAFT_MUTATION,
  GET_DRAFTS_AND_FINDING_TITLES,
} from "scenes/Dashboard/containers/GroupDraftsView/queries";
import type {
  IAddDraftMutationResult,
  IAddDraftMutationVariables,
  IDraftVariables,
  IGroupDraftsAndFindingsAttr,
  ISuggestion,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import {
  checkDuplicates,
  formatDrafts,
} from "scenes/Dashboard/containers/GroupDraftsView/utils";
import {
  ButtonToolbar,
  Col100,
  HintFieldText,
  Row,
} from "styles/styledComponents";
import { Have } from "utils/authz/Have";
import { FormikAutocompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
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
  const { t } = useTranslation();

  const goToFinding: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    push(`${url}/${rowInfo.id}/locations`);
  };

  const [isDraftModalOpen, setIsDraftModalOpen] = useState(false);
  const [searchTextFilter, setSearchTextFilter] = useState("");

  const openNewDraftModal: () => void = useCallback((): void => {
    setIsDraftModalOpen(true);
  }, []);

  const closeNewDraftModal: () => void = useCallback((): void => {
    setIsDraftModalOpen(false);
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
      dataField: "reportDate",
      header: "Date",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      width: "30%",
      wrapped: true,
    },
    {
      dataField: "description",
      header: "Description",
      onSort: onSortState,
      width: "38%",
      wrapped: true,
    },
    {
      dataField: "severityScore",
      header: "Severity",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "openVulnerabilities",
      header: "Open Vulns.",
      onSort: onSortState,
      width: "10%",
    },
    {
      dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "draftStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
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
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning(
        "An error occurred getting group drafts or findings",
        error
      );
    });
  };

  const { data, refetch } = useQuery<IGroupDraftsAndFindingsAttr>(
    GET_DRAFTS_AND_FINDING_TITLES,
    {
      onError: handleQryError,
      variables: { groupName },
    }
  );

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
        t("group.drafts.successCreate"),
        t("group.drafts.titleSuccess")
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
        msgError(t("validations.draftTitle"));
      } else if (
        error.message ===
        "Exception - A draft of this type has been already created. Please submit vulnerabilities there"
      ) {
        msgError(
          t("validations.duplicateDraft", {
            type: "draft",
          })
        );
      } else if (
        error.message ===
        "Exception - A finding of this type has been already created. Please submit vulnerabilities there"
      ) {
        msgError(
          t("validations.duplicateDraft", {
            type: "finding",
          })
        );
      } else {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("An error occurred while adding drafts", error);
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

  const handleSubmit = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      const [matchingSuggestion] = suggestions.filter(
        (suggestion: ISuggestion): boolean =>
          `${suggestion.key}. ${suggestion.title}` === values.title
      );
      const draftData = _.omit(matchingSuggestion, ["key"]);
      await addDraft({
        variables: {
          ...draftData,
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
      return t("group.drafts.hint.empty");
    }

    return matchingSuggestion.description;
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }
  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(titleSuggestions);

  const validateNoDuplicates = (title: string): string | undefined =>
    checkDuplicates(title, data.group.drafts, data.group.findings);

  const dataset: IGroupDraftsAndFindingsAttr["group"]["drafts"][0][] =
    formatDrafts(data.group.drafts);
  const filterSearchtextResult: IGroupDraftsAndFindingsAttr["group"]["drafts"][0][] =
    filterSearchText(dataset, searchTextFilter);

  return (
    <React.StrictMode>
      <Modal
        onClose={closeNewDraftModal}
        open={isDraftModalOpen}
        title={t("group.drafts.new")}
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
                      validateNoDuplicates,
                    ])}
                  />
                </Col100>
              </Row>
              {dirty && isValid ? (
                <React.Fragment>
                  <hr />
                  <HintFieldText>
                    {t("group.drafts.hint.description")}
                  </HintFieldText>
                  <HintFieldText>
                    {getFindingDescription(values.title)}
                  </HintFieldText>
                </React.Fragment>
              ) : undefined}
              <ModalFooter>
                <Button onClick={closeNewDraftModal} variant={"secondary"}>
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty || !isValid || submitting}
                  type={"submit"}
                  variant={"primary"}
                >
                  {t("confirmmodal.proceed")}
                </Button>
              </ModalFooter>
            </Form>
          )}
        </Formik>
      </Modal>
      <Table
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={filterSearchtextResult}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "draftSort", "{}") as string
        )}
        exportCsv={true}
        extraButtons={
          <Row>
            <Have I={"can_report_vulnerabilities"}>
              <ButtonToolbar>
                <TooltipWrapper
                  id={"group.drafts.btn.tooltip"}
                  message={t("group.drafts.btn.tooltip")}
                >
                  <Button onClick={openNewDraftModal} variant={"secondary"}>
                    <FontAwesomeIcon icon={faPlus} />
                    &nbsp;{t("group.drafts.btn.text")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbar>
            </Have>
          </Row>
        }
        headers={tableHeaders}
        id={"tblDrafts"}
        pageSize={10}
        rowEvents={{ onClick: goToFinding }}
        search={false}
      />
    </React.StrictMode>
  );
};

export { GroupDraftsView };
