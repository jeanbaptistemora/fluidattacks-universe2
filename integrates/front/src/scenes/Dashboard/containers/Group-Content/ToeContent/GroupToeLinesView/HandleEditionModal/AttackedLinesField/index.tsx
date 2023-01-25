import { Field } from "formik";
import { min } from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedLinesFieldProps } from "./types";

import type { IToeLinesData } from "../../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  isOptionalInteger,
  optionalNumberBetween,
} from "utils/validations";

const AttackedLinesField: React.FC<IAttackedLinesFieldProps> = (
  props: IAttackedLinesFieldProps
): JSX.Element => {
  const { selectedToeLinesDatas } = props;
  const { t } = useTranslation();

  const maxSelectedLoc: number =
    min(
      selectedToeLinesDatas.map(
        (toeLinesData: IToeLinesData): number => toeLinesData.loc
      )
    ) ?? 1;

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLInputElement>): void => {
      if (event.key.length > 1 || /\d/u.test(event.key)) return;
      event.preventDefault();
    },
    []
  );

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.editModal.fields.attackedLines")}</b>&nbsp;
        <i>
          {`(${t("group.toe.lines.editModal.fields.attackedLinesComment")})`}
        </i>
      </ControlLabel>
      <Field
        component={FormikText}
        min={"0"}
        name={"attackedLines"}
        onKeyDown={handleKeyDown}
        step={"1"}
        type={"number"}
        validate={composeValidators([
          isOptionalInteger,
          optionalNumberBetween(0, maxSelectedLoc),
        ])}
      />
    </FormGroup>
  );
};

export { AttackedLinesField };
