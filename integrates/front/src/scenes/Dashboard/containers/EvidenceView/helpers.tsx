/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloError, FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";

import type { IEvidenceItem } from ".";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleUpdateDescriptionError = (updateError: ApolloError): void => {
  updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred updating finding evidence",
          updateError
        );
    }
  });
};

const handleUpdateEvidenceError = (updateError: ApolloError): void => {
  updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Invalid File Size":
        msgError(translate.t("validations.fileSize", { count: 10 }));
        break;
      case "Exception - Invalid File Type":
        msgError(translate.t("group.events.form.wrongImageType"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred updating finding evidence",
          updateError
        );
    }
  });
};

function setPreffix(name: string): string {
  if (name === "animation") {
    return translate.t("searchFindings.tabEvidence.animationExploit");
  }

  return name === "exploitation"
    ? translate.t("searchFindings.tabEvidence.evidenceExploit")
    : "";
}

const showUrl = (
  showEmpty: boolean,
  evidence: { url: string }
): JSX.Element | string => {
  return showEmpty ? <div /> : `${location.href}/${evidence.url}`;
};

const setAltDescription = (
  preffix: string,
  evidence: IEvidenceItem
): string => {
  return preffix !== "" && evidence.description !== ""
    ? `${preffix}: ${evidence.description}`
    : `${preffix}${evidence.description}`;
};

const updateChangesHelper = async (
  updateEvidence: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  updateDescription: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  file: FileList | undefined,
  key: string,
  description: string,
  findingId: string,
  descriptionChanged: boolean
): Promise<void> => {
  if (file !== undefined) {
    const mtResult = await updateEvidence({
      variables: {
        evidenceId: key.toUpperCase(),
        file: file[0],
        findingId,
      },
    });
    const { success } = (
      mtResult as {
        data: { updateEvidence: { success: boolean } };
      }
    ).data.updateEvidence;

    if (success && descriptionChanged) {
      await updateDescription({
        variables: {
          description,
          evidenceId: key.toUpperCase(),
          findingId,
        },
      });
    }
  } else if (descriptionChanged) {
    await updateDescription({
      variables: {
        description,
        evidenceId: key.toUpperCase(),
        findingId,
      },
    });
  }
};

export {
  handleUpdateDescriptionError,
  handleUpdateEvidenceError,
  setPreffix,
  showUrl,
  setAltDescription,
  updateChangesHelper,
};
