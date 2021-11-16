import MDEditor from "@uiw/react-md-editor";
import type { FieldInputProps } from "formik";
import { ErrorMessage, Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IGroupAccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import { ActionButtons } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/ActionButtons";
import {
  Alert,
  Col25,
  Flex,
  GroupScopeTextWide,
  Row,
} from "styles/styledComponents";
import { ValidationError } from "utils/forms/fields/styles";
import { maxLength } from "utils/validations";

const MAX_GROUP_CONTEXT_LENGTH = 10000;

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
      sastAccess: string;
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
        <Flex>
          <h2>{t("searchFindings.groupAccessInfoSection.groupContext")}</h2>
        </Flex>
        <Row>
          {dataset.sastAccess || isEditing ? (
            <GroupScopeTextWide>
              {isEditing ? (
                <Field name={"sastAccess"} validate={maxGroupContextLength}>
                  {({
                    field,
                    form: { values, setFieldValue },
                  }: IFieldProps): JSX.Element => {
                    function handleMDChange(value: string | undefined): void {
                      setFieldValue("sastAccess", value);
                    }

                    return (
                      <React.Fragment>
                        <MDEditor
                          height={200}
                          highlightEnable={false}
                          onChange={handleMDChange}
                          value={values.sastAccess}
                        />
                        <ValidationError>
                          <ErrorMessage name={field.name} />
                        </ValidationError>
                        <Alert>
                          {"*"}&nbsp;
                          {t(
                            "searchFindings.groupAccessInfoSection.markdownAlert"
                          )}
                        </Alert>
                      </React.Fragment>
                    );
                  }}
                </Field>
              ) : (
                <MDEditor.Markdown source={dataset.sastAccess} />
              )}
            </GroupScopeTextWide>
          ) : (
            <GroupScopeTextWide>
              {t("searchFindings.groupAccessInfoSection.noGroupContext")}
            </GroupScopeTextWide>
          )}
          <Col25>
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
          </Col25>
        </Row>
      </Form>
    </React.StrictMode>
  );
};

export { GroupContextForm, IFieldProps };
