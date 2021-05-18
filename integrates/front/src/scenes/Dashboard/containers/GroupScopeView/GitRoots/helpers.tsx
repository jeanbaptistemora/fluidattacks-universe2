import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { BaseSchema } from "yup";
import { array, lazy, object, string } from "yup";

import type { IGitRootAttr } from "../types";
import { Alert } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IGitIgnoreAlertProps {
  gitignore: string[];
}

const GitIgnoreAlert: React.FC<IGitIgnoreAlertProps> = (
  props: IGitIgnoreAlertProps
): JSX.Element => {
  const { gitignore } = props;
  const { t } = useTranslation();

  if (_.isUndefined(gitignore)) {
    return <div />;
  }

  return _.isEmpty(gitignore) ? (
    <div />
  ) : (
    <Alert>{t("group.scope.git.filter.warning")}</Alert>
  );
};

const gitModalSchema = lazy(
  (values: IGitRootAttr): BaseSchema =>
    object().shape({
      gitignore: array().of(
        string()
          .required(translate.t("validations.required"))
          .test(
            "excludeFormat",
            translate.t("validations.excludeFormat"),
            (value): boolean => {
              const repoUrl = values.url;

              if (!_.isUndefined(repoUrl) && !_.isUndefined(value)) {
                const [urlBasename] = repoUrl.split("/").slice(-1);
                const repoName: string = urlBasename.endsWith(".git")
                  ? urlBasename.replace(".git", "")
                  : urlBasename;

                return (
                  value
                    .toLowerCase()
                    .split("/")
                    .indexOf(repoName.toLowerCase()) !== 0
                );
              }

              return false;
            }
          )
      ),
    })
);

export { GitIgnoreAlert, gitModalSchema };
