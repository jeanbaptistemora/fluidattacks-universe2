import React from "react";
import { useTranslation } from "react-i18next";

import { Input } from "components/Input";
import { FormGroup } from "styles/styledComponents";
import {
  composeValidators,
  required,
  validCommitHash,
} from "utils/validations";

const LastCommitField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Input
        label={t("group.toe.lines.addModal.fields.lastCommit")}
        name={"lastCommit"}
        type={"text"}
        validate={composeValidators([required, validCommitHash])}
      />
    </FormGroup>
  );
};

export { LastCommitField };
