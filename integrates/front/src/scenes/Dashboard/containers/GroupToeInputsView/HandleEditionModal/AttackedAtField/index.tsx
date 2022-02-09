import { Field, useFormikContext } from "formik";
import _ from "lodash";
import type { Moment } from "moment";
import moment, { max } from "moment";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedAtFieldProps } from "./types";

import type { IToeInputData } from "../../types";
import type { IFormValues } from "../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDateTime } from "utils/forms/fields";
import {
  composeValidators,
  optionalDateTimeBetween,
  validOptionalDatetime,
} from "utils/validations";

const AttackedAtField: React.FC<IAttackedAtFieldProps> = (
  props: IAttackedAtFieldProps
): JSX.Element => {
  const { selectedToeInputDatas } = props;
  const { t } = useTranslation();

  const {
    values: { bePresent },
    setFieldValue,
  } = useFormikContext<IFormValues>();

  const from: Moment = max(
    selectedToeInputDatas.map(
      (toeLinesData: IToeInputData): Moment =>
        _.isUndefined(toeLinesData.attackedAt)
          ? moment(toeLinesData.seenAt)
          : moment(toeLinesData.attackedAt)
    )
  );

  useEffect((): void => {
    if (bePresent) {
      setFieldValue("attackedAt", moment().add(-1, "second"));
    } else {
      setFieldValue("attackedAt", undefined);
    }
  }, [bePresent, setFieldValue]);

  return (
    <FormGroup>
      {bePresent ? (
        <React.Fragment>
          <ControlLabel>
            <b>{t("group.toe.inputs.editModal.fields.attackedAt")}</b>
          </ControlLabel>
          <Field
            component={FormikDateTime}
            name={"attackedAt"}
            type={"date"}
            validate={composeValidators([
              validOptionalDatetime,
              optionalDateTimeBetween(from, moment()),
            ])}
          />
        </React.Fragment>
      ) : undefined}
    </FormGroup>
  );
};

export { AttackedAtField };
