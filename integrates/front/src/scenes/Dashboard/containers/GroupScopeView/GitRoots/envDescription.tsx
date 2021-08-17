import React from "react";
import { useTranslation } from "react-i18next";

import { Row } from "styles/styledComponents";

interface IDescriptionProps {
  repositoryUrls: string[];
}

const Description = ({ repositoryUrls }: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <div>
      <h3>{t("group.scope.git.title")}</h3>
      <Row>
        <ul>
          {repositoryUrls.map(
            (url): JSX.Element => (
              <li key={url}>{url}</li>
            )
          )}
        </ul>
      </Row>
    </div>
  );
};

export const renderEnvDescription = (props: IDescriptionProps): JSX.Element => (
  <Description repositoryUrls={props.repositoryUrls} />
);
