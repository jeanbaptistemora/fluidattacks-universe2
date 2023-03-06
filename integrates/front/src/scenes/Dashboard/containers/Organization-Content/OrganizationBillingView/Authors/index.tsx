import type { ColumnDef } from "@tanstack/react-table";
import _, { isNull, isUndefined } from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import type {
  IOrganizationActiveGroupAttr,
  IOrganizationActorAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
} from "../types";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { Text } from "components/Text";

interface IOrganizationAuthorAttrsProps {
  authors: IOrganizationAuthorAttr[];
}

export const OrganizationAuthors: React.FC<IOrganizationAuthorAttrsProps> = ({
  authors,
}: IOrganizationAuthorAttrsProps): JSX.Element => {
  const { t } = useTranslation();

  const formatActor = (actor: string): IOrganizationActorAttr | undefined => {
    const textMatch: RegExpMatchArray | null =
      /^(?<name>.+) <(?<email>[^>]+)>$/u.exec(actor);
    if (isNull(textMatch)) {
      return undefined;
    }

    if (isUndefined(textMatch.groups)) {
      return undefined;
    }
    const { email, name } = textMatch.groups;

    return { email, name };
  };

  const formatAuthorsData = (
    authorData: IOrganizationAuthorAttr[]
  ): IOrganizationAuthorsTable[] =>
    authorData.map(
      (author: IOrganizationAuthorAttr): IOrganizationAuthorsTable => {
        const actor: IOrganizationActorAttr | undefined = formatActor(
          author.actor
        );
        const actorName: string = _.capitalize(actor?.name);
        const actorEmail = actor?.email;
        const groupsAuthors: string = author.activeGroups
          .map((group: IOrganizationActiveGroupAttr): string => group.name)
          .join(", ");

        return {
          actorEmail,
          actorName,
          groupsAuthors,
        };
      }
    );

  const tableColumns: ColumnDef<IOrganizationAuthorsTable>[] = [
    {
      accessorKey: "actorName",
      header: t("organization.tabs.billing.authors.headers.authorName"),
    },
    {
      accessorKey: "actorEmail",
      header: t("organization.tabs.billing.authors.headers.authorEmail"),
    },
    {
      accessorKey: "groupsAuthors",
      header: t("organization.tabs.billing.authors.headers.activeGroups"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<IOrganizationAuthorsTable>[]>([
    {
      id: "actorEmail",
      key: "actorEmail",
      label: t("organization.tabs.billing.authors.headers.authorEmail"),
      type: "text",
    },
    {
      id: "actorName",
      key: "actorName",
      label: t("organization.tabs.billing.authors.headers.authorName"),
      type: "text",
    },
    {
      id: "groupsAuthors",
      key: "groupsAuthors",
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
        csvHeaders={{
          groupsAuthors: t(
            "organization.tabs.billing.authors.headers.activeGroups"
          ),
        }}
        csvName={t("organization.tabs.billing.authors.title")}
        data={filteredDataset}
        exportCsv={true}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblGroups"}
      />
    </div>
  );
};
