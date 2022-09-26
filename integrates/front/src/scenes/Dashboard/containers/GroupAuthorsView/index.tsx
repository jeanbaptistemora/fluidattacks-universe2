/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  ColumnFiltersState,
  PaginationState,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import type { ReactElement } from "react";
import React, { useCallback, useEffect, useMemo, useState } from "react";
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
import { Table } from "components/TableNew/index";
import type { ICellHelper } from "components/TableNew/types";
import { Tooltip } from "components/Tooltip";
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

  const formatText: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => <p className={styles.wrapped}>{value}</p>;

  const formatDate: (date: Date) => string = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };

  function commitFormatter(value: string): string {
    const COMMIT_LENGTH: number = 7;

    return value.slice(0, COMMIT_LENGTH);
  }

  const formatCommit: (value: string) => ReactElement<Text> = (
    value: string
  ): ReactElement<Text> => (
    <p className={styles.wrapped}>{commitFormatter(value)}</p>
  );

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
      if (invitationState === "REGISTERED") {
        return t("group.authors.invitationState.confirmed");
      }
      if (invitationState === "PENDING") {
        return t("group.authors.invitationState.pending");
      }

      return t("group.authors.invitationState.unregistered");
    },
    [stackHolderData, t]
  );

  const hasInvitationPermissions: boolean = useMemo(
    (): boolean =>
      stackHolderData !== undefined &&
      permissions.can("api_resolvers_query_stakeholder__resolve_for_group") &&
      permissions.can("api_mutations_grant_stakeholder_access_mutate"),
    [permissions, stackHolderData]
  );

  const [columnFilters, columnFiltersSetter] =
    useStoredState<ColumnFiltersState>("tblAuthorsList-columnFilters", []);
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblAuthorsList-visibilityState", {
      invitation: hasInvitationPermissions,
    });
  const [pagination, setpagination] = useStoredState<PaginationState>(
    "tblAuthorsList-pagination",
    {
      pageIndex: 0,
      pageSize: 10,
    }
  );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblAuthorsList-sortingState",
    []
  );

  const columns: ColumnDef<IAuthors & { invitationState: string }>[] = [
    {
      accessorKey: "actor",
      cell: (
        cell: ICellHelper<IAuthors & { invitationState: string }>
      ): JSX.Element => formatText(cell.getValue()),
      header: t("group.authors.actor"),
    },
    {
      accessorKey: "groups",
      cell: (
        cell: ICellHelper<IAuthors & { invitationState: string }>
      ): JSX.Element => formatText(cell.getValue()),
      header: t("group.authors.groupsContributed"),
    },
    {
      accessorKey: "commit",
      cell: (
        cell: ICellHelper<IAuthors & { invitationState: string }>
      ): JSX.Element => formatCommit(cell.getValue()),
      header: t("group.authors.commit"),
    },
    {
      accessorKey: "repository",
      cell: (
        cell: ICellHelper<IAuthors & { invitationState: string }>
      ): JSX.Element => formatText(cell.getValue()),
      header: t("group.authors.repository"),
    },
    {
      accessorKey: "invitation",
      cell: (
        cell: ICellHelper<IAuthors & { invitationState: string }>
      ): JSX.Element => cell.getValue(),
      header: t("searchFindings.usersTable.invitationState"),
    },
  ];

  const columnsExtra: ColumnDef<IAuthors & { invitationState: string }>[] = [
    {
      accessorKey: "invitationState",
      header: t("searchFindings.usersTable.invitationState"),
      meta: { filterType: "select" },
    },
  ];

  useEffect((): void => {
    setColumnVisibility({
      invitation: hasInvitationPermissions,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasInvitationPermissions]);

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
                    <Tooltip
                      id={"authorsGrantTooltip"}
                      tip={t("group.authors.tooltip.text")}
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
                    </Tooltip>
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

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

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
        columnFilterSetter={columnFiltersSetter}
        columnFilterState={columnFilters}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={[
          ...columns,
          ...(hasInvitationPermissions ? columnsExtra : []),
        ]}
        data={datasetText}
        enableColumnFilters={true}
        exportCsv={true}
        id={"tblAuthorsList"}
        paginationSetter={setpagination}
        paginationState={pagination}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
    </React.StrictMode>
  );
};

export { GroupAuthorsView };
