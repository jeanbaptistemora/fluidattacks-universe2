import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import type { IGroupAccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";
import { ActionButtons } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/ActionButtons";
import { Col40, Flex, GroupScopeText, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { EditableField, FormikTextArea } from "utils/forms/fields";
import { maxLength } from "utils/validations";

const MAX_ACCESS_INFO_LENGTH = 2000;

const maxAccessInfoLength: ConfigurableValidator = maxLength(
  MAX_ACCESS_INFO_LENGTH
);

interface IDescriptionViewFormProps {
  data: IGroupAccessInfo | undefined;
  isEditing: boolean;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const AccessInfoForm: React.FC<IDescriptionViewFormProps> = ({
  data,
  isEditing,
  setEditing,
}: IDescriptionViewFormProps): JSX.Element => {
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
          <h2>{t("searchFindings.groupAccessInfoSection.accessInfo")}</h2>
        </Flex>
        <Row>
          {hasAccessInfo || isEditing ? (
            <GroupScopeText>
              {dataset.sastAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.sast")}</h3>
                  </Flex>
                  <Can
                    do={"api_mutations_update_group_access_info_mutate"}
                    passThrough={true}
                  >
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={FormikTextArea}
                        currentValue={dataset.sastAccess}
                        id={
                          "searchFindings.groupAccessInfoSection.tooltips.sast.id"
                        }
                        label={""}
                        markdown={true}
                        name={"sastAccess"}
                        renderAsEditable={isEditing}
                        tooltip={t(
                          "searchFindings.groupAccessInfoSection.tooltips.sast"
                        )}
                        type={"text"}
                        validate={maxAccessInfoLength}
                        visibleWhileEditing={canEdit}
                      />
                    )}
                  </Can>
                </React.Fragment>
              ) : undefined}
              {dataset.dastAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.dast")}</h3>
                  </Flex>
                  <Can
                    do={"api_mutations_update_group_access_info_mutate"}
                    passThrough={true}
                  >
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={FormikTextArea}
                        currentValue={dataset.dastAccess}
                        id={
                          "searchFindings.groupAccessInfoSection.tooltips.dast.id"
                        }
                        label={""}
                        markdown={true}
                        name={"dastAccess"}
                        renderAsEditable={isEditing}
                        tooltip={t(
                          "searchFindings.groupAccessInfoSection.tooltips.dast"
                        )}
                        type={"text"}
                        validate={maxAccessInfoLength}
                        visibleWhileEditing={canEdit}
                      />
                    )}
                  </Can>
                </React.Fragment>
              ) : undefined}
              {dataset.mobileAccess || isEditing ? (
                <React.Fragment>
                  <Flex>
                    <h3>{t("searchFindings.groupAccessInfoSection.mobile")}</h3>
                  </Flex>
                  <Can
                    do={"api_mutations_update_group_access_info_mutate"}
                    passThrough={true}
                  >
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={FormikTextArea}
                        currentValue={dataset.mobileAccess}
                        id={
                          "searchFindings.groupAccessInfoSection.tooltips.mobile.id"
                        }
                        label={""}
                        markdown={true}
                        name={"mobileAccess"}
                        renderAsEditable={isEditing}
                        tooltip={t(
                          "searchFindings.groupAccessInfoSection.tooltips.mobile"
                        )}
                        type={"text"}
                        validate={maxAccessInfoLength}
                        visibleWhileEditing={canEdit}
                      />
                    )}
                  </Can>
                </React.Fragment>
              ) : undefined}
            </GroupScopeText>
          ) : (
            <GroupScopeText>
              {t("searchFindings.groupAccessInfoSection.noAccessInfo")}
            </GroupScopeText>
          )}
          <Col40>
            <ActionButtons
              isEditing={isEditing}
              isPristine={isGroupAccessInfoPristine}
              onEdit={toggleEdit}
              onUpdate={handleSubmit}
            />
          </Col40>
        </Row>
        <Flex>
          <h2>{t("searchFindings.groupAccessInfoSection.disambiguation")}</h2>
        </Flex>
        <Row>
          {dataset.disambiguation || isEditing ? (
            <GroupScopeText>
              <Can
                do={"api_mutations_update_group_access_info_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
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
                    validate={maxAccessInfoLength}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </GroupScopeText>
          ) : (
            <GroupScopeText>
              {t("searchFindings.groupAccessInfoSection.noDisambiguation")}
            </GroupScopeText>
          )}
        </Row>
      </Form>
    </React.StrictMode>
  );
};

export { AccessInfoForm };
