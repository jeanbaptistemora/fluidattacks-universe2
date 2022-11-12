/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IUpdateVulnerabilityForm } from "../../types";
import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikDropdown } from "utils/forms/fields";
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
    <EditableField
      component={FormikDropdown}
      currentValue={""}
      label={t("searchFindings.tabVuln.vulnTable.source")}
      name={"source"}
      renderAsEditable={true}
      type={"text"}
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
    </EditableField>
  ) : (
    <div />
  );
};

export { SourceField };