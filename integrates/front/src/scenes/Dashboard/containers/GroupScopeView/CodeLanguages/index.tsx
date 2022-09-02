import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { ICodeLanguage } from "../types";
import { Table } from "components/Table";
import { Text } from "components/Text";

interface ICodeLanguagesProps {
  languages: ICodeLanguage[] | null;
}

export const CodeLanguages: React.FC<ICodeLanguagesProps> = ({
  languages,
}: ICodeLanguagesProps): JSX.Element => {
  const { t } = useTranslation();
  if (languages === null) {
    return <div />;
  }

  const totalLoc = languages.reduce(
    (total, language): number => total + language.loc,
    0
  );
  const data: ICodeLanguage[] = languages.map(
    (lang): ICodeLanguage => ({
      language: lang.language,
      loc: lang.loc,
      percentage: `${Math.round((lang.loc * 100) / totalLoc)}%`,
    })
  );

  return (
    <Fragment>
      <Text fw={7} mb={3} mt={4} size={5}>
        {t("group.scope.codeLanguages.title")}
      </Text>
      <Table
        dataset={data}
        exportCsv={false}
        headers={[
          {
            dataField: "language",
            header: t("group.scope.codeLanguages.lang"),
            nonToggleList: true,
            visible: true,
          },
          {
            dataField: "loc",
            header: t("group.scope.codeLanguages.loc"),
            nonToggleList: true,
            visible: true,
          },
          {
            dataField: "percentage",
            header: t("group.scope.codeLanguages.percent"),
            nonToggleList: true,
            visible: true,
          },
        ]}
        id={"codeLanguages"}
        pageSize={5}
        search={false}
      />
    </Fragment>
  );
};
