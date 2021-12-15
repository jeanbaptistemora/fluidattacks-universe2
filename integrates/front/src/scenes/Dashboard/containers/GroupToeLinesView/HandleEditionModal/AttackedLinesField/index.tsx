import { Field } from "formik";
import { min } from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedLinesFieldProps } from "./types";

import type { IToeLinesData } from "../../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  numeric,
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
        name={"attackedLines"}
        type={"number"}
        validate={composeValidators([
          optionalNumberBetween(1, maxSelectedLoc),
          numeric,
        ])}
      />
    </FormGroup>
  );
};

export { AttackedLinesField };
