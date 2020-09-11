/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for accessing render props from apollo components
 */
import { MutationFunction, MutationResult } from "@apollo/react-common";
import { Mutation } from "@apollo/react-components";
import { useMutation } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { submit } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { FileInput } from "scenes/Dashboard/components/FileInput";
import {
  DOWNLOAD_VULNERABILITIES, GET_VULNERABILITIES, UPLOAD_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  IDownloadVulnerabilitiesResult, IUploadVulnerabilitiesResult, IVulnerabilitiesViewProps,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import store from "store";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import { isValidVulnsFile } from "utils/validations";

const uploadVulnerabilities: ((props: IVulnerabilitiesViewProps) => JSX.Element) =
(props: IVulnerabilitiesViewProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);

  const handleUploadResult: ((mtResult: IUploadVulnerabilitiesResult) => void) =
  (mtResult: IUploadVulnerabilitiesResult): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.uploadFile.success) {
        store.dispatch(submit("editDescription"));
        msgSuccess(
          translate.t("group_alerts.file_updated"),
          translate.t("group_alerts.title_success"));
      }
    }
  };
  const handleUploadError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
    interface IErrorInfo { keys: string[]; msg: string; values: string & string[]; }
    const formatError: (errorName: string, errorValue: string) => string =
      (errorName: string, errorValue: string): string =>
        (` ${translate.t(errorName)} "${errorValue}" ${translate.t("group_alerts.invalid")}. `);

    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message.includes("Exception - Error in range limit numbers")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        msgError(`${translate.t("group_alerts.range_error")} ${errorObject.values}`);
      } else if (message.includes("Exception - Invalid Schema")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
          const listValuesFormated: string[] = errorObject.values.map(
            (x: string) => formatError("group_alerts.value", x));
          const listKeysFormated: string[] = errorObject.keys.map(
            (x: string) => formatError("group_alerts.key", x));
          msgErrorStick(
            listKeysFormated.join("") + listValuesFormated.join(""),
            translate.t("group_alerts.invalid_schema"));
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
        const errorObject: IErrorInfo = JSON.parse(message);
        msgErrorStick(`${translate.t("group_alerts.path_value")}
          ${formatError("group_alerts.value", errorObject.values)}`);
      } else if (message.includes("Exception - Error in port value")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        msgErrorStick(`${translate.t("group_alerts.port_value")}
          ${formatError("group_alerts.value", errorObject.values)}`);
      } else if (message === "Exception - Error in specific value") {
        msgError(translate.t("group_alerts.invalid_specific"));
      } else if (message === "Exception - Error Uploading File to S3") {
        msgError(translate.t("group_alerts.error_textsad"));
      } else {
        msgError(translate.t("group_alerts.invalid_specific"));
        Logger.warning(message);
      }
    });
  };

  const [downloadVulnerability] = useMutation(DOWNLOAD_VULNERABILITIES, {
    onCompleted: (result: IDownloadVulnerabilitiesResult): void => {
      if (!_.isUndefined(result)) {
        if (result.downloadVulnFile.success && result.downloadVulnFile.url !== "") {
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
              downloadError,
            );
            break;
          default:
            Logger.warning("An error occurred downloading vuln file", downloadError);
        }
      });
    },
  });

  return (
    <Mutation
      mutation={UPLOAD_VULNERABILITIES}
      onCompleted={handleUploadResult}
      onError={handleUploadError}
      refetchQueries={[
        {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: permissions.can("backend_api_resolvers_finding__get_analyst"),
            identifier: props.findingId,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit: groupPermissions.can("has_forces"),
            canGetHistoricState: permissions.can("backend_api_resolvers_finding__get_historic_state"),
            findingId: props.findingId,
          },
        },
      ]}
    >
      {(uploadVulnerability: MutationFunction, mutationResult: MutationResult): JSX.Element => {

      const handleUploadVulnerability: (() => void) = (): void => {
        if (isValidVulnsFile("#vulnerabilities")) {
          const selected: FileList | null = (document.querySelector("#vulnerabilities") as HTMLInputElement).files;
          if (!_.isNil(selected)) {
            void uploadVulnerability({
              variables: {
                file: selected[0],
                findingId: props.findingId,
              },
            });
          }
        }
      };

      const handleDownloadVulnerability: (() => void) = (): void => {
        downloadVulnerability({
          variables: {
            findingId: props.findingId,
          },
        });
      };

      return (
        <React.Fragment>
          <Row>
            <Col md={4} sm={12}>
              <Button
                bsStyle="default"
                onClick={handleDownloadVulnerability}
                disabled={mutationResult.loading}
              >
                <FluidIcon icon="export" />
                &nbsp;{translate.t("search_findings.tab_description.download_vulnerabilities")}
              </Button>
            </Col>
            <Col md={5} sm={12}>
              <FileInput icon="search" id="vulnerabilities" type=".yaml, .yml" visible={true} />
            </Col>
            <Col md={3} sm={12}>
              <Button
                bsStyle="primary"
                onClick={handleUploadVulnerability}
                disabled={mutationResult.loading}
              >
                <FluidIcon icon="import" />
                &nbsp;{translate.t("search_findings.tab_description.update_vulnerabilities")}
              </Button>
            </Col>
          </Row>
        </React.Fragment>
      );
    }}
    </Mutation>
  );
};

export { uploadVulnerabilities as UploadVulnerabilites };
