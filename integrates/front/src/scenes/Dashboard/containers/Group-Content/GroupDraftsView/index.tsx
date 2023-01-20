import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef, Row as tableRow } from "@tanstack/react-table";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import { Alert } from "components/Alert";
import { Button } from "components/Button";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { getFindingNames } from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/findingNames";
import {
  ADD_DRAFT_MUTATION,
  GET_DRAFTS_AND_FINDING_TITLES,
  GET_ME_HAS_DRAFTS_REJECTED,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/queries";
import type {
  IAddDraftMutationResult,
  IAddDraftMutationVariables,
  IDraftVariables,
  IGetMeHasDraftsRejected,
  IGroupDraftsAndFindingsAttr,
  ISuggestion,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/types";
import {
  checkDuplicates,
  formatDrafts,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/utils";
import { Col100, HintFieldText, Row } from "styles/styledComponents";
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

  const goToFinding = useCallback(
    (
      rowInfo: tableRow<IGroupDraftsAndFindingsAttr["group"]["drafts"][0]>
    ): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        push(`${url}/${rowInfo.original.id}/locations`);
        event.preventDefault();
      };
    },
    [push, url]
  );

  const [isDraftModalOpen, setIsDraftModalOpen] = useState(false);

  const openNewDraftModal: () => void = useCallback((): void => {
    setIsDraftModalOpen(true);
  }, []);

  const closeNewDraftModal: () => void = useCallback((): void => {
    setIsDraftModalOpen(false);
  }, []);

  const tableColumns: ColumnDef<
    IGroupDraftsAndFindingsAttr["group"]["drafts"][0]
  >[] = [
    {
      accessorKey: "reportDate",
      header: "Date",
    },
    {
      accessorKey: "title",
      header: "Type",
    },
    {
      accessorKey: "description",
      header: "Description",
    },
    {
      accessorKey: "severityScore",
      header: "Severity",
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open Vulns.",
    },
    {
      accessorKey: "currentState",
      cell: (
        cell: ICellHelper<IGroupDraftsAndFindingsAttr["group"]["drafts"][0]>
      ): JSX.Element => statusFormatter(cell.getValue()),
      header: "State",
    },
  ];

  const [filters, setFilters] = useState<
    IFilter<IGroupDraftsAndFindingsAttr["group"]["drafts"][0]>[]
  >([
    {
      id: "currentState",
      key: "currentState",
      label: "State",
      selectOptions: ["Created", "Rejected", "Submitted"],
      type: "select",
    },
  ]);

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

  const { data: dataHasDraftsRejected, refetch: refetchHasDraftsRejected } =
    useQuery<IGetMeHasDraftsRejected>(GET_ME_HAS_DRAFTS_REJECTED, {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred getting me has drafts rejected",
            error
          );
        });
      },
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
        t("group.drafts.successCreate"),
        t("group.drafts.titleSuccess")
      );
      await refetch();
    }
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
      } else if (
        error.message === "Exception - User has pending rejected drafts"
      ) {
        msgError(t("validations.hasDraftsRejected"));
        void refetchHasDraftsRejected();
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

  const dataset: IGroupDraftsAndFindingsAttr["group"]["drafts"][0][] =
    formatDrafts(data?.group.drafts ?? []);

  const filteredData: IGroupDraftsAndFindingsAttr["group"]["drafts"][0][] =
    useFilters(dataset, filters);

  if (
    _.isUndefined(data) ||
    _.isEmpty(data) ||
    _.isUndefined(dataHasDraftsRejected) ||
    _.isEmpty(dataHasDraftsRejected)
  ) {
    return <div />;
  }
  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(titleSuggestions);

  const validateNoDuplicates = (title: string): string | undefined =>
    checkDuplicates(title, data.group.drafts, data.group.findings);

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
                  {dataHasDraftsRejected.me.hasDraftsRejected ? (
                    <Alert>{t("group.drafts.error.hasDraftsRejected")}</Alert>
                  ) : (
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
                  )}
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
              <ModalConfirm
                disabled={
                  !dirty ||
                  !isValid ||
                  submitting ||
                  dataHasDraftsRejected.me.hasDraftsRejected
                }
                onCancel={closeNewDraftModal}
              />
            </Form>
          )}
        </Formik>
      </Modal>
      <Table
        columns={tableColumns}
        data={filteredData}
        exportCsv={true}
        extraButtons={
          <Have I={"can_report_vulnerabilities"}>
            <Tooltip
              id={"group.drafts.btn.tooltip"}
              tip={t("group.drafts.btn.tooltip")}
            >
              <Button onClick={openNewDraftModal} variant={"primary"}>
                <FontAwesomeIcon icon={faPlus} />
                &nbsp;{t("group.drafts.btn.text")}
              </Button>
            </Tooltip>
          </Have>
        }
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblDrafts"}
        onRowClick={goToFinding}
      />
    </React.StrictMode>
  );
};

export { GroupDraftsView };
