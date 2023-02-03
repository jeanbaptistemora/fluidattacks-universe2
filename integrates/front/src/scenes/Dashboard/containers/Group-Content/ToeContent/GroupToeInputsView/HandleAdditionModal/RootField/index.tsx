import React from "react";

import type { IRootFieldProps } from "./types";

import type { Root } from "../types";
import { Select } from "components/Input";
import { FormGroup } from "styles/styledComponents";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const RootField: React.FC<IRootFieldProps> = (
  props: IRootFieldProps
): JSX.Element => {
  const { roots } = props;

  return (
    <FormGroup>
      <Select
        label={translate.t("group.toe.inputs.addModal.fields.root")}
        name={"rootId"}
        validate={required}
      >
        {roots.map((root: Root): JSX.Element => {
          return (
            <option key={root.id} value={root.id}>
              {root.nickname}
            </option>
          );
        })}
      </Select>
    </FormGroup>
  );
};

export { RootField };
