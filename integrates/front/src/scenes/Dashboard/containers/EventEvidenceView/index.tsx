/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { faFile, faImage } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ApolloError, NetworkStatus } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router";
import { InjectedFormProps, Validator } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  DOWNLOAD_FILE_MUTATION, GET_EVENT_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import { default as globalStyle } from "styles/global.css";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import { isValidFileSize, validEventFile, validEvidenceImage } from "utils/validations";

const eventEvidenceView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery(GET_EVENT_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading event evidences", error);
      });
    },
    variables: { eventId },
  });
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [downloadEvidence] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadEventFile: { url: string } }): void => {
      openUrl(downloadData.downloadEventFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred downloading event file", error);
      });
    },
  });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: refetch,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred removing event evidence", error);
      });
    },
  });
  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - The event has already been closed":
            msgError(translate.t("group.events.alreadyClosed"));
            break;
          case "Exception - Invalid File Size":
            msgError(translate.t("validations.file_size", { count: 10 }));
            break;
          case "Exception - Invalid File Type: EVENT_IMAGE":
            msgError(translate.t("group.events.form.wrong_image_type"));
            break;
          case "Exception - Invalid File Type: EVENT_FILE":
            msgError(translate.t("group.events.form.wrong_file_type"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating event evidence", updateError);
        }
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  const openImage: (() => void) = (): void => {
    if (!isEditing && !isRefetching) { setLightboxIndex(0); }
  };

  const handleDownload: (() => void) = (): void => {
    if (!isEditing) {
      void downloadEvidence({ variables: { eventId, fileName: data.event.evidenceFile } });
    }
  };

  const removeImage: (() => void) = (): void => {
    setEditing(false);
    void removeEvidence({ variables: { eventId, evidenceType: "IMAGE" } });
  };

  const removeFile: (() => void) = (): void => {
    setEditing(false);
    void removeEvidence({ variables: { eventId, evidenceType: "FILE" } });
  };

  const handleUpdate: ((values: {}) => void) = async (values: {}): Promise<void> => {
    setEditing(false);

    const updateChanges: ((evidence: { file?: FileList }, key: string) => Promise<void>) = async (
      evidence: { file?: FileList }, key: string): Promise<void> => {
      const { file } = evidence;

      if (!_.isUndefined(file)) {
        await updateEvidence({ variables: { eventId, evidenceType: key.toUpperCase(), file: file[0] } });
      }
    };

    await Promise.all(_.map(values, updateChanges));
    setLightboxIndex(-1);
    await refetch();
  };

  const showEmpty: boolean = _.isEmpty(data.event.evidence) || isRefetching;

  const maxFileSize: Validator = isValidFileSize(10);

  return (
    <React.StrictMode>
      <React.Fragment>
        <ButtonToolbarRow>
          <Can do="backend_api_mutations_update_event_evidence_mutate">
            <TooltipWrapper
              id={translate.t("group.events.evidence.edit_tooltip.id")}
              message={translate.t("group.events.evidence.edit_tooltip")}
            >
              <Button disabled={data.event.eventStatus === "SOLVED"} onClick={handleEditClick}>
                <FluidIcon icon="edit" />&nbsp;{translate.t("group.events.evidence.edit")}
              </Button>
            </TooltipWrapper>
          </Can>
        </ButtonToolbarRow>
        <br />
        {_.isEmpty(data.event.evidence) && _.isEmpty(data.event.evidenceFile) && !isEditing ? (
          <div className={globalStyle["no-data"]}>
            <FontAwesomeIcon size={"3x"} icon={faImage} />
            <p>{translate.t("group.events.evidence.no_data")}</p>
          </div>
        ) : undefined}
        <GenericForm name="editEvidences" onSubmit={handleUpdate}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              {isEditing ? (
                <ButtonToolbarRow>
                  <TooltipWrapper
                    id={translate.t("search_findings.tab_evidence.update_tooltip.id")}
                    message={translate.t("search_findings.tab_evidence.update_tooltip")}
                  >
                    <Button type="submit" disabled={pristine}>
                      <FluidIcon icon="loading" />&nbsp;{translate.t("search_findings.tab_evidence.update")}
                    </Button>
                  </TooltipWrapper>
                </ButtonToolbarRow>
              ) : undefined}
              {!_.isEmpty(data.event.evidence) || isEditing ? (
                <EvidenceImage
                  acceptedMimes="image/gif,image/png"
                  content={showEmpty ? <div /> : `${location.href}/${data.event.evidence}`}
                  description="Evidence"
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidence)}
                  name="image"
                  onClick={openImage}
                  onDelete={removeImage}
                  validate={[validEvidenceImage, maxFileSize]}
                />
              ) : undefined}
              {!_.isEmpty(data.event.evidenceFile) || isEditing ? (
                <EvidenceImage
                  acceptedMimes="application/pdf,application/zip,text/csv,text/plain"
                  content={
                    <div>
                      <FontAwesomeIcon size={"1x"} icon={faFile} />
                    </div>
                  }
                  description="File"
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidenceFile)}
                  name="file"
                  onClick={handleDownload}
                  onDelete={removeFile}
                  validate={[validEventFile, maxFileSize]}
                />
              ) : undefined}
            </React.Fragment>
          )}</GenericForm>
        <EvidenceLightbox
          evidenceImages={[{ url: data.event.evidence }]}
          index={lightboxIndex}
          onChange={setLightboxIndex}
        />
      </React.Fragment>
    </React.StrictMode>
  );
};

export { eventEvidenceView as EventEvidenceView };
