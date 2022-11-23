import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ITagFieldProps } from "./types";

import { ControlLabel } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikTagInput } from "utils/forms/fields";

const TagField: React.FC<ITagFieldProps> = ({
  handleDeletion,
  hasNewVulnSelected,
  isAcceptedSelected,
  isAcceptedUndefinedSelected,
  isInProgressSelected,
}: ITagFieldProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canDeleteVulnsTags: boolean = permissions.can(
    "api_mutations_remove_vulnerability_tags_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <div className={"mb4 nt2 w-100"}>
          <ControlLabel>
            <b>{t("searchFindings.tabDescription.tag")}</b>
          </ControlLabel>
          <Field
            component={FormikTagInput}
            disabled={!(canUpdateVulnsTreatment && canDeleteVulnsTags)}
            name={"tag"}
            onDeletion={handleDeletion}
            placeholder={""}
            type={"text"}
          />
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { TagField };
