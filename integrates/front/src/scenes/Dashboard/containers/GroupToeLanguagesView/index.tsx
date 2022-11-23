import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GET_TOE_LANGUAGES } from "./queries";
import type { ICodeLanguage } from "./types";

import { formatPercentage } from "../GroupToeLinesView/utils";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Text } from "components/Text";
import { Logger } from "utils/logger";

export const GroupToeLanguagesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const { data } = useQuery<{
    group: {
      codeLanguages: ICodeLanguage[] | null;
    };
  }>(GET_TOE_LANGUAGES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load group toe languages", error);
      });
    },
    variables: {
      groupName,
    },
  });

  if (data === undefined) {
    return <div />;
  }

  const languages =
    data.group.codeLanguages === null ? [] : data.group.codeLanguages;

  const totalLoc = languages.reduce(
    (total, language): number => total + language.loc,
    0
  );
  const completeData: ICodeLanguage[] = languages.map(
    (lang): ICodeLanguage => ({
      language: lang.language,
      loc: lang.loc,
      percentage: lang.loc / totalLoc,
    })
  );

  return (
    <Fragment>
      <Text fw={7} mb={3} mt={4} size={"big"}>
        {t("group.toe.codeLanguages.title")}
      </Text>
      <Table
        columns={[
          {
            accessorKey: "language",
            header: String(t("group.toe.codeLanguages.lang")),
          },
          {
            accessorKey: "loc",
            header: String(t("group.toe.codeLanguages.loc")),
          },
          {
            accessorKey: "percentage",
            cell: (cell: ICellHelper<ICodeLanguage>): string =>
              formatPercentage(cell.getValue()),
            header: String(t("group.toe.codeLanguages.percent")),
          },
        ]}
        data={completeData}
        id={"tblCodeLanguages"}
      />
    </Fragment>
  );
};
