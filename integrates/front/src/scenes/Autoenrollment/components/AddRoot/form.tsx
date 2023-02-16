import { Form } from "formik";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Input, InputArray, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import type { IRootAttr } from "scenes/Autoenrollment/types";

interface IAddRootFormProps {
  isSubmitting: boolean;
  rootMessages: {
    message: string;
    type: string;
  };
  setFieldValue: (
    field: string,
    value: boolean | string,
    shouldValidate?: boolean | undefined
  ) => void;
  setShowSubmitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  showSubmitAlert: boolean;
  values: IRootAttr;
}

export const AddRootForm: React.FC<IAddRootFormProps> = ({
  isSubmitting,
  rootMessages,
  setFieldValue,
  setShowSubmitAlert,
  showSubmitAlert,
  values,
}: IAddRootFormProps): JSX.Element => {
  const { t } = useTranslation();

  const onTypeChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.preventDefault();
      if (event.target.value === "SSH") {
        setFieldValue("credentials.type", "SSH");
        setFieldValue("credentials.auth", "");
        setFieldValue("credentials.isPat", false);
      }
      if (event.target.value === "USER") {
        setFieldValue("credentials.type", "HTTPS");
        setFieldValue("credentials.auth", "USER");
        setFieldValue("credentials.isPat", false);
      }
      if (event.target.value === "TOKEN") {
        setFieldValue("credentials.type", "HTTPS");
        setFieldValue("credentials.auth", "TOKEN");
        setFieldValue("credentials.isPat", true);
      }
    },
    [setFieldValue]
  );

  return (
    <Form>
      <Row justify={"start"}>
        <Col lg={50} md={50} sm={100}>
          <Input
            label={t("autoenrollment.url.label")}
            name={"url"}
            placeholder={t("autoenrollment.url.placeholder")}
            tooltip={t("autoenrollment.url.tooltip")}
            type={"text"}
          />
        </Col>
        <Col lg={50} md={50} sm={100}>
          <Input
            label={t("autoenrollment.branch.label")}
            name={"branch"}
            placeholder={t("autoenrollment.branch.placeholder")}
            type={"text"}
          />
        </Col>
        <Col lg={50} md={50} sm={100}>
          <Select
            label={t("autoenrollment.credentials.type.label")}
            name={"credentials.typeCredential"}
            onChange={onTypeChange}
          >
            <option value={""}>{""}</option>
            <option value={"SSH"}>
              {t("autoenrollment.credentials.type.ssh")}
            </option>
            <option value={"USER"}>
              {t("autoenrollment.credentials.auth.user")}
            </option>
            <option value={"TOKEN"}>
              {t("autoenrollment.credentials.auth.azureToken")}
            </option>
          </Select>
        </Col>
        <Col lg={50} md={50} sm={100}>
          <Input
            disabled={values.credentials.type === ""}
            label={t("autoenrollment.credentials.name.label")}
            name={"credentials.name"}
            placeholder={t("autoenrollment.credentials.name.placeholder")}
          />
        </Col>
        {values.credentials.type === "SSH" && (
          <Col lg={100} md={100} sm={100}>
            <TextArea
              label={t("group.scope.git.repo.credentials.sshKey")}
              name={"credentials.key"}
              placeholder={t("group.scope.git.repo.credentials.sshHint")}
            />
          </Col>
        )}
        {values.credentials.type === "HTTPS" &&
          values.credentials.auth === "TOKEN" && (
            <React.Fragment>
              <Col lg={100} md={100} sm={100}>
                <Input
                  label={t("autoenrollment.credentials.token")}
                  name={"credentials.token"}
                />
              </Col>
              <Col lg={100} md={100} sm={100}>
                {values.credentials.isPat === true ? (
                  <Input
                    label={t(
                      "autoenrollment.credentials.azureOrganization.text"
                    )}
                    name={"credentials.azureOrganization"}
                    tooltip={t(
                      "autoenrollment.credentials.azureOrganization.tooltip"
                    )}
                  />
                ) : undefined}
              </Col>
            </React.Fragment>
          )}
        {values.credentials.type === "HTTPS" &&
          values.credentials.auth === "USER" && (
            <Fragment>
              <Col lg={50} md={50} sm={100}>
                <Input
                  label={t("autoenrollment.credentials.user")}
                  name={"credentials.user"}
                />
              </Col>
              <Col lg={50} md={50} sm={100}>
                <Input
                  label={t("autoenrollment.credentials.password")}
                  name={"credentials.password"}
                  type={"password"}
                />
              </Col>
            </Fragment>
          )}
        <Col lg={100} md={100} sm={100}>
          <Input
            id={"env"}
            label={t("autoenrollment.environment.label")}
            name={"env"}
            placeholder={t("autoenrollment.environment.placeholder")}
            tooltip={t("Description of the application environment")}
          />
        </Col>
        <Col lg={100} md={100} sm={100}>
          <InputArray
            id={"exclusions"}
            initValue={""}
            label={t("autoenrollment.exclusions.label")}
            max={5}
            name={"exclusions"}
            placeholder={t("autoenrollment.exclusions.placeholder")}
            tooltip={t("autoenrollment.exclusions.tooltip")}
          />
        </Col>
        {!showSubmitAlert && rootMessages.message !== "" && (
          <Alert
            onTimeOut={setShowSubmitAlert}
            variant={rootMessages.type as IAlertProps["variant"]}
          >
            {rootMessages.message}
          </Alert>
        )}
      </Row>
      <div className={"flex justify-start mt3"}>
        <Button disabled={isSubmitting} type={"submit"} variant={"primary"}>
          {t("autoenrollment.next")}
        </Button>
      </div>
    </Form>
  );
};
