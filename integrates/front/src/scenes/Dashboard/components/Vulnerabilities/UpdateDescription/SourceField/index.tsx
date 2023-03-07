import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IUpdateVulnerabilityForm } from "../../types";
import { Editable, Select } from "components/Input";
import { authzPermissionsContext } from "utils/authz/config";
import { required } from "utils/validations";

const SourceField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canSeeSource: boolean = permissions.can("see_vulnerability_source");
  const canUpdateVulnerabilityDescription: boolean = permissions.can(
    "api_mutations_update_vulnerability_description_mutate"
  );

  const { initialValues } = useFormikContext<IUpdateVulnerabilityForm>();

  return canSeeSource && canUpdateVulnerabilityDescription ? (
    <Editable
      currentValue={""}
      isEditing={true}
      label={t("searchFindings.tabVuln.vulnTable.source")}
    >
      <Select
        label={t("searchFindings.tabVuln.vulnTable.source")}
        name={"source"}
        validate={_.isEmpty(initialValues.source) ? undefined : required}
      >
        <option value={""} />
        <option value={"ANALYST"}>
          {t(`searchFindings.tabVuln.vulnTable.vulnerabilitySource.ANALYST`)}
        </option>
        <option value={"CUSTOMER"}>
          {t(`searchFindings.tabVuln.vulnTable.vulnerabilitySource.CUSTOMER`)}
        </option>
        <option value={"DETERMINISTIC"}>
          {t(
            `searchFindings.tabVuln.vulnTable.vulnerabilitySource.DETERMINISTIC`
          )}
        </option>
        <option value={"ESCAPE"}>
          {t(`searchFindings.tabVuln.vulnTable.vulnerabilitySource.ESCAPE`)}
        </option>
        <option value={"MACHINE"}>
          {t(`searchFindings.tabVuln.vulnTable.vulnerabilitySource.MACHINE`)}
        </option>
      </Select>
    </Editable>
  ) : (
    <div />
  );
};

export { SourceField };
