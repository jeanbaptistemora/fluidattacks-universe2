import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { FormikHelpers } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { errorMessageHelper } from "./helpers";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  DOWNLOAD_VULNERABILITIES,
  UPLOAD_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import type {
  IDownloadVulnerabilitiesResultAttr,
  IUploadVulnerabilitiesResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_LOCATIONS } from "scenes/Dashboard/containers/GroupFindingsView/loaders/Locations/queries";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import {
  ButtonToolbarLeft,
  Col33,
  FormGroup,
  RowCenter,
} from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikFileInput } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { composeValidators, isValidVulnsFile } from "utils/validations";

interface IUploadVulnProps {
  findingId: string;
  refetchData: () => void;
}

interface IErrorInfoAttr {
  keys: string[];
  msg: string;
  values: string[] & string;
}

const UploadVulnerabilities: React.FC<IUploadVulnProps> = ({
  findingId,
  refetchData,
}: IUploadVulnProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  function handleUploadError(updateError: ApolloError): void {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message.includes("Exception - Error in range limit numbers")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgError(`${t("groupAlerts.rangeError")} ${errorObject.values}`);
      } else if (
        message.startsWith(
          "Exception - Uploaded vulnerability is a confirmed Zero Risk"
        )
      ) {
        msgError(
          t("groupAlerts.zeroRiskAlreadyUploaded", {
            info: message.split("Zero Risk:")[1],
          })
        );
      } else if (
        message.startsWith(
          "Exception -  The line does not exist in the range of 0 and lines of code"
        )
      ) {
        msgError(
          t("searchFindings.tabVuln.alerts.uploadFile.lineDoesNotExistInLoc", {
            line: message.split("code: ")[1],
          })
        );
      } else if (message.includes("Exception - Invalid Schema")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
          const listValuesFormated: string[] = Array.from(
            new Set(
              errorObject.values.map((valX: string): string =>
                t("searchFindings.tabVuln.alerts.uploadFile.value", {
                  pattern: valX,
                })
              )
            )
          );
          const listKeysFormated: string[] = Array.from(
            new Set(
              errorObject.keys.map((valY: string): string =>
                t("searchFindings.tabVuln.alerts.uploadFile.key", {
                  key: valY,
                })
              )
            )
          );
          msgErrorStick(
            listKeysFormated.join("") + listValuesFormated.join(""),
            t("groupAlerts.invalidSchema")
          );
        } else {
          msgError(t("groupAlerts.invalidSchema"));
        }
      } else {
        switch (message) {
          case "Exception - The vulnerability path does not exist in the toe lines":
            msgError(
              t(
                "searchFindings.tabVuln.alerts.uploadFile.linesPathDoesNotExist"
              )
            );
            break;
          case "Exception -  The vulnerability URL and field do not exist in the toe inputs":
            msgError(
              t(
                "searchFindings.tabVuln.alerts.uploadFile.inputUrlAndFieldDoNotExist"
              )
            );
            break;
          default:
            errorMessageHelper(message);
        }
      }
    });
  }

  const [uploadVulnerability, { loading }] =
    useMutation<IUploadVulnerabilitiesResultAttr>(UPLOAD_VULNERABILITIES, {
      onCompleted: (result: IUploadVulnerabilitiesResultAttr): void => {
        if (!_.isUndefined(result)) {
          if (result.uploadFile.success) {
            msgSuccess(
              t("groupAlerts.fileUpdated"),
              t("groupAlerts.titleSuccess")
            );
            refetchData();
          }
        }
      },
      onError: handleUploadError,
      refetchQueries: [
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState: permissions.can(
              "api_resolvers_finding_historic_state_resolve"
            ),
            findingId,
          },
        },
        {
          query: GET_FINDING_LOCATIONS,
          variables: {
            findingId,
          },
        },
      ],
    });
  const [downloadVulnerability] =
    useMutation<IDownloadVulnerabilitiesResultAttr>(DOWNLOAD_VULNERABILITIES, {
      onCompleted: (result: IDownloadVulnerabilitiesResultAttr): void => {
        if (!_.isUndefined(result)) {
          if (
            result.downloadVulnerabilityFile.success &&
            result.downloadVulnerabilityFile.url !== ""
          ) {
            openUrl(result.downloadVulnerabilityFile.url);
          }
        }
      },
      onError: (downloadError: ApolloError): void => {
        downloadError.graphQLErrors.forEach(
          ({ message }: GraphQLError): void => {
            msgError(t("groupAlerts.errorTextsad"));
            if (message === "Exception - Error Uploading File to S3") {
              Logger.warning(
                "An error occurred downloading vuln file while uploading file to S3",
                downloadError
              );
            } else {
              Logger.warning(
                "An error occurred downloading vuln file",
                downloadError
              );
            }
          }
        );
      },
    });

  interface IUploadVulnFile {
    filename: FileList;
  }

  async function handleUploadVulnerability(
    values: IUploadVulnFile,
    formikHelpers: FormikHelpers<IUploadVulnFile>
  ): Promise<void> {
    await uploadVulnerability({
      variables: {
        file: values.filename[0],
        findingId,
      },
    });
    formikHelpers.resetForm();
  }

  function handleDownloadVulnerability(): void {
    void downloadVulnerability({
      variables: {
        findingId,
      },
    });
  }

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ filename: undefined as unknown as FileList }}
      name={"uploadVulns"}
      onSubmit={handleUploadVulnerability}
    >
      {({ dirty }): React.ReactNode => (
        <Form>
          <br />
          <RowCenter>
            <Col33>
              <ButtonToolbarLeft>
                <TooltipWrapper
                  id={t(
                    "searchFindings.tabDescription.downloadVulnerabilitiesTooltip.id"
                  )}
                  message={t(
                    "searchFindings.tabDescription.downloadVulnerabilitiesTooltip"
                  )}
                >
                  <Button
                    disabled={loading}
                    onClick={handleDownloadVulnerability}
                    variant={"secondary"}
                  >
                    <FluidIcon icon={"export"} />
                    &nbsp;
                    {t("searchFindings.tabDescription.downloadVulnerabilities")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarLeft>
            </Col33>
            <div className={"ph1-5 w-25-ns upload-file"}>
              <FormGroup>
                <Field
                  accept={".yaml, .yml"}
                  component={FormikFileInput}
                  id={"filename"}
                  name={"filename"}
                  validate={composeValidators([isValidVulnsFile])}
                />
              </FormGroup>
            </div>
            <Col33>
              <ButtonToolbarLeft>
                <TooltipWrapper
                  id={t(
                    "searchFindings.tabDescription.updateVulnerabilitiesTooltip.id"
                  )}
                  message={t(
                    "searchFindings.tabDescription.updateVulnerabilitiesTooltip"
                  )}
                >
                  <Button
                    disabled={!dirty || loading}
                    type={"submit"}
                    variant={"primary"}
                  >
                    <FluidIcon icon={"import"} />
                    &nbsp;
                    {t("searchFindings.tabDescription.updateVulnerabilities")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarLeft>
            </Col33>
          </RowCenter>
        </Form>
      )}
    </Formik>
  );
};

export type { IErrorInfoAttr };
export { UploadVulnerabilities };
