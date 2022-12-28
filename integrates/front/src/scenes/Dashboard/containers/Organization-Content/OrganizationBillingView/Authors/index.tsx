import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { Text } from "components/Text";
import type {
  IOrganizationActiveGroupAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/types";

interface IOrganizationAuthorAttrsProps {
  authors: IOrganizationAuthorAttr[];
}

export const OrganizationAuthors: React.FC<IOrganizationAuthorAttrsProps> = ({
  authors,
}: IOrganizationAuthorAttrsProps): JSX.Element => {
  const { t } = useTranslation();

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
      <Table
        columns={tableColumns}
        data={filteredDataset}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblGroups"}
      />
    </div>
  );
};
