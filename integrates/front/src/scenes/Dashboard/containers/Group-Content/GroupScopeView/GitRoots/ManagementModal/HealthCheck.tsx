import { Field } from "formik";
import type { Dispatch, FC, SetStateAction } from "react";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../../types";
import { Alert } from "components/Alert";
import { Checkbox, Label } from "components/Input";
import { Hr, Row } from "components/Layout";
import { Text } from "components/Text";
import { Have } from "utils/authz/Have";
import { FormikRadioGroup } from "utils/forms/fields";

interface IHealthCheckProps {
  initValues: IFormValues;
  isEditing: boolean;
  isHealthChecked: boolean;
  setHasSquad: Dispatch<SetStateAction<boolean>>;
  setIsHealthChecked: Dispatch<SetStateAction<boolean>>;
  values: IFormValues;
}

const HealthCheck: FC<IHealthCheckProps> = ({
  initValues,
  isEditing,
  setHasSquad,
  setIsHealthChecked,
  values,
}: Readonly<IHealthCheckProps>): JSX.Element => {
  const { t } = useTranslation();

  const [confirmHealthCheck, setConfirmHealthCheck] = useState(
    isEditing && (initValues.includesHealthCheck ?? false)
  );

  const [isRootChange, setIsRootChange] = useState(
    [initValues.url, initValues.branch].join("")
  );

  const setSquad = useCallback((): void => {
    setHasSquad(true);
  }, [setHasSquad]);

  if ([values.url, values.branch].join("") !== isRootChange) {
    setIsRootChange([values.url, values.branch].join(""));
    if (
      [values.url, values.branch].join("") !==
      [initValues.url, initValues.branch].join("")
    ) {
      setIsHealthChecked(false);
    }
  }

  return (
    <Have I={"has_squad"}>
      <Hr mv={16} />
      <Text fw={7} mb={2} size={"medium"}>
        {t("group.scope.git.healthCheck.title")}
      </Text>
      <fieldset className={"bn"}>
        <Row id={"git-root-add-health-check"} onMouseMove={setSquad}>
          <div>
            <Label>{t("group.scope.git.healthCheck.confirm")}</Label>
            <Field
              component={FormikRadioGroup}
              initialState={
                isEditing ? (confirmHealthCheck ? "Yes" : "No") : null
              }
              labels={["Yes", "No"]}
              name={"includesHealthCheck"}
              onSelect={setConfirmHealthCheck}
              type={"Radio"}
              uncheck={setIsHealthChecked}
            />
          </div>
          {values.includesHealthCheck ?? false ? (
            <Alert>
              <Checkbox
                label={t("group.scope.git.healthCheck.accept")}
                name={"healthCheckConfirm"}
                required={true}
                value={"includeA"}
              />
            </Alert>
          ) : undefined}
          {values.includesHealthCheck ?? true ? undefined : (
            <Alert>
              <div>
                <Checkbox
                  label={t("group.scope.git.healthCheck.rejectA")}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectA"}
                />
                <Checkbox
                  label={t("group.scope.git.healthCheck.rejectB")}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectB"}
                />
                <Checkbox
                  label={t("group.scope.git.healthCheck.rejectC")}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectC"}
                />
              </div>
            </Alert>
          )}
        </Row>
      </fieldset>
    </Have>
  );
};

export type { IHealthCheckProps };
export { HealthCheck };
