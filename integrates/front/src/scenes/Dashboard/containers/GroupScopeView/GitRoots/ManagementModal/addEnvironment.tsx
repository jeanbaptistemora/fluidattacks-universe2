import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { FormikProps } from "formik";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, useCallback, useRef } from "react";
import { useTranslation } from "react-i18next";
import type { StringSchema } from "yup";
import { object, string } from "yup";

import { ADD_ENVIRONMENT_URL } from "../../queries";
import { Input, Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { GET_FILES } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type {
  IGetFilesQuery,
  IGroupFileAttr,
} from "scenes/Dashboard/containers/GroupSettingsView/types";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddEnvironmentProps {
  groupName: string;
  rootId: string;
  closeFunction: () => void;
  onSubmit: () => void;
  onUpdate: () => void;
}

interface IFormProps {
  cloudName: string | undefined;
  groupName: string;
  url: string;
  type: string;
  rootId: string;
  urlType: string;
}
interface IFile {
  description: string;
  fileName: string;
  uploadDate: string;
}

const AddEnvironment: FC<IAddEnvironmentProps> = ({
  groupName,
  rootId,
  closeFunction,
  onSubmit,
  onUpdate,
}: IAddEnvironmentProps): JSX.Element => {
  const { t } = useTranslation();
  const formInitialValues: IFormProps = {
    cloudName: undefined,
    groupName,
    rootId,
    type: "",
    url: "",
    urlType: "",
  };
  const formRef = useRef<FormikProps<IFormProps>>(null);
  const validations = object().shape({
    cloudName: string().oneOf(["AZURE", "AWS", "GCP"]).nullable(),
    url: string()
      .when("urlType", {
        is: "URL",
        then: (schema): StringSchema => schema.url(t("validations.invalidUrl")),
      })
      .when("cloudName", {
        is: "AWS",
        then: string().matches(/^\d{12}$/u),
      })
      .required(t("validations.required")),
    urlType: string()
      .oneOf(["URL", "APK", "CLOUD"])
      .defined(t("validations.invalidUrlType")),
  });

  const { data } = useQuery<IGetFilesQuery>(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group files", error);
      });
    },
    variables: { groupName },
  });
  const resourcesFiles: IGroupFileAttr[] =
    _.isUndefined(data) || _.isEmpty(data) || _.isNull(data.resources.files)
      ? []
      : data.resources.files;
  const filesDataset: IFile[] = resourcesFiles as IFile[];
  const [addEnvironmentUrl] = useMutation(ADD_ENVIRONMENT_URL, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.addEnvironment.success"),
        t("group.scope.git.addEnvironment.successTittle")
      );
      onSubmit();
      onUpdate();
      closeFunction();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't add environment url", error);
      });
    },
  });
  const submitForm = useCallback(
    async ({
      cloudName,
      url,
      urlType,
    }: {
      cloudName: string | undefined;
      url: string;
      urlType: string;
    }): Promise<void> => {
      await addEnvironmentUrl({
        variables: { cloudName, groupName, rootId, url, urlType },
      });
    },
    [addEnvironmentUrl, groupName, rootId]
  );

  return (
    <Formik
      initialValues={formInitialValues}
      innerRef={formRef}
      name={"addGitEnv"}
      onSubmit={submitForm}
      validationSchema={validations}
    >
      {({ isValid, dirty, isSubmitting }): JSX.Element => {
        return (
          <Form>
            <Row>
              <Col>
                <Select
                  label={
                    <Fragment>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.addEnvironment.type")}
                    </Fragment>
                  }
                  name={"urlType"}
                >
                  <option value={""}>{""}</option>
                  <option value={"CLOUD"}>{"Cloud"}</option>
                  <option value={"APK"}>{"APK"}</option>
                  <option value={"URL"}>{"URL"}</option>
                </Select>
              </Col>
              {formRef.current !== null &&
              formRef.current.values.urlType === "CLOUD" ? (
                <Col>
                  <Select
                    label={
                      <Fragment>
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                        {"Cloud Name"}
                      </Fragment>
                    }
                    name={"cloudName"}
                  >
                    <option value={""}>{""}</option>
                    <option value={"AWS"}>{"AWS"}</option>
                    <option value={"GCP"}>{"Google Cloud Platform"}</option>
                    <option value={"AZURE"}>{"Azure"}</option>
                  </Select>
                </Col>
              ) : undefined}
            </Row>
            <div className={"mt3"}>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {formRef.current === null
                  ? t("group.scope.git.addEnvironment.url")
                  : formRef.current.values.urlType === "CLOUD" &&
                    formRef.current.values.cloudName === "AWS"
                  ? t("group.scope.git.addEnvironment.aws")
                  : formRef.current.values.urlType === "APK"
                  ? t("group.scope.git.addEnvironment.apk")
                  : t("group.scope.git.addEnvironment.url")}
              </ControlLabel>
              {formRef.current !== null &&
              formRef.current.values.urlType === "APK" ? (
                <Select name={"url"}>
                  <option value={""}>{""}</option>
                  {filesDataset.map(
                    (file): JSX.Element => (
                      <option key={file.fileName} value={file.fileName}>
                        {file.fileName}
                      </option>
                    )
                  )}
                </Select>
              ) : (
                <Input name={"url"} />
              )}
            </div>
            <ModalConfirm
              disabled={!dirty || isSubmitting || !isValid}
              id={"add-env-url-confirm"}
              onCancel={closeFunction}
            />
          </Form>
        );
      }}
    </Formik>
  );
};

export { AddEnvironment };
