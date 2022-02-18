import { Field } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IComponentFieldProps } from "./types";

import { ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { validPath } from "utils/validations";

const ComponentField: React.FC<IComponentFieldProps> = (
  props: IComponentFieldProps
): JSX.Element => {
  const { host } = props;
  const { t } = useTranslation();

  const validatePath: ConfigurableValidator = validPath(host);

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.inputs.addModal.fields.component")} </b>
      </ControlLabel>
      <Row>
        {_.isUndefined(host) ? undefined : <span>{host}</span>}
        <Field
          component={FormikText}
          disabled={false}
          name={"path"}
          placeholder={t("group.toe.inputs.addModal.fields.path")}
          type={"text"}
          validate={validatePath}
        />
      </Row>
    </FormGroup>
  );
};

export { ComponentField };
