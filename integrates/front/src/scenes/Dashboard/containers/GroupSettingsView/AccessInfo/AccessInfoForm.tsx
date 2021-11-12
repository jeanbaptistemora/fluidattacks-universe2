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

const MAX_ACCESS_INFO_LENGTH = 10000;

const maxAccessInfoLength: ConfigurableValidator = maxLength(
  MAX_ACCESS_INFO_LENGTH
);

interface IAccessInfoForm {
  data: IGroupAccessInfo | undefined;
  isEditing: boolean;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

/* eslint-disable react/no-unused-prop-types */
interface IFieldProps {
  field: FieldInputProps<string>;
  form: {
    values: {
      dastAccess: string;
      disambiguation: string;
      mobileAccess: string;
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

const AccessInfoForm: React.FC<IAccessInfoForm> = ({
  data,
  isEditing,
  setEditing,
}: IAccessInfoForm): JSX.Element => {
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
  const hasAccessInfo =
    dataset.dastAccess || dataset.mobileAccess || dataset.sastAccess;

  return (
    <React.StrictMode>
      <Form id={"editGroupAccessInfo"}>
        <Flex>
          <h2>{t("searchFindings.groupAccessInfoSection.groupContext")}</h2>
        </Flex>
        <Row>
          {hasAccessInfo || isEditing ? (
            <GroupScopeTextWide>
              {dataset.sastAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.sast")}</h3>
                  </Flex>
                  {isEditing ? (
                    <Field name={"sastAccess"} validate={maxAccessInfoLength}>
                      {({
                        field,
                        form: { values, setFieldValue },
                      }: IFieldProps): JSX.Element => {
                        function handleMDChange(
                          value: string | undefined
                        ): void {
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
                </React.Fragment>
              ) : undefined}
              {dataset.dastAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.dast")}</h3>
                  </Flex>
                  {isEditing ? (
                    <Field name={"dastAccess"} validate={maxAccessInfoLength}>
                      {({
                        field,
                        form: { values, setFieldValue },
                      }: IFieldProps): JSX.Element => {
                        function handleMDChange(
                          value: string | undefined
                        ): void {
                          setFieldValue("dastAccess", value);
                        }

                        return (
                          <React.Fragment>
                            <MDEditor
                              height={200}
                              highlightEnable={false}
                              onChange={handleMDChange}
                              value={values.dastAccess}
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
                    <MDEditor.Markdown source={dataset.dastAccess} />
                  )}
                </React.Fragment>
              ) : undefined}
              {dataset.mobileAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.mobile")}</h3>
                  </Flex>
                  {isEditing ? (
                    <Field name={"mobileAccess"} validate={maxAccessInfoLength}>
                      {({
                        field,
                        form: { values, setFieldValue },
                      }: IFieldProps): JSX.Element => {
                        function handleMDChange(
                          value: string | undefined
                        ): void {
                          setFieldValue("mobileAccess", value);
                        }

                        return (
                          <React.Fragment>
                            <MDEditor
                              height={200}
                              highlightEnable={false}
                              onChange={handleMDChange}
                              value={values.mobileAccess}
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
                    <MDEditor.Markdown source={dataset.mobileAccess} />
                  )}
                </React.Fragment>
              ) : undefined}
            </GroupScopeTextWide>
          ) : (
            <GroupScopeTextWide>
              {t("searchFindings.groupAccessInfoSection.noAccessInfo")}
            </GroupScopeTextWide>
          )}
          <Col25>
            <ActionButtons
              editTooltip={t(
                "searchFindings.groupAccessInfoSection.tooltips.editGroupAccessInfo"
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

export { AccessInfoForm, IFieldProps };
