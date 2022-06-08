import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { ADD_ENVIRONMENT_URL } from "../../queries";
import { Button } from "components/Button";
import { ControlLabel } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddEnvironmentProps {
  groupName: string;
  rootId: string;
  closeFunction: () => void;
}

interface IFormProps {
  cloudName: string | undefined;
  groupName: string;
  url: string;
  type: string;
  rootId: string;
  urlType: string;
}

const AddEnvironment: React.FC<IAddEnvironmentProps> = ({
  groupName,
  rootId,
  closeFunction,
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
  const validations = object().shape({
    url: string()
      .url(t("validations.invalidUrl"))
      .required(t("validations.required")),
    urlType: string()
      .oneOf(["URL", "APK", "CLOUD"])
      .defined(t("validations.invalidUrlType")),
  });
  const [addEnvironmentUrl] = useMutation(ADD_ENVIRONMENT_URL, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.addEnvironment.success"),
        t("group.scope.git.addEnvironment.successTitle")
      );
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
      url,
      urlType,
    }: {
      url: string;
      urlType: string;
    }): Promise<void> => {
      await addEnvironmentUrl({
        variables: { groupName, rootId, url, urlType },
      });
    },
    [addEnvironmentUrl, groupName, rootId]
  );

  return (
    <Formik
      initialValues={formInitialValues}
      name={"addGitEnv"}
      onSubmit={submitForm}
      validationSchema={validations}
    >
      {({ isValid, dirty, isSubmitting }): JSX.Element => {
        return (
          <Form>
            <div className={"mt3"}>
              <ControlLabel>
                {t("group.scope.git.addEnvironment.url")}
              </ControlLabel>
              <Field component={FormikText} name={"url"} type={"text"} />
            </div>
            <div className={"mt3"}>
              <ControlLabel>
                {t("group.scope.git.addEnvironment.type")}
              </ControlLabel>
              <Field component={FormikDropdown} name={"urlType"}>
                <option value={""}>{""}</option>
                <option value={"CLOUD"}>{"Cloud"}</option>
                <option value={"APK"}>{"APK"}</option>
                <option value={"URL"}>{"URL"}</option>
              </Field>
            </div>
            <div className={"mt3"}>
              <Button
                disabled={!dirty || isSubmitting || !isValid}
                id={"add-environment-url-button"}
                type={"submit"}
                variant={"primary"}
              >
                {t("confirmmodal.proceed")}
              </Button>
            </div>
            <Button onClick={closeFunction} variant={"secondary"}>
              {t("confirmmodal.cancel")}
            </Button>
          </Form>
        );
      }}
    </Formik>
  );
};

export { AddEnvironment };
