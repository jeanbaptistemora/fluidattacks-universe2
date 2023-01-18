import React from "react";
import { useTranslation } from "react-i18next";

import { InputDateTime } from "components/Input";
import {
  composeValidators,
  dateTimeBeforeToday,
  required,
} from "utils/validations";

const ModifiedDateField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <InputDateTime
      label={t("group.toe.lines.addModal.fields.modifiedDate")}
      name={"modifiedDate"}
      validate={composeValidators([required, dateTimeBeforeToday])}
    />
  );
};

export { ModifiedDateField };
