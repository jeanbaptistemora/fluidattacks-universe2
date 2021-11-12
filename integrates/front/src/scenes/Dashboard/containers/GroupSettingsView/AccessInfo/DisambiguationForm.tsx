import MDEditor from "@uiw/react-md-editor";
import { ErrorMessage, Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IGroupAccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import type { IFieldProps } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/AccessInfoForm";
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
        <Flex>
          <h2>{t("searchFindings.groupAccessInfoSection.disambiguation")}</h2>
        </Flex>
        <Row>
          {dataset.disambiguation || isEditing ? (
            <GroupScopeTextWide>
              {isEditing ? (
                <Field
                  name={"disambiguation"}
                  validate={maxDisambiguationInfoLength}
                >
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
                          {t(
                            "searchFindings.groupAccessInfoSection.markdownAlert"
                          )}
                        </Alert>
                      </React.Fragment>
                    );
                  }}
                </Field>
              ) : (
                <MDEditor.Markdown source={dataset.disambiguation} />
              )}
            </GroupScopeTextWide>
          ) : (
            <GroupScopeTextWide>
              {t("searchFindings.groupAccessInfoSection.noDisambiguation")}
            </GroupScopeTextWide>
          )}
          <Col25>
            <ActionButtons
              editTooltip={t(
                "searchFindings.groupAccessInfoSection.tooltips.editDisambiguationInfo"
              )}
              isEditing={isEditing}
              isPristine={isDisambiguationInfoPristine}
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

export { DisambiguationForm };
