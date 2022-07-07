import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import type { ReactElement } from "react";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { handleGrantError } from "../GroupStakeholdersView/helpers";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
} from "../GroupStakeholdersView/queries";
import type {
  IAddStakeholderAttr,
  IGetStakeholdersAttrs,
} from "../GroupStakeholdersView/types";
import { Button } from "components/Button";
import { Table } from "components/Table";
import { commitFormatter } from "components/Table/formatters";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import {
  filterSearchText,
  filterSelect,
  filterText,
} from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import type { IStakeholderAttr } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import styles from "scenes/Dashboard/containers/GroupAuthorsView/index.css";
import { GET_BILLING } from "scenes/Dashboard/containers/GroupAuthorsView/queries";
import type {
  IAuthors,
  IData,
  IGroupAuthor,
} from "scenes/Dashboard/containers/GroupAuthorsView/types";
import { Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IFilterSet {
  author: string;
  groupsContributed: string;
  invitationState?: string;
  repository: string;
}

const GroupAuthorsView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const DATE_RANGE = 12;
  const dateRange: Date[] = _.range(0, DATE_RANGE).map(
    (month: number): Date => new Date(thisYear, thisMonth - month)
  );

  const [billingDate, setBillingDate] = useState(dateRange[0].toISOString());

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupAuthorsFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterAuthorsTable, setFilterAuthorsTable] =
    useStoredState<IFilterSet>(
      "filterGroupAuthorsSet",
      {
        author: "",
        groupsContributed: "",
        invitationState: "",
        repository: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const formatText: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => <p className={styles.wrapped}>{value}</p>;

  const formatCommit: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => (
    <p className={styles.wrapped}>{commitFormatter(value)}</p>
  );

  const formatDate: (date: Date) => string = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };

  const handleDateChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      setBillingDate(event.target.value);
    },
    []
  );

  const {
    data: stackHolderData,
    loading: loadingStakeholders,
    refetch,
  } = useQuery<IGetStakeholdersAttrs>(GET_STAKEHOLDERS, {
    fetchPolicy: "cache-first",
    onError: (error: ApolloError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group stakeholders", error);
    },
    skip: permissions.cannot(
      "api_resolvers_query_stakeholder__resolve_for_group"
    ),
    variables: { groupName },
  });

  const { data } = useQuery<IData>(GET_BILLING, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting billing data", error);
      });
    },
    variables: { date: billingDate, groupName },
  });

  const [grantAccess, { loading }] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: async (mtResult: IAddStakeholderAttr): Promise<void> => {
      if (mtResult.grantStakeholderAccess.success) {
        await refetch();
        mixpanel.track("AddUserAccess");
        const { email } = mtResult.grantStakeholderAccess.grantedStakeholder;
        msgSuccess(
          `${t("searchFindings.tabUsers.success")} ${email}`,
          t("searchFindings.tabUsers.titleSuccess")
        );
      }
    },
    onError: (grantError: ApolloError): void => {
      handleGrantError(grantError);
    },
  });

  const formatInvitation = useCallback(
    (actorEmail: string): string => {
      const invitationState: string =
        stackHolderData === undefined
          ? ""
          : stackHolderData.group.stakeholders.reduce(
              (previousValue: string, stakeholder: IStakeholderAttr): string =>
                stakeholder.email.toLocaleLowerCase() ===
                actorEmail.toLocaleLowerCase()
                  ? stakeholder.invitationState
                  : previousValue,
              ""
            );
      if (invitationState === "CONFIRMED") {
        return t("group.authors.invitationState.confirmed");
      }
      if (invitationState === "PENDING") {
        return t("group.authors.invitationState.pending");
      }

      return t("group.authors.invitationState.unregistered");
    },
    [stackHolderData, t]
  );

  const headersAuthorsTable: IHeaderConfig[] = [
    {
      dataField: "actor",
      formatter: formatText,
      header: t("group.authors.actor"),
      width: "40%",
      wrapped: true,
    },
    {
      dataField: "groups",
      formatter: formatText,
      header: t("group.authors.groupsContributed"),
      width: "20%",
      wrapped: true,
    },
    {
      dataField: "commit",
      formatter: formatCommit,
      header: t("group.authors.commit"),
      width: "20%",
      wrapped: true,
    },
    {
      dataField: "repository",
      formatter: formatText,
      header: t("group.authors.repository"),
      width: "20%",
      wrapped: true,
    },
    {
      csvExport: false,
      dataField: "invitation",
      header: t("group.authors.invitationState.confirmed"),
      sortFunc: (
        _a,
        _b,
        order,
        _dataField,
        rowA: IAuthors,
        rowB: IAuthors
      ): number => {
        function invitationState(actor: string): string {
          const place: number = actor.lastIndexOf("<");

          return place >= 0
            ? formatInvitation(actor.substring(place + 1, actor.length - 1))
            : formatInvitation(actor);
        }
        if (
          (order === "asc" &&
            invitationState(rowB.actor) < invitationState(rowA.actor)) ||
          (order === "desc" &&
            invitationState(rowA.actor) < invitationState(rowB.actor))
        ) {
          return 1;
        }

        return -1;
      },
      visible:
        stackHolderData !== undefined &&
        permissions.can("api_resolvers_query_stakeholder__resolve_for_group") &&
        permissions.can("api_mutations_grant_stakeholder_access_mutate"),
      width: "130px",
      wrapped: true,
    },
  ];

  const stakeholdersEmail: string[] = useMemo(
    (): string[] =>
      stackHolderData === undefined
        ? []
        : stackHolderData.group.stakeholders.map(
            (stakeholder: IStakeholderAttr): string =>
              stakeholder.email.toLocaleLowerCase()
          ),
    [stackHolderData]
  );

  const dataset: IAuthors[] = useMemo(
    (): IAuthors[] =>
      data === undefined
        ? []
        : data.group.authors.data.map((value: IGroupAuthor): IAuthors => {
            const { actor } = value;
            const place: number = actor.lastIndexOf("<");
            const actorEmail =
              place >= 0 ? actor.substring(place + 1, actor.length - 1) : actor;

            if (stackHolderData === undefined) {
              return {
                ...value,
                invitation: <React.StrictMode />,
              };
            }

            if (stakeholdersEmail.includes(actorEmail.toLowerCase())) {
              return {
                ...value,
                invitation: (
                  <React.StrictMode>
                    {statusFormatter(
                      formatInvitation(actorEmail.toLowerCase())
                    )}
                  </React.StrictMode>
                ),
              };
            }

            async function handleSendInvitation(
              event: React.MouseEvent<HTMLButtonElement>
            ): Promise<void> {
              event.stopPropagation();

              const resendStakeholder = {
                email: actorEmail.toLocaleLowerCase(),
                groupName,
                responsibility: "",
                role: "USER",
              };
              await grantAccess({
                variables: {
                  ...resendStakeholder,
                },
              });
            }

            return {
              ...value,
              invitation: (
                <React.StrictMode>
                  <Can do={"api_mutations_grant_stakeholder_access_mutate"}>
                    <TooltipWrapper
                      id={"authorsGrantTooltip"}
                      message={t("group.authors.tooltip.text")}
                    >
                      <div className={"nl2"}>
                        <Button
                          disabled={loading || loadingStakeholders}
                          onClick={handleSendInvitation}
                          variant={"secondary"}
                        >
                          {t("group.authors.sendInvitation")}
                        </Button>
                      </div>
                    </TooltipWrapper>
                  </Can>
                </React.StrictMode>
              ),
            };
          }),
    [
      data,
      formatInvitation,
      grantAccess,
      groupName,
      loading,
      loadingStakeholders,
      stackHolderData,
      stakeholdersEmail,
      t,
    ]
  );

  const datasetText = useMemo(
    (): (IAuthors & { invitationState: string })[] =>
      dataset.map((value: IAuthors): IAuthors & { invitationState: string } => {
        const { actor } = value;
        const place: number = actor.lastIndexOf("<");
        const actorEmail =
          place >= 0 ? actor.substring(place + 1, actor.length - 1) : actor;

        return {
          ...value,
          invitationState: formatInvitation(actorEmail.toLowerCase()),
        };
      }),
    [dataset, formatInvitation]
  );

  const hasInvitationPermissions: boolean = useMemo(
    (): boolean =>
      stackHolderData !== undefined &&
      permissions.can("api_resolvers_query_stakeholder__resolve_for_group") &&
      permissions.can("api_mutations_grant_stakeholder_access_mutate"),
    [permissions, stackHolderData]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextDataset: IAuthors[] = filterSearchText(
    datasetText,
    searchTextFilter
  ).map((value: IAuthors): IAuthors => _.omit(value, "invitationState"));

  function onAuthorChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        author: event.target.value,
      })
    );
  }
  const filterAuthorDataset: IAuthors[] = filterText(
    dataset,
    filterAuthorsTable.author,
    "actor"
  );
  function onGroupsContributedChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        groupsContributed: event.target.value,
      })
    );
  }
  const filterGroupsContributedDataset: IAuthors[] = filterText(
    dataset,
    filterAuthorsTable.groupsContributed,
    "groups"
  );
  function onRepositoryChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        repository: event.target.value,
      })
    );
  }
  const filterRepositoryDataset: IAuthors[] = filterText(
    dataset,
    filterAuthorsTable.repository,
    "repository"
  );

  const onFilterAuthorsTableChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setFilterAuthorsTable(
      (value): IFilterSet => ({
        ...value,
        invitationState: event.target.value,
      })
    );
  };

  function clearFilters(): void {
    setFilterAuthorsTable(
      (): IFilterSet => ({
        author: "",
        groupsContributed: "",
        invitationState: "",
        repository: "",
      })
    );
    setSearchTextFilter("");
  }
  const filterInvitationDataset: IAuthors[] = filterSelect(
    datasetText,
    filterAuthorsTable.invitationState ?? "",
    "invitationState"
  ).map((value: IAuthors): IAuthors => _.omit(value, "invitationState"));

  const resultDataset: IAuthors[] = _.intersectionWith(
    filterSearchtextDataset,
    filterAuthorDataset,
    filterRepositoryDataset,
    filterGroupsContributedDataset,
    filterInvitationDataset,
    _.isEqual
  );

  const additionalFilter: IFilterProps[] = [
    {
      defaultValue: filterAuthorsTable.invitationState ?? "",
      onChangeSelect: onFilterAuthorsTableChange,
      placeholder: "Registration status",
      selectOptions: {
        Pending: "Pending",
        Registered: "Registered",
        Unregistered: "Unregistered",
      },
      tooltipId: "group.authors.filtersTooltips.invitation.id",
      tooltipMessage: "group.authors.filtersTooltips.invitation",
      type: "select",
    },
  ];

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterAuthorsTable.author,
      onChangeInput: onAuthorChange,
      placeholder: "Author",
      tooltipId: "group.authors.filtersTooltips.actor.id",
      tooltipMessage: "group.authors.filtersTooltips.actor",
      type: "text",
    },
    {
      defaultValue: filterAuthorsTable.groupsContributed,
      onChangeInput: onGroupsContributedChange,
      placeholder: "Groups Contributed",
      tooltipId: "group.authors.filtersTooltips.groupsContributed.id",
      tooltipMessage: "group.authors.filtersTooltips.groupsContributed",
      type: "text",
    },
    {
      defaultValue: filterAuthorsTable.repository,
      onChangeInput: onRepositoryChange,
      placeholder: "Repository",
      tooltipId: "group.authors.filtersTooltips.repository.id",
      tooltipMessage: "group.authors.filtersTooltips.repository",
      type: "text",
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col100 className={"pl0"}>
          <p>{t("group.authors.tableAdvice")}</p>
        </Col100>
      </Row>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col100 className={styles.dateCol}>
          <select className={styles.selectDate} onChange={handleDateChange}>
            {dateRange.map(
              (date: Date, index: number): JSX.Element => (
                <option
                  // Dates have no unique components unfortunately
                  // eslint-disable-next-line react/no-array-index-key
                  key={index.toString()}
                  selected={date.toISOString() === billingDate}
                  value={date.toISOString()}
                >
                  {formatDate(date)}
                </option>
              )
            )}
          </select>
        </Col100>
      </Row>
      <Table
        clearFiltersButton={clearFilters}
        customFilters={{
          customFiltersProps: [
            ...customFiltersProps,
            ...(hasInvitationPermissions ? additionalFilter : []),
          ],
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
          resultSize: {
            current: resultDataset.length,
            total: dataset.length,
          },
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={
          /* eslint-disable-next-line fp/no-mutating-methods */
          resultDataset.sort((itemA, itemB): number =>
            itemA.actor > itemB.actor ? 1 : -1
          )
        }
        defaultSorted={{ dataField: "actor", order: "asc" }}
        exportCsv={true}
        headers={headersAuthorsTable}
        id={"tblAuthorsList"}
        pageSize={100}
        search={false}
      />
    </React.StrictMode>
  );
};

export { GroupAuthorsView };
