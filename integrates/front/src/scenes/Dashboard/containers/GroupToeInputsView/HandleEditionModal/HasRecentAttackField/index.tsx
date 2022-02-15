import { Field, useFormikContext } from "formik";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";

const HasRecentAttack: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const {
    values: { bePresent },
    setFieldValue,
  } = useFormikContext<IFormValues>();

  function handleHasRecentAttackBtnChange(hasRecentAttack: boolean): void {
    setFieldValue("hasRecentAttack", hasRecentAttack);
  }

  useEffect((): void => {
    if (bePresent) {
      setFieldValue("hasRecentAttack", true);
    } else {
      setFieldValue("hasRecentAttack", undefined);
    }
  }, [bePresent, setFieldValue]);

  return (
    <FormGroup>
      {bePresent ? (
        <React.Fragment>
          <ControlLabel>
            <b>{t("group.toe.inputs.editModal.fields.hasRecentAttack")}</b>
          </ControlLabel>
          <Field
            component={FormikSwitchButton}
            name={"hasRecentAttack"}
            offlabel={t("group.toe.inputs.no")}
            onChange={handleHasRecentAttackBtnChange}
            onlabel={t("group.toe.inputs.yes")}
            type={"checkbox"}
          />
        </React.Fragment>
      ) : undefined}
    </FormGroup>
  );
};

export { HasRecentAttack };
