/* eslint-disable complexity */
import type { FormikErrors } from "formik";
import type { FC } from "react";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";
import type { Step } from "react-joyride";

import type { IFormValues } from "../../types";
import {
  getRepositoryTourStepsText,
  shouldHideRepositoryTourFooter,
} from "../helpers";
import { BaseStep, Tour } from "components/Tour";

interface IRepositoryTourProps {
  errors: FormikErrors<IFormValues>;
  finishTour: () => void;
  dirty: boolean;
  isGitAccessible: boolean;
  runTour: boolean;
  values: IFormValues;
}

const RepositoryTour: FC<IRepositoryTourProps> = ({
  errors,
  finishTour,
  dirty,
  isGitAccessible,
  runTour,
  values,
}: Readonly<IRepositoryTourProps>): JSX.Element => {
  const { t } = useTranslation();

  const steps: Step[] = [
    {
      ...BaseStep,
      content: t("tours.addGitRoot.intro"),
      placement: "center",
      target: "#git-root-add-use-vpn",
      title: t("group.scope.common.add"),
    },
    {
      ...BaseStep,
      content: t("tours.addGitRoot.rootUrl"),
      hideBackButton: true,
      hideFooter: values.url.length === 0,
      target: "#git-root-add-repo-url",
    },
    {
      ...BaseStep,
      content: t("tours.addGitRoot.rootBranch"),
      hideFooter: values.branch.length === 0,
      target: "#git-root-add-repo-branch",
    },
    {
      ...BaseStep,
      content: t("tours.addGitRoot.vpn"),
      target: "#git-root-add-use-vpn",
    },
    {
      ...BaseStep,
      content: t("tours.addGitRoot.nickname"),
      hideFooter: values.nickname.length === 0,
      target: "#git-root-add-nickname",
    },
    {
      ...BaseStep,
      content: (
        <Fragment>
          {t("tours.addGitRoot.rootCredentials.content")}
          <ul>
            {getRepositoryTourStepsText(values)}
            {values.credentials.name === "" ? (
              <li>{t("tours.addGitRoot.rootCredentials.name")}</li>
            ) : undefined}
            {isGitAccessible ? undefined : (
              <li>{t("tours.addGitRoot.rootCredentials.invalid")}</li>
            )}
          </ul>
        </Fragment>
      ),
      hideFooter: shouldHideRepositoryTourFooter(values),
      placement: "left",
      target: "#git-root-add-credentials",
    },
    {
      ...BaseStep,
      content: t("tours.addGitRoot.rootEnvironment"),
      hideFooter: values.environment.length === 0,
      target: "#git-root-add-env",
    },
    {
      ...BaseStep,
      content: (
        <Fragment>
          {t("tours.addGitRoot.rootHasHealthCheck")}
          {values.includesHealthCheck !== null &&
          errors.healthCheckConfirm !== undefined ? (
            <ul>
              <li>{t("tours.addGitRoot.healthCheckConditions")}</li>
            </ul>
          ) : undefined}
        </Fragment>
      ),
      hideFooter:
        values.includesHealthCheck === null ||
        errors.healthCheckConfirm !== undefined,
      placement: "left",
      target: "#git-root-add-health-check",
    },
    {
      ...BaseStep,
      content:
        !isGitAccessible || !dirty
          ? t("tours.addGitRoot.proceedButton.invalidForm")
          : t("tours.addGitRoot.proceedButton.validForm"),
      target: "#git-root-add-confirm",
    },
  ];

  return <Tour onFinish={finishTour} run={runTour} steps={steps} />;
};

export type { IRepositoryTourProps };
export { RepositoryTour };
