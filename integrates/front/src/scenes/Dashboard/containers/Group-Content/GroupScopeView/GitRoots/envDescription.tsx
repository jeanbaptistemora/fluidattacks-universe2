import React from "react";
import { useTranslation } from "react-i18next";

import { Row } from "components/Layout";
import { formatDate } from "utils/formatHelpers";

interface IDescriptionProps {
  repositoryUrls: string[];
  createdAt: Date | null;
  createdBy: string | null;
  url: string;
}

const Description = ({
  repositoryUrls,
  createdAt,
  createdBy,
  url,
}: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <div>
      <h3>{t("group.scope.git.envUrl")}</h3>
      <Row>
        <ul className={"list"}>
          <li className={"pv1"}>
            <a href={url} rel={"noreferrer"} target={"_blank"}>
              {url}
            </a>
          </li>
          <li className={"pv1"}>{`${t(
            "group.scope.git.createdAt"
          )} ${formatDate(createdAt as unknown as string)}`}</li>
          {createdBy === null ? undefined : (
            <li className={"pv1"}>{`${t(
              "group.scope.git.createdBy"
            )} ${createdBy}`}</li>
          )}
        </ul>
      </Row>
      <h3>{t("group.scope.git.title")}</h3>
      <Row>
        <ul className={"list"}>
          {repositoryUrls.map(
            (_url): JSX.Element => (
              <li key={_url}>{_url}</li>
            )
          )}
        </ul>
      </Row>
    </div>
  );
};

export const renderEnvDescription = (props: IDescriptionProps): JSX.Element => (
  <Description
    createdAt={props.createdAt}
    createdBy={props.createdBy}
    repositoryUrls={props.repositoryUrls}
    url={props.url}
  />
);
