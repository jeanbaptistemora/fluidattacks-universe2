import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IGroupAccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import { ActionButtons } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/ActionButtons";
import { Col40, Flex, GroupScopeText, Row } from "styles/styledComponents";
import { EditableField, FormikTextArea } from "utils/forms/fields";
import { maxLength } from "utils/validations";

const MAX_DISAMBIGUATION_INFO_LENGTH = 2000;

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
            <GroupScopeText>
              <EditableField
                component={FormikTextArea}
                currentValue={dataset.disambiguation}
                id={
                  "searchFindings.groupAccessInfoSection.tooltips.disambiguation.id"
                }
                label={""}
                markdown={true}
                name={"disambiguation"}
                renderAsEditable={isEditing}
                tooltip={t(
                  "searchFindings.groupAccessInfoSection.tooltips.disambiguation"
                )}
                type={"text"}
                validate={maxDisambiguationInfoLength}
              />
            </GroupScopeText>
          ) : (
            <GroupScopeText>
              {t("searchFindings.groupAccessInfoSection.noDisambiguation")}
            </GroupScopeText>
          )}
          <Col40>
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
          </Col40>
        </Row>
      </Form>
    </React.StrictMode>
  );
};

export { DisambiguationForm };
