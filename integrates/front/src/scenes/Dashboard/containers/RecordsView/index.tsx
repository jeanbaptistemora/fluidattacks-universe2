import { useMutation, useQuery } from "@apollo/react-hooks";
import { faCloudUploadAlt, faList } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useParams } from "react-router";
import { Field, InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION } from "scenes/Dashboard/containers/EvidenceView/queries";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/RecordsView/queries";
import { default as globalStyle } from "styles/global.css";
import { ButtonToolbarRow, Col100, Row, RowCenter } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FileInput } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required, validRecordsFile } from "utils/validations";

const recordsView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding records", error);
    });
  };

  const handleRemoveErrors: ((removeError: ApolloError) => void) = (removeError: ApolloError): void => {
    msgError(translate.t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred removing records", removeError);
  };

  const { data, refetch } = useQuery(GET_FINDING_RECORDS, {
    onError: handleErrors,
    variables: { findingId },
  });

  const handleUpdateResult: (() => void) = (): void => {
    void refetch();
  };

  const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Wrong File Structure":
          msgError(translate.t("groupAlerts.invalidStructure"));
          break;
        case "Exception - Invalid File Size":
          msgError(translate.t("validations.file_size", { count: 1 }));
          break;
        case "Exception - Invalid File Type":
          msgError(translate.t("groupAlerts.fileTypeCsv"));
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred updating records", updateError);
      }
    });
  };

  const [updateRecords, updateRes] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onCompleted: handleUpdateResult,
    onError: handleUpdateError,
  });

  const handleSubmit: ((values: { filename: FileList }) => void) = (
    values: { filename: FileList },
  ): void => {
    setEditing(false);
    void updateRecords({ variables: { evidenceId: "RECORDS", file: values.filename[0], findingId } });
  };

  const [removeRecords, removeRes] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: handleUpdateResult,
    onError: handleRemoveErrors,
  });

  const handleRemoveClick: (() => void) = (): void => {
    mixpanel.track("RemoveRecords");
    setEditing(false);
    void removeRecords({ variables: { evidenceId: "RECORDS", findingId } });
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <Can do="backend_api_mutations_update_evidence_mutate">
          <Row>
            <Col100 className={"pa0"}>
              <ButtonToolbarRow>
                <TooltipWrapper
                  id={translate.t("search_findings.tab_records.editableTooltip.id")}
                  message={translate.t("search_findings.tab_records.editableTooltip")}
                >
                  <Button className={"fr"} onClick={handleEditClick}>
                    <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_records.editable")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarRow>
            </Col100>
          </Row>
        </Can>
        <br />
        {isEditing ? (
          <GenericForm name="records" onSubmit={handleSubmit}>
            {({ pristine }: InjectedFormProps): React.ReactNode => (
              <React.Fragment>
                <ButtonToolbarRow className={"mb3"}>
                  <Field
                    accept=".csv"
                    component={FileInput}
                    className={"fr"}
                    id="recordsFile"
                    name="filename"
                    validate={[required, validRecordsFile]}
                  />
                  <Button className={"h-25"} type="submit" disabled={pristine || updateRes.loading}>
                    <FontAwesomeIcon icon={faCloudUploadAlt} />
                    &nbsp;{translate.t("search_findings.tab_evidence.update")}
                  </Button>
                </ButtonToolbarRow>
              </React.Fragment>
            )}
          </GenericForm>
        ) : undefined}
        {isEditing && !_.isEmpty(JSON.parse(data.finding.records)) ? (
          <Row>
            <Col100 className={"pa0"}>
              <Button className={"fr"} onClick={handleRemoveClick} disabled={removeRes.loading}>
                <FluidIcon icon="delete" />
                &nbsp;{translate.t("search_findings.tab_evidence.remove")}
              </Button>
            </Col100>
          </Row>
        ) : undefined}
        <RowCenter>
          {_.isEmpty(JSON.parse(data.finding.records)) ? (
            <div className={globalStyle["no-data"]}>
              <FontAwesomeIcon size={"3x"} icon={faList} />
              <p>{translate.t("group.findings.records.noData")}</p>
            </div>
          ) : (
              <DataTableNext
                bordered={true}
                dataset={JSON.parse(data.finding.records)}
                exportCsv={false}
                headers={[]}
                id="tblRecords"
                pageSize={15}
                search={false}
              />
            )}
        </RowCenter>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { recordsView as RecordsView };
