/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { Fragment, useState } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Input, InputArray, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import {
  handleValidationError,
  rootSchema,
} from "scenes/Autoenrollment/helpers";
import { VALIDATE_GIT_ACCESS } from "scenes/Autoenrollment/queries";
import type {
  ICheckGitAccessResult,
  IRootAttr,
} from "scenes/Autoenrollment/types";

interface IAddRootProps {
  initialValues: IRootAttr;
  onCompleted: () => void;
  rootMessages: {
    message: string;
    type: string;
  };
  setRepositoryValues: React.Dispatch<React.SetStateAction<IRootAttr>>;
  setRootMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
}

const AddRoot: React.FC<IAddRootProps> = ({
  initialValues,
  onCompleted,
  rootMessages,
  setRepositoryValues,
  setRootMessages,
}: IAddRootProps): JSX.Element => {
  const { t } = useTranslation();

  const [isDirty, setIsDirty] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [validateGitAccess] =
    useMutation<ICheckGitAccessResult>(VALIDATE_GIT_ACCESS);

  async function validateAndSubmit(values: IRootAttr): Promise<void> {
    try {
      await validateGitAccess({
        variables: {
          branch: values.branch,
          credentials: {
            key: values.credentials.key
              ? Buffer.from(values.credentials.key).toString("base64")
              : undefined,
            name: values.credentials.name,
            password: values.credentials.password,
            token: values.credentials.token,
            type: values.credentials.type,
            user: values.credentials.user,
          },
          url: values.url,
        },
      });
      setShowSubmitAlert(false);
      setRepositoryValues(values);
      setRootMessages({
        message: t("group.scope.git.repo.credentials.checkAccess.success"),
        type: "success",
      });
      onCompleted();
    } catch (error) {
      setShowSubmitAlert(false);
      const { graphQLErrors } = error as ApolloError;
      handleValidationError(graphQLErrors, setRootMessages);
    }
  }

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={initialValues}
        name={"newRoot"}
        onSubmit={validateAndSubmit}
        validationSchema={rootSchema(isDirty)}
      >
        {({ dirty, isSubmitting, values }): JSX.Element => {
          setIsDirty(dirty);

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
                    name={"credentials.type"}
                  >
                    <option value={""}>{""}</option>
                    <option value={"HTTPS"}>
                      {t("autoenrollment.credentials.type.https")}
                    </option>
                    <option value={"SSH"}>
                      {t("autoenrollment.credentials.type.ssh")}
                    </option>
                  </Select>
                </Col>
                <Col lg={50} md={50} sm={100}>
                  <Input
                    disabled={values.credentials.type === ""}
                    label={t("autoenrollment.credentials.name.label")}
                    name={"credentials.name"}
                    placeholder={t(
                      "autoenrollment.credentials.name.placeholder"
                    )}
                  />
                </Col>
                {values.credentials.type === "SSH" && (
                  <Col lg={100} md={100} sm={100}>
                    <TextArea
                      label={t("group.scope.git.repo.credentials.sshKey")}
                      name={"credentials.key"}
                      placeholder={t(
                        "group.scope.git.repo.credentials.sshHint"
                      )}
                    />
                  </Col>
                )}
                {values.credentials.type === "HTTPS" && (
                  <Col lg={100} md={100} sm={100}>
                    <Select name={"credentials.auth"}>
                      <option value={"TOKEN"}>
                        {t("autoenrollment.credentials.auth.token")}
                      </option>
                      <option value={"USER"}>
                        {t("autoenrollment.credentials.auth.user")}
                      </option>
                    </Select>
                  </Col>
                )}
                {values.credentials.type === "HTTPS" &&
                  values.credentials.auth === "TOKEN" && (
                    <Col lg={100} md={100} sm={100}>
                      <Input
                        label={t("autoenrollment.credentials.token")}
                        name={"credentials.token"}
                      />
                    </Col>
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
                <Button
                  disabled={isSubmitting}
                  type={"submit"}
                  variant={"primary"}
                >
                  {t("autoenrollment.next")}
                </Button>
              </div>
            </Form>
          );
        }}
      </Formik>
    </div>
  );
};

export { AddRoot };
