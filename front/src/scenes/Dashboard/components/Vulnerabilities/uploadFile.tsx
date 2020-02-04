/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for accessing render props from apollo components
 */
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, MutationResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { msgError, msgErrorStick, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidVulnsFile } from "../../../../utils/validations";
import * as actionsDescription from "../../containers/DescriptionView/actions";
import { GET_FINDING_HEADER } from "../../containers/FindingContent/queries";
import { GET_FINDINGS } from "../../containers/ProjectFindingsView/queries";
import { FileInput } from "../FileInput";
import { GET_VULNERABILITIES, UPLOAD_VULNERABILITIES } from "./queries";
import { IUploadVulnerabilitiesResult, IVulnerabilitiesViewProps } from "./types";

const uploadVulnerabilities: ((props: IVulnerabilitiesViewProps) => JSX.Element) =
(props: IVulnerabilitiesViewProps): JSX.Element => {
  const baseUrl: string = `${window.location.href.split("/dashboard#!")[0]}`;
  const canGetHistoricState: boolean = _.includes(["analyst", "admin"], props.userRole);
  const projectName: string = !_.isUndefined(props.descriptParam) ? props.descriptParam.projectName : "";

  const handleUploadResult: ((mtResult: IUploadVulnerabilitiesResult) => void) =
  (mtResult: IUploadVulnerabilitiesResult): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.uploadFile.success) {
        store.dispatch(actionsDescription.editDescription());
        msgSuccess(
          translate.t("proj_alerts.file_updated"),
          translate.t("proj_alerts.title_success"));
      }
    }
  };
  const handleUploadError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
    interface IErrorInfo { keys: string[]; msg: string; values: string & string[]; }
    const formatError: (errorName: string, errorValue: string) => string =
      (errorName: string, errorValue: string): string =>
        (` ${translate.t(errorName)} "${errorValue}" ${translate.t("proj_alerts.invalid")}. `);

    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message.includes("Exception - Error in range limit numbers")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        msgError(`${translate.t("proj_alerts.range_error")} ${errorObject.values}`);
      } else if (message.includes("Exception - Invalid Schema")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
          const listValuesFormated: string[] = errorObject.values.map(
            (x: string) => formatError("proj_alerts.value", x));
          const listKeysFormated: string[] = errorObject.keys.map(
            (x: string) => formatError("proj_alerts.key", x));
          msgErrorStick(
            listKeysFormated.join("") + listValuesFormated.join(""),
            translate.t("proj_alerts.invalid_schema"));
        } else {
          msgError(translate.t("proj_alerts.invalid_schema"));
        }
      } else if (message === "Exception - Invalid File Size") {
        msgError(translate.t("proj_alerts.file_size_py"));
      } else if (message === "Exception - Invalid File Type") {
        msgError(translate.t("proj_alerts.file_type_yaml"));
      } else if (message.includes("Exception - Error in path value")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        msgErrorStick(`${translate.t("proj_alerts.path_value")}
          ${formatError("proj_alerts.value", errorObject.values)}`);
      } else if (message.includes("Exception - Error in port value")) {
        const errorObject: IErrorInfo = JSON.parse(message);
        msgErrorStick(`${translate.t("proj_alerts.port_value")}
          ${formatError("proj_alerts.value", errorObject.values)}`);
      } else if (message === "Exception - Error in specific value") {
        msgError(translate.t("proj_alerts.invalid_specific"));
      } else {
        msgError(translate.t("proj_alerts.invalid_specific"));
        rollbar.error(message);
      }
    });
  };

  return (
    <Mutation
      mutation={UPLOAD_VULNERABILITIES}
      onCompleted={handleUploadResult}
      onError={handleUploadError}
      refetchQueries={[{ query: GET_VULNERABILITIES, variables: { analystField: canGetHistoricState,
                                                                  identifier: props.findingId } },
                       { query: GET_FINDING_HEADER, variables: { findingId: props.findingId,
                                                                 submissionField: canGetHistoricState } },
                       { query: GET_FINDINGS, variables: { projectName } }]}
    >
    {(uploadVulnerability: MutationFn,
      mutationResult: MutationResult): React.ReactNode => {

      const handleUploadVulnerability: (() => void) = (): void => {
        if (isValidVulnsFile("#vulnerabilities")) {
          const selected: FileList | null = (document.querySelector("#vulnerabilities") as HTMLInputElement).files;
          if (!_.isNil(selected)) {
            uploadVulnerability({
              variables: {
                file: selected[0],
                findingId: props.findingId,
              },
            })
            .catch();
          }
        }
      };

      return (
        <React.Fragment>
          <Row>
            <Col md={4} sm={12}>
              <Button bsStyle="default" href={`${baseUrl}/${props.findingId}/download_vulnerabilities`}>
                <FluidIcon icon="export" />
                &nbsp;{translate.t("search_findings.tab_description.download_vulnerabilities")}
              </Button>
            </Col>
            <Col md={5} sm={12}>
              <FileInput icon="search" id="vulnerabilities" type=".yaml, .yml" visible={true} />
            </Col>
            <Col md={3} sm={12}>
              <Button bsStyle="primary" onClick={handleUploadVulnerability} disabled={mutationResult.loading}>
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
