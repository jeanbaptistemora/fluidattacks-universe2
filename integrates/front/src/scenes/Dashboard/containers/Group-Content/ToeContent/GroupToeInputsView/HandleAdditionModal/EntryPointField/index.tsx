import React from "react";
import { useTranslation } from "react-i18next";

import { Input } from "components/Input";
import { FormGroup } from "styles/styledComponents";
import { composeValidators, validTextField } from "utils/validations";

const EntryPointField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Input
        label={t("group.toe.inputs.addModal.fields.entryPoint")}
        name={"entryPoint"}
        type={"text"}
        validate={composeValidators([validTextField])}
      />
    </FormGroup>
  );
};

export { EntryPointField };
