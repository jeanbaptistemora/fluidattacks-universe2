import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { DataTableNext } from "components/DataTableNext";
import { Field } from "redux-form";
import { FileInput } from "utils/forms/fields";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/RecordsView/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import type { InjectedFormProps } from "redux-form";
import { Logger } from "utils/logger";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import globalStyle from "styles/global.css";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import {
  ButtonToolbarRow,
  Col100,
  Row,
  RowCenter,
} from "styles/styledComponents";
import {
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EvidenceView/queries";
import { faCloudUploadAlt, faList } from "@fortawesome/free-solid-svg-icons";
import { required, validRecordsFile } from "utils/validations";
import { useMutation, useQuery } from "@apollo/react-hooks";

const RecordsView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: () => void = React.useCallback((): void => {
    setEditing(!isEditing);
  }, [isEditing]);

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding records", error);
    });
  };

  const handleRemoveErrors: (removeError: ApolloError) => void = (
    removeError: ApolloError
  ): void => {
    msgError(translate.t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred removing records", removeError);
  };

  const { data, refetch } = useQuery(GET_FINDING_RECORDS, {
    onError: handleErrors,
    variables: { findingId },
  });

  const handleUpdateResult: () => void = (): void => {
    void refetch();
  };

  const handleUpdateError: (updateError: ApolloError) => void = (
    updateError: ApolloError
  ): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Wrong File Structure":
          msgError(translate.t("groupAlerts.invalidStructure"));
          break;
        case "Exception - Invalid File Size":
          msgError(translate.t("validations.fileSize", { count: 1 }));
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

  const handleSubmit: (values: {
    filename: FileList;
  }) => void = React.useCallback(
    (values: { filename: FileList }): void => {
      setEditing(false);
      void updateRecords({
        variables: {
          evidenceId: "RECORDS",
          file: values.filename[0],
          findingId,
        },
      });
    },
    [findingId, updateRecords]
  );

  const [removeRecords, removeRes] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: handleUpdateResult,
    onError: handleRemoveErrors,
  });

  const handleRemoveClick: () => void = React.useCallback((): void => {
    mixpanel.track("RemoveRecords");
    setEditing(false);
    void removeRecords({ variables: { evidenceId: "RECORDS", findingId } });
  }, [findingId, removeRecords]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <Can do={"backend_api_mutations_update_evidence_mutate"}>
          <Row>
            {/* eslint-disable-next-line react/forbid-component-props */}
            <Col100 className={"pa0"}>
              <ButtonToolbarRow>
                <TooltipWrapper
                  id={translate.t(
                    "searchFindings.tabRecords.editableTooltip.id"
                  )}
                  message={translate.t(
                    "searchFindings.tabRecords.editableTooltip"
                  )}
                >
                  {/* eslint-disable-next-line react/forbid-component-props */}
                  <Button className={"fr"} onClick={handleEditClick}>
                    <FluidIcon icon={"edit"} />
                    &nbsp;{translate.t("searchFindings.tabRecords.editable")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarRow>
            </Col100>
          </Row>
        </Can>
        <br />
        {isEditing ? (
          <GenericForm name={"records"} onSubmit={handleSubmit}>
            {({ pristine }: InjectedFormProps): React.ReactNode => (
              // eslint-disable-next-line react/forbid-component-props
              <ButtonToolbarRow className={"mb3"}>
                <Field
                  accept={".csv"}
                  // eslint-disable-next-line react/forbid-component-props
                  className={"fr"}
                  component={FileInput}
                  id={"recordsFile"}
                  name={"filename"}
                  validate={[required, validRecordsFile]}
                />
                <Button
                  // eslint-disable-next-line react/forbid-component-props
                  className={"h-25"}
                  disabled={pristine || updateRes.loading}
                  type={"submit"}
                >
                  <FontAwesomeIcon icon={faCloudUploadAlt} />
                  &nbsp;{translate.t("searchFindings.tabEvidence.update")}
                </Button>
              </ButtonToolbarRow>
            )}
          </GenericForm>
        ) : undefined}
        {/* eslint-disable-next-line @typescript-eslint/no-unsafe-member-access */}
        {isEditing && !_.isEmpty(JSON.parse(data.finding.records)) ? (
          <Row>
            {/* eslint-disable-next-line react/forbid-component-props */}
            <Col100 className={"pa0"}>
              <Button
                // eslint-disable-next-line react/forbid-component-props
                className={"fr"}
                disabled={removeRes.loading}
                onClick={handleRemoveClick}
              >
                <FluidIcon icon={"delete"} />
                &nbsp;{translate.t("searchFindings.tabEvidence.remove")}
              </Button>
            </Col100>
          </Row>
        ) : undefined}
        <RowCenter>
          {/* eslint-disable-next-line @typescript-eslint/no-unsafe-member-access */}
          {_.isEmpty(JSON.parse(data.finding.records)) ? (
            <div className={globalStyle["no-data"]}>
              <FontAwesomeIcon icon={faList} size={"3x"} />
              <p>{translate.t("group.findings.records.noData")}</p>
            </div>
          ) : (
            <DataTableNext
              bordered={true}
              // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
              dataset={JSON.parse(data.finding.records)}
              exportCsv={false}
              headers={[]}
              id={"tblRecords"}
              pageSize={15}
              search={false}
            />
          )}
        </RowCenter>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { RecordsView };
