import MDEditor from "@uiw/react-md-editor";
import type { FieldInputProps } from "formik";
import { ErrorMessage, Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { Alert } from "components/Alert";
import { Text } from "components/Text";
import type { IGroupAccessInfo } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo";
import { ActionButtons } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/ActionButtons";
import { ValidationError } from "utils/forms/fields/styles";
import { maxLength } from "utils/validations";

const MAX_GROUP_CONTEXT_LENGTH = 20000;

const maxGroupContextLength: ConfigurableValidator = maxLength(
  MAX_GROUP_CONTEXT_LENGTH
);

interface IGroupContextForm {
  data: IGroupAccessInfo | undefined;
  isEditing: boolean;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

/* eslint-disable react/no-unused-prop-types */
interface IFieldProps {
  field: FieldInputProps<string>;
  form: {
    values: {
      disambiguation: string;
      groupContext: string;
    };
    setFieldValue: (
      field: string,
      value: string | undefined,
      shouldValidate?: boolean | undefined
    ) => void;
  };
}
/* eslint-disable react/no-unused-prop-types */

const GroupContextForm: React.FC<IGroupContextForm> = ({
  data,
  isEditing,
  setEditing,
}: IGroupContextForm): JSX.Element => {
  const { dirty, resetForm, submitForm } = useFormikContext();
  const isGroupAccessInfoPristine = !dirty;
  const { t } = useTranslation();

  const toggleEdit: () => void = useCallback((): void => {
    if (!isGroupAccessInfoPristine) {
      resetForm();
    }
    setEditing(!isEditing);
  }, [isGroupAccessInfoPristine, isEditing, resetForm, setEditing]);

  const handleSubmit: () => void = useCallback((): void => {
    if (!isGroupAccessInfoPristine) {
      void submitForm();
    }
  }, [isGroupAccessInfoPristine, submitForm]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset = data.group;

  return (
    <React.StrictMode>
      <Form id={"editGroupAccessInfo"}>
        {isEditing ? (
          <Field name={"groupContext"} validate={maxGroupContextLength}>
            {({
              field,
              form: { values, setFieldValue },
            }: IFieldProps): JSX.Element => {
              function handleMDChange(value: string | undefined): void {
                setFieldValue("groupContext", value);
              }

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
            }}
          </Field>
        ) : dataset.groupContext ? (
          <div data-color-mode={"light"}>
            <MDEditor.Markdown
              source={dataset.groupContext}
              // eslint-disable-next-line react/forbid-component-props
              style={{ backgroundColor: "inherit" }}
            />
          </div>
        ) : (
          <Text mb={2}>
            {t("searchFindings.groupAccessInfoSection.noGroupContext")}
          </Text>
        )}
        <ActionButtons
          editTooltip={t(
            "searchFindings.groupAccessInfoSection.tooltips.editGroupContext"
          )}
          isEditing={isEditing}
          isPristine={isGroupAccessInfoPristine}
          onEdit={toggleEdit}
          onUpdate={handleSubmit}
          permission={"api_mutations_update_group_access_info_mutate"}
        />
      </Form>
    </React.StrictMode>
  );
};

export type { IFieldProps };
export { GroupContextForm };
