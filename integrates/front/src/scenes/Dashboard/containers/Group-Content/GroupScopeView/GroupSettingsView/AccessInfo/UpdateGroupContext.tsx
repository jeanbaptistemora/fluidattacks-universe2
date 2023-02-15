import MDEditor from "@uiw/react-md-editor";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IFieldProps } from "./GroupContextForm";

import { Alert } from "components/Alert";
import { ValidationError } from "utils/forms/fields/styles";

export const UpdateGroupContext: React.FC<IFieldProps> = ({
  field,
  form: { values, setFieldValue },
}: IFieldProps): JSX.Element => {
  const { t } = useTranslation();

  const handleMDChange = useCallback(
    (value: string | undefined): void => {
      setFieldValue("groupContext", value);
    },
    [setFieldValue]
  );

  return (
    <React.Fragment>
      <MDEditor
        height={200}
        highlightEnable={false}
        onChange={handleMDChange}
        // PrefixCls={""}
        value={values.groupContext}
      />
      <ValidationError>
        <ErrorMessage name={field.name} />
      </ValidationError>
      <Alert>
        {"*"}&nbsp;
        {t("searchFindings.groupAccessInfoSection.markdownAlert")}
      </Alert>
    </React.Fragment>
  );
};
