import { Field } from "redux-form";
import type { ITagFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TagInput } from "utils/forms/fields";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { ControlLabel, FormGroup } from "styles/styledComponents";

const TagField: React.FC<ITagFieldProps> = (
  props: ITagFieldProps
): JSX.Element => {
  const {
    handleDeletion,
    hasNewVulnSelected,
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
  } = props;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );
  const canDeleteVulnsTags: boolean = permissions.can(
    "backend_api_mutations_delete_vulnerability_tags_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <FormGroup>
          <ControlLabel>
            <b>{translate.t("searchFindings.tabDescription.tag")}</b>
          </ControlLabel>
          <Field
            component={TagInput}
            name={"tag"}
            onDeletion={handleDeletion}
            readOnly={!(canUpdateVulnsTreatment && canDeleteVulnsTags)}
            type={"text"}
          />
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { TagField };
