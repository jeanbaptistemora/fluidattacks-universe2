import React from "react";
import { useTranslation } from "react-i18next";

import { TextArea } from "components/Input";
import { FormGroup } from "styles/styledComponents";
import {
  composeValidators,
  required,
  validCsvInput,
  validTextField,
} from "utils/validations";

const FilenameField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <TextArea
        label={t("group.toe.lines.addModal.fields.filename")}
        name={"filename"}
        validate={composeValidators([required, validCsvInput, validTextField])}
      />
    </FormGroup>
  );
};

export { FilenameField };
