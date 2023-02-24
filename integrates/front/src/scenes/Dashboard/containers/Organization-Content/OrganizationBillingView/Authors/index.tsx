import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type {
  IGetOrganizationBilling,
  IOrganizationActiveGroupAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
} from "./types";

import { GET_ORGANIZATION_AUTHORS_BILLING } from "../queries";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { FormikSelect } from "components/Input/Formik/FormikSelect";
import { Col, Row } from "components/Layout";
import { Table } from "components/Table";
import { Text } from "components/Text";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IOrganizationAuthorAttrsProps {
  organizationId: string;
}

export const OrganizationAuthors: React.FC<IOrganizationAuthorAttrsProps> = ({
  organizationId,
}: IOrganizationAuthorAttrsProps): JSX.Element => {
  const { t } = useTranslation();
  const now: Date = new Date();
  const thisYear: number = now.getFullYear();
  const thisMonth: number = now.getMonth();
  const DATE_RANGE = 12;
  const dateRange: Date[] = _.range(0, DATE_RANGE).map(
    (month: number): Date => new Date(thisYear, thisMonth - month)
  );
  const [billingDate, setBillingDate] = useState(dateRange[0].toISOString());
  const { data } = useQuery<IGetOrganizationBilling>(
    GET_ORGANIZATION_AUTHORS_BILLING,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred getting billing data", error);
        });
      },
      variables: { date: billingDate, organizationId },
    }
  );
  const authors: IOrganizationAuthorAttr[] =
    data === undefined ? [] : data.organization.billing.authors;
  const handleDateChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      setBillingDate(event.target.value);
    },
    []
  );
  const formatDate: (date: Date) => string = (date: Date): string => {
    const month: number = date.getMonth() + 1;
    const monthStr: string = month.toString();

    return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
  };
  const formatAuthorsData = (
    authorData: IOrganizationAuthorAttr[]
  ): IOrganizationAuthorsTable[] =>
    authorData.map(
      (author: IOrganizationAuthorAttr): IOrganizationAuthorsTable => {
        const actor: string = _.capitalize(author.actor);
        const activeGroups: string = author.activeGroups
          .map((group: IOrganizationActiveGroupAttr): string => group.name)
          .join(", ");

        return {
          ...author,
          activeGroups,
          actor,
        };
      }
    );

  const tableColumns: ColumnDef<IOrganizationAuthorsTable>[] = [
    {
      accessorKey: "actor",
      header: t("organization.tabs.billing.authors.headers.authorName"),
    },
    {
      accessorKey: "activeGroups",
      header: t("organization.tabs.billing.authors.headers.activeGroups"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<IOrganizationAuthorsTable>[]>([
    {
      id: "actor",
      key: "actor",
      label: t("organization.tabs.billing.authors.headers.authorName"),
      type: "text",
    },
    {
      id: "activeGroups",
      key: "activeGroups",
      label: t("organization.tabs.billing.authors.headers.activeGroups"),
      type: "text",
    },
  ]);

  const dataset: IOrganizationAuthorsTable[] = formatAuthorsData(authors);

  const filteredDataset = useFilters(dataset, filters);

  return (
    <div>
      <Text fw={7} mb={3} mt={4} size={"big"}>
        {t("organization.tabs.billing.authors.title")}
      </Text>
      <Row>
        <Row>{t("organization.tabs.billing.authors.label")}</Row>
        <Col lg={10} md={10}>
          <FormikSelect
            field={{
              name: "billingDate",
              onBlur: (): void => undefined,
              onChange: handleDateChange,
              value: billingDate,
            }}
            form={{ errors: {}, touched: {} }}
            name={"billingDate"}
          >
            {dateRange.map(
              (date: Date): JSX.Element => (
                <option key={date.toISOString()} value={date.toISOString()}>
                  {formatDate(date)}
                </option>
              )
            )}
          </FormikSelect>
        </Col>
      </Row>
      <Table
        columns={tableColumns}
        data={filteredDataset}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblGroups"}
      />
    </div>
  );
};
