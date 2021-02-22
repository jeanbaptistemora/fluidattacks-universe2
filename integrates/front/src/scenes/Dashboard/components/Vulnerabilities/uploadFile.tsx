/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import type { Dispatch } from "redux";
import { FileInput } from "utils/forms/fields";
import { FluidIcon } from "components/FluidIcon";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { isValidVulnsFile } from "utils/validations";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useDispatch } from "react-redux";
import { useMutation } from "@apollo/react-hooks";
import {
  ButtonToolbarLeft,
  Col25,
  Col33,
  FormGroup,
  RowCenter,
} from "styles/styledComponents";
import {
  DOWNLOAD_VULNERABILITIES,
  UPLOAD_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import { Field, reset } from "redux-form";
import type {
  IDownloadVulnerabilitiesResultAttr,
  IUploadVulnerabilitiesResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";

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
      values: string & string[];
    }
    function formatError(errorName: string, errorValue: string): string {
      return ` ${translate.t(errorName)} "${errorValue}" ${translate.t(
        "group_alerts.invalid"
      )}. `;
    }

    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message.includes("Exception - Error in range limit numbers")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgError(
          `${translate.t("group_alerts.range_error")} ${errorObject.values}`
        );
      } else if (message.includes("Exception - Invalid Schema")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
          const listValuesFormated: string[] = Array.from(
            new Set(
              errorObject.values.map((x: string): string =>
                translate.t(
                  "search_findings.tab_vuln.alerts.uploadFile.value",
                  { pattern: x }
                )
              )
            )
          );
          const listKeysFormated: string[] = Array.from(
            new Set(
              errorObject.keys.map((x: string): string =>
                translate.t("search_findings.tab_vuln.alerts.uploadFile.key", {
                  key: x,
                })
              )
            )
          );
          msgErrorStick(
            listKeysFormated.join("") + listValuesFormated.join(""),
            translate.t("group_alerts.invalid_schema")
          );
        } else {
          msgError(translate.t("group_alerts.invalid_schema"));
        }
      } else if (message === "Exception - Invalid characters") {
        msgError(translate.t("validations.invalid_char"));
      } else if (message === "Exception - Invalid File Size") {
        msgError(translate.t("validations.file_size", { count: 1 }));
      } else if (message === "Exception - Invalid File Type") {
        msgError(translate.t("group_alerts.file_type_yaml"));
      } else if (message.includes("Exception - Error in path value")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgErrorStick(`${translate.t("group_alerts.path_value")}
          ${formatError("group_alerts.value", errorObject.values)}`);
      } else if (message.includes("Exception - Error in port value")) {
        const errorObject: IErrorInfoAttr = JSON.parse(message);
        msgErrorStick(`${translate.t("group_alerts.port_value")}
          ${formatError("group_alerts.value", errorObject.values)}`);
      } else if (message === "Exception - Error in specific value") {
        msgError(translate.t("group_alerts.invalid_specific"));
      } else if (
        message ===
        "Exception - You can upload a maximum of 100 vulnerabilities per file"
      ) {
        msgError(translate.t("group_alerts.invalid_n_of_vulns"));
      } else if (message === "Exception - Error Uploading File to S3") {
        msgError(translate.t("group_alerts.error_textsad"));
      } else if (message === "Exception - Invalid Stream") {
        translate.t("group_alerts.invalid_schema");
        msgError(
          translate.t(
            "search_findings.tab_vuln.alerts.uploadFile.invalidStream"
          )
        );
      } else {
        msgError(translate.t("group_alerts.invalid_specific"));
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

  const [uploadVulnerability, { loading }] = useMutation<
    IUploadVulnerabilitiesResultAttr
  >(UPLOAD_VULNERABILITIES, {
    onCompleted: (result: IUploadVulnerabilitiesResultAttr): void => {
      if (!_.isUndefined(result)) {
        if (result.uploadFile.success) {
          msgSuccess(
            translate.t("group_alerts.file_updated"),
            translate.t("group_alerts.title_success")
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
  const [downloadVulnerability] = useMutation<
    IDownloadVulnerabilitiesResultAttr
  >(DOWNLOAD_VULNERABILITIES, {
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
      downloadError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
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
      });
    },
  });

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
                  "search_findings.tab_description.download_vulnerabilities_tooltip.id"
                )}
                message={translate.t(
                  "search_findings.tab_description.download_vulnerabilities_tooltip"
                )}
              >
                <Button
                  disabled={loading}
                  onClick={handleDownloadVulnerability}
                >
                  <FluidIcon icon={"export"} />
                  &nbsp;
                  {translate.t(
                    "search_findings.tab_description.download_vulnerabilities"
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
                  "search_findings.tab_description.update_vulnerabilities_tooltip.id"
                )}
                message={translate.t(
                  "search_findings.tab_description.update_vulnerabilities_tooltip"
                )}
              >
                <Button disabled={loading} type={"submit"}>
                  <FluidIcon icon={"import"} />
                  &nbsp;
                  {translate.t(
                    "search_findings.tab_description.update_vulnerabilities"
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
