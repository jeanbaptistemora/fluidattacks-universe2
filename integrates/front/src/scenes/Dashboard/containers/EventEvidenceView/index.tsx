/* eslint-disable @typescript-eslint/restrict-template-expressions, @typescript-eslint/no-unsafe-member-access 
--- Needed annotations as DB queries use "any" type
*/
import { useMutation, useQuery } from "@apollo/react-hooks";
import { faFile, faImage } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ApolloError } from "apollo-client";
import { NetworkStatus } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router";
import type { InjectedFormProps, Validator } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import globalStyle from "styles/global.css";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import { translate } from "utils/translations/translate";
import {
  isValidFileSize,
  validEventFile,
  validEvidenceImage,
} from "utils/validations";

const EventEvidenceView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isEditing, setEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setEditing(!isEditing);
  }, [isEditing]);

  const [lightboxIndex, setLightboxIndex] = useState(-1);

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery(GET_EVENT_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event evidences", error);
      });
    },
    variables: { eventId },
  });
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [downloadEvidence] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: {
      downloadEventFile: { url: string };
    }): void => {
      openUrl(downloadData.downloadEventFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred downloading event file", error);
      });
    },
  });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: refetch,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
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
            msgError(translate.t("validations.fileSize", { count: 10 }));
            break;
          case "Exception - Invalid File Type: EVENT_IMAGE":
            msgError(translate.t("group.events.form.wrongImageType"));
            break;
          case "Exception - Invalid File Type: EVENT_FILE":
            msgError(translate.t("group.events.form.wrongFileType"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating event evidence",
              updateError
            );
        }
      });
    },
  });

  const handleUpdate: (values: Record<string, unknown>) => void = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      setEditing(false);

      const updateChanges: (
        evidence: { file?: FileList },
        key: string
      ) => Promise<void> = async (
        evidence: { file?: FileList },
        key: string
      ): Promise<void> => {
        const { file } = evidence;

        if (!_.isUndefined(file)) {
          await updateEvidence({
            variables: {
              eventId,
              evidenceType: key.toUpperCase(),
              file: file[0],
            },
          });
        }
      };

      await Promise.all(_.map(values, updateChanges));
      setLightboxIndex(-1);
      await refetch();
    },
    [eventId, refetch, updateEvidence]
  );

  const openImage: () => void = useCallback((): void => {
    if (!isEditing && !isRefetching) {
      setLightboxIndex(0);
    }
  }, [isEditing, isRefetching]);

  const handleDownload: () => void = (): void => {
    if (!isEditing) {
      void downloadEvidence({
        variables: { eventId, fileName: data.event.evidenceFile },
      });
    }
  };

  const removeImage: () => void = useCallback((): void => {
    setEditing(false);
    void removeEvidence({ variables: { eventId, evidenceType: "IMAGE" } });
  }, [eventId, removeEvidence]);

  const removeFile: () => void = useCallback((): void => {
    setEditing(false);
    void removeEvidence({ variables: { eventId, evidenceType: "FILE" } });
  }, [eventId, removeEvidence]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const showEmpty: boolean = _.isEmpty(data.event.evidence) || isRefetching;
  const MAX_FILE_SIZE = 10;
  const maxFileSize: Validator = isValidFileSize(MAX_FILE_SIZE);

  return (
    <React.StrictMode>
      <React.Fragment>
        <ButtonToolbarRow>
          <Can do={"backend_api_mutations_update_event_evidence_mutate"}>
            <TooltipWrapper
              id={translate.t("group.events.evidence.editTooltip.id")}
              message={translate.t("group.events.evidence.editTooltip")}
            >
              <Button
                disabled={data.event.eventStatus === "SOLVED"}
                onClick={handleEditClick}
              >
                <FluidIcon icon={"edit"} />
                &nbsp;{translate.t("group.events.evidence.edit")}
              </Button>
            </TooltipWrapper>
          </Can>
        </ButtonToolbarRow>
        <br />
        {_.isEmpty(data.event.evidence) &&
        _.isEmpty(data.event.evidenceFile) &&
        !isEditing ? (
          <div className={globalStyle["no-data"]}>
            <FontAwesomeIcon icon={faImage} size={"3x"} />
            <p>{translate.t("group.events.evidence.noData")}</p>
          </div>
        ) : undefined}
        <GenericForm name={"editEvidences"} onSubmit={handleUpdate}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              {isEditing ? (
                <ButtonToolbarRow>
                  <TooltipWrapper
                    id={translate.t(
                      "searchFindings.tabEvidence.updateTooltip.id"
                    )}
                    message={translate.t(
                      "searchFindings.tabEvidence.updateTooltip"
                    )}
                  >
                    <Button disabled={pristine} type={"submit"}>
                      <FluidIcon icon={"loading"} />
                      &nbsp;{translate.t("searchFindings.tabEvidence.update")}
                    </Button>
                  </TooltipWrapper>
                </ButtonToolbarRow>
              ) : undefined}
              {!_.isEmpty(data.event.evidence) || isEditing ? (
                <EvidenceImage
                  acceptedMimes={"image/gif,image/png"}
                  content={
                    showEmpty ? (
                      <div />
                    ) : (
                      `${location.href}/${data.event.evidence}`
                    )
                  }
                  date={data.event.evidenceDate}
                  description={"Evidence"}
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidence)}
                  name={"image"}
                  onClick={openImage}
                  onDelete={removeImage}
                  validate={[validEvidenceImage, maxFileSize]}
                />
              ) : undefined}
              {!_.isEmpty(data.event.evidenceFile) || isEditing ? (
                <EvidenceImage
                  acceptedMimes={
                    "application/pdf,application/zip,text/csv,text/plain"
                  }
                  content={
                    <div>
                      <FontAwesomeIcon icon={faFile} size={"1x"} />
                    </div>
                  }
                  date={data.event.evidenceFileDate}
                  description={"File"}
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidenceFile)}
                  name={"file"}
                  onClick={handleDownload} // eslint-disable-line react/jsx-no-bind -- Needed due to a memory leakage
                  onDelete={removeFile}
                  validate={[validEventFile, maxFileSize]}
                />
              ) : undefined}
            </React.Fragment>
          )}
        </GenericForm>
        <EvidenceLightbox
          evidenceImages={[{ url: data.event.evidence }]}
          index={lightboxIndex}
          onChange={setLightboxIndex}
        />
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventEvidenceView };
