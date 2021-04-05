/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import { useMutation } from "@apollo/react-hooks";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useDispatch } from "react-redux";
import type { Dispatch } from "redux";
import { Field, reset } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  DOWNLOAD_VULNERABILITIES,
  UPLOAD_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import type {
  IDownloadVulnerabilitiesResultAttr,
  IUploadVulnerabilitiesResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import {
  ButtonToolbarLeft,
  Col25,
  Col33,
  FormGroup,
  RowCenter,
} from "styles/styledComponents";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { FileInput } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import { isValidVulnsFile } from "utils/validations";

interface IUploadVulnProps {
  findingId: string;
  groupName: string;
}

export const UploadVulnerabilities: React.FC<IUploadVulnProps> = ({
  findingId,
  groupName,
}: IUploadVulnProps): JSX.Element => {
  const dispatch: Dispatch = useDispatch();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);

  function handleUploadError(updateError: ApolloError): void {
    interface IErrorInfoAttr {
      keys: string[];
      msg: string;
      values: string[] & string;
    }
    function formatError(errorName: string, errorValue: string): string {
      return ` ${translate.t(errorName)} "${errorValue}" ${translate.t(
        "groupAlerts.invalid"
      )}. `;
    }

    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message.includes("Exception - Error in range limit numbers")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgError(
          `${translate.t("groupAlerts.rangeError")} ${errorObject.values}`
        );
      } else if (message.includes("Exception - Invalid Schema")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
          const listValuesFormated: string[] = Array.from(
            new Set(
              errorObject.values.map((valX: string): string =>
                translate.t("searchFindings.tabVuln.alerts.uploadFile.value", {
                  pattern: valX,
                })
              )
            )
          );
          const listKeysFormated: string[] = Array.from(
            new Set(
              errorObject.keys.map((valY: string): string =>
                translate.t("searchFindings.tabVuln.alerts.uploadFile.key", {
                  key: valY,
                })
              )
            )
          );
          msgErrorStick(
            listKeysFormated.join("") + listValuesFormated.join(""),
            translate.t("groupAlerts.invalidSchema")
          );
        } else {
          msgError(translate.t("groupAlerts.invalidSchema"));
        }
      } else if (message === "Exception - Invalid characters") {
        msgError(translate.t("validations.invalidChar"));
      } else if (message === "Exception - Invalid File Size") {
        msgError(translate.t("validations.fileSize", { count: 1 }));
      } else if (message === "Exception - Invalid File Type") {
        msgError(translate.t("groupAlerts.fileTypeYaml"));
      } else if (message.includes("Exception - Error in path value")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgErrorStick(`${translate.t("groupAlerts.pathValue")}
          ${formatError("groupAlerts.value", errorObject.values)}`);
      } else if (message.includes("Exception - Error in port value")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgErrorStick(`${translate.t("groupAlerts.portValue")}
          ${formatError("groupAlerts.value", errorObject.values)}`);
      } else if (message === "Exception - Error in specific value") {
        msgError(translate.t("groupAlerts.invalidSpecific"));
      } else if (
        message ===
        "Exception - You can upload a maximum of 100 vulnerabilities per file"
      ) {
        msgError(translate.t("groupAlerts.invalidNOfVulns"));
      } else if (message === "Exception - Error Uploading File to S3") {
        msgError(translate.t("groupAlerts.errorTextsad"));
      } else if (message === "Exception - Invalid Stream") {
        translate.t("groupAlerts.invalidSchema");
        msgError(
          translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidStream")
        );
      } else if (message === "Exception - Access denied or root not found") {
        msgError(
          translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidRoot")
        );
      } else {
        msgError(translate.t("groupAlerts.invalidSpecific"));
        Logger.warning(message);
      }
      // Clean the files stored on input field
      const formElement: HTMLFormElement = document.querySelector(
        "#vulnerabilities"
      ) as HTMLFormElement;
      formElement.reset();
      dispatch(reset("vulns"));
    });
  }

  const [
    uploadVulnerability,
    { loading },
  ] = useMutation<IUploadVulnerabilitiesResultAttr>(UPLOAD_VULNERABILITIES, {
    onCompleted: (result: IUploadVulnerabilitiesResultAttr): void => {
      if (!_.isUndefined(result)) {
        if (result.uploadFile.success) {
          msgSuccess(
            translate.t("groupAlerts.fileUpdated"),
            translate.t("groupAlerts.titleSuccess")
          );
          dispatch(reset("vulns"));
        }
      }
    },
    onError: handleUploadError,
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst: permissions.can(
            "backend_api_resolvers_vulnerability_analyst_resolve"
          ),
          canRetrieveZeroRisk: permissions.can(
            "backend_api_resolvers_finding_zero_risk_resolve"
          ),
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_HEADER,
        variables: {
          canGetExploit: groupPermissions.can("has_forces"),
          canGetHistoricState: permissions.can(
            "backend_api_resolvers_finding_historic_state_resolve"
          ),
          findingId,
        },
      },
    ],
  });
  const [
    downloadVulnerability,
  ] = useMutation<IDownloadVulnerabilitiesResultAttr>(
    DOWNLOAD_VULNERABILITIES,
    {
      onCompleted: (result: IDownloadVulnerabilitiesResultAttr): void => {
        if (!_.isUndefined(result)) {
          if (
            result.downloadVulnFile.success &&
            result.downloadVulnFile.url !== ""
          ) {
            openUrl(result.downloadVulnFile.url);
          }
        }
      },
      onError: (downloadError: ApolloError): void => {
        downloadError.graphQLErrors.forEach(
          ({ message }: GraphQLError): void => {
            msgError(translate.t("groupAlerts.errorTextsad"));
            switch (message) {
              case "Exception - Error Uploading File to S3":
                Logger.warning(
                  "An error occurred downloading vuln file while uploading file to S3",
                  downloadError
                );
                break;
              default:
                Logger.warning(
                  "An error occurred downloading vuln file",
                  downloadError
                );
            }
          }
        );
      },
    }
  );

  function handleUploadVulnerability(values: { filename: FileList }): void {
    void uploadVulnerability({
      variables: {
        file: values.filename[0],
        findingId,
      },
    });
  }

  function handleDownloadVulnerability(): void {
    void downloadVulnerability({
      variables: {
        findingId,
      },
    });
  }

  return (
    <GenericForm name={"vulns"} onSubmit={handleUploadVulnerability}>
      <React.Fragment>
        <br />
        <RowCenter>
          <Col33>
            <ButtonToolbarLeft>
              <TooltipWrapper
                id={translate.t(
                  "searchFindings.tabDescription.downloadVulnerabilitiesTooltip.id"
                )}
                message={translate.t(
                  "searchFindings.tabDescription.downloadVulnerabilitiesTooltip"
                )}
              >
                <Button
                  disabled={loading}
                  onClick={handleDownloadVulnerability}
                >
                  <FluidIcon icon={"export"} />
                  &nbsp;
                  {translate.t(
                    "searchFindings.tabDescription.downloadVulnerabilities"
                  )}
                </Button>
              </TooltipWrapper>
            </ButtonToolbarLeft>
          </Col33>
          <Col25 className={"upload-file"}>
            <FormGroup>
              <Field
                accept={".yaml, .yml"}
                component={FileInput}
                id={"vulnerabilities"}
                name={"filename"}
                validate={[isValidVulnsFile]}
              />
            </FormGroup>
          </Col25>
          <Col33>
            <ButtonToolbarLeft>
              <TooltipWrapper
                id={translate.t(
                  "searchFindings.tabDescription.updateVulnerabilitiesTooltip.id"
                )}
                message={translate.t(
                  "searchFindings.tabDescription.updateVulnerabilitiesTooltip"
                )}
              >
                <Button disabled={loading} type={"submit"}>
                  <FluidIcon icon={"import"} />
                  &nbsp;
                  {translate.t(
                    "searchFindings.tabDescription.updateVulnerabilities"
                  )}
                </Button>
              </TooltipWrapper>
            </ButtonToolbarLeft>
          </Col33>
        </RowCenter>
      </React.Fragment>
    </GenericForm>
  );
};
