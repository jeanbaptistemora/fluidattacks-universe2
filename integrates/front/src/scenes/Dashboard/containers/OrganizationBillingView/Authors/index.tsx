/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Table } from "components/Table";
import { Text } from "components/Text";
import type {
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";

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
        const groups: string = author.groups.join(", ");

        return {
          ...author,
          actor,
          groups,
        };
      }
    );

  const tableColumns: ColumnDef<IOrganizationAuthorsTable>[] = [
    {
      accessorKey: "actor",
      header: t("organization.tabs.billing.authors.headers.authorName"),
    },
    {
      accessorKey: "groups",
      header: t("organization.tabs.billing.authors.headers.groups"),
    },
  ];

  const dataset: IOrganizationAuthorsTable[] = formatAuthorsData(authors);

  return (
    <div>
      <Text fw={7} mb={3} mt={4} size={"big"}>
        {t("organization.tabs.billing.authors.title")}
      </Text>
      <Table
        columns={tableColumns}
        data={dataset}
        enableColumnFilters={true}
        id={"tblGroups"}
      />
    </div>
  );
};
