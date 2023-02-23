import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IComponentFieldProps } from "./types";

import { Input } from "components/Input";
import { Row } from "components/Layout";
import { FormGroup } from "styles/styledComponents";
import {
  composeValidators,
  validPath,
  validTextField,
} from "utils/validations";

const ComponentField: React.FC<IComponentFieldProps> = (
  props: IComponentFieldProps
): JSX.Element => {
  const { host } = props;
  const { t } = useTranslation();

  const validatePath: ConfigurableValidator = validPath(host);

  return (
    <FormGroup>
      <Row>
        {_.isUndefined(host) ? undefined : <span>{host}</span>}
        {_.isString(host) && host.includes("?") ? undefined : (
          <Input
            disabled={false}
            label={t("group.toe.inputs.addModal.fields.component")}
            name={"path"}
            placeholder={t("group.toe.inputs.addModal.fields.path")}
            type={"text"}
            validate={composeValidators([validatePath, validTextField])}
          />
        )}
      </Row>
    </FormGroup>
  );
};

export { ComponentField };
