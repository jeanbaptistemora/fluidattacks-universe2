import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { TextArea } from "components/Input";
import { FormGroup } from "styles/styledComponents";
import {
  composeValidators,
  maxLength,
  validCsvInput,
  validTextField,
} from "utils/validations";

const MAX_COMMENTS_LENGTH: number = 200;
const maxCommentsLength: ConfigurableValidator = maxLength(MAX_COMMENTS_LENGTH);
const CommentsField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <TextArea
        label={t("group.toe.lines.editModal.fields.comments")}
        name={"comments"}
        validate={composeValidators([
          validTextField,
          maxCommentsLength,
          validCsvInput,
        ])}
      />
    </FormGroup>
  );
};

export { CommentsField };
