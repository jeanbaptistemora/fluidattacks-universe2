import MDEditor from "@uiw/react-md-editor";
import { ErrorMessage, Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { Alert } from "components/Alert";
import { Text } from "components/Text";
import type { IGroupAccessInfo } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo";
import { ActionButtons } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/ActionButtons";
import type { IFieldProps } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/GroupContextForm";
import { ValidationError } from "utils/forms/fields/styles";
import { maxLength } from "utils/validations";

const MAX_DISAMBIGUATION_INFO_LENGTH = 10000;

const maxDisambiguationInfoLength: ConfigurableValidator = maxLength(
  MAX_DISAMBIGUATION_INFO_LENGTH
);

interface IDisambiguationForm {
  data: IGroupAccessInfo | undefined;
  isEditing: boolean;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const DisambiguationForm: React.FC<IDisambiguationForm> = ({
  data,
  isEditing,
  setEditing,
}: IDisambiguationForm): JSX.Element => {
  const { dirty, resetForm, submitForm } = useFormikContext();
  const isDisambiguationInfoPristine = !dirty;
  const { t } = useTranslation();

  const toggleEdit: () => void = useCallback((): void => {
    if (!isDisambiguationInfoPristine) {
      resetForm();
    }
    setEditing(!isEditing);
  }, [isDisambiguationInfoPristine, isEditing, resetForm, setEditing]);

  const handleSubmit: () => void = useCallback((): void => {
    if (!isDisambiguationInfoPristine) {
      void submitForm();
    }
  }, [isDisambiguationInfoPristine, submitForm]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset = data.group;

  return (
    <React.StrictMode>
      <Form id={"editDisambiguationInfo"}>
        {isEditing ? (
          <Field name={"disambiguation"} validate={maxDisambiguationInfoLength}>
            {({
              field,
              form: { values, setFieldValue },
            }: IFieldProps): JSX.Element => {
              function handleMDChange(value: string | undefined): void {
                setFieldValue("disambiguation", value);
              }

              return (
                <React.Fragment>
                  <MDEditor
                    height={200}
                    highlightEnable={false}
                    onChange={handleMDChange}
                    value={values.disambiguation}
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
        ) : dataset.disambiguation ? (
          <MDEditor.Markdown prefixCls={""} source={dataset.disambiguation} />
        ) : (
          <Text mb={2}>
            {t("searchFindings.groupAccessInfoSection.noDisambiguation")}
          </Text>
        )}
        <ActionButtons
          editTooltip={t(
            "searchFindings.groupAccessInfoSection.tooltips.editDisambiguationInfo"
          )}
          isEditing={isEditing}
          isPristine={isDisambiguationInfoPristine}
          onEdit={toggleEdit}
          onUpdate={handleSubmit}
          permission={"api_mutations_update_group_disambiguation_mutate"}
        />
      </Form>
    </React.StrictMode>
  );
};

export { DisambiguationForm };
