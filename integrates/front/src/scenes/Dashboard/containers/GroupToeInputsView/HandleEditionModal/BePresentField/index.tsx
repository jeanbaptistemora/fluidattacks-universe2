import { Field, useFormikContext } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";

const BePresentField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const { setFieldValue } = useFormikContext<IFormValues>();

  function handleBePresenBtnChange(bePresent: boolean): void {
    setFieldValue("bePresent", bePresent);
  }

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.inputs.editModal.fields.bePresent")}</b>
      </ControlLabel>
      <Field
        component={FormikSwitchButton}
        name={"bePresent"}
        offlabel={t("group.toe.inputs.no")}
        onChange={handleBePresenBtnChange}
        onlabel={t("group.toe.inputs.yes")}
        type={"checkbox"}
      />
    </FormGroup>
  );
};

export { BePresentField };
