import { Field } from "formik";
import _ from "lodash";
import type { Moment } from "moment";
import moment, { max } from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedAtFieldProps } from "./types";

import type { IToeLinesData } from "../../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDateTime } from "utils/forms/fields";
import {
  composeValidators,
  dateTimeBetween,
  required,
  validDatetime,
} from "utils/validations";

const AttackedAtField: React.FC<IAttackedAtFieldProps> = (
  props: IAttackedAtFieldProps
): JSX.Element => {
  const { selectedToeLinesDatas } = props;
  const { t } = useTranslation();

  const from: Moment = max(
    selectedToeLinesDatas.map(
      (toeLinesData: IToeLinesData): Moment =>
        _.isEmpty(toeLinesData.attackedAt)
          ? moment(toeLinesData.seenAt)
          : moment(toeLinesData.attackedAt)
    )
  );

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.editModal.fields.attackedAt")}</b>
      </ControlLabel>
      <Field
        component={FormikDateTime}
        name={"attackedAt"}
        type={"date"}
        validate={composeValidators([
          required,
          validDatetime,
          dateTimeBetween(from, moment()),
        ])}
      />
    </FormGroup>
  );
};

export { AttackedAtField };
