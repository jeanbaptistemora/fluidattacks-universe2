import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import {
  faFile,
  faImage,
  faPen,
  faRotateRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { handleUpdateEvidenceError, showContent } from "./helpers";
import type {
  IEventEvidenceAttr,
  IGetEventEvidences,
  IUpdateEventEvidenceResultAttr,
} from "./types";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import globalStyle from "styles/global.css";
import { ButtonToolbarRow, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import {
  composeValidators,
  isValidEvidenceName,
  isValidFileSize,
  validEventFile,
  validEvidenceImage,
} from "utils/validations";

const EventEvidenceView: React.FC = (): JSX.Element => {
  const { eventId, groupName, organizationName } = useParams<{
    eventId: string;
    groupName: string;
    organizationName: string;
  }>();
  const { t } = useTranslation();

  // State management
  const [isEditing, setIsEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const [currentImage, setCurrentImage] = useState(0);
  const [isViewerOpen, setIsViewerOpen] = useState(false);

  const closeImageViewer = (index: number, isOpen: boolean): void => {
    setCurrentImage(index);
    setIsViewerOpen(isOpen);
  };

  const setOpenImageViewer: (index: number) => void = useCallback(
    (index): void => {
      setCurrentImage(index);
      setIsViewerOpen(true);
    },
    []
  );

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery<IGetEventEvidences>(
    GET_EVENT_EVIDENCES,
    {
      notifyOnNetworkStatusChange: true,
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading event evidences", error);
        });
      },
      variables: { eventId },
    }
  );
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [downloadEvidence] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: {
      downloadEventFile: { url: string };
    }): void => {
      openUrl(downloadData.downloadEventFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred downloading event file", error);
      });
    },
  });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing event evidence", error);
      });
    },
    refetchQueries: [GET_EVENT_EVIDENCES],
  });
  const [updateEvidence] = useMutation<IUpdateEventEvidenceResultAttr>(
    UPDATE_EVIDENCE_MUTATION,
    {
      onError: (updateError: ApolloError): void => {
        handleUpdateEvidenceError(updateError);
      },
    }
  );

  const handleUpdate: (
    values: Record<string, { file?: FileList }>
  ) => Promise<void> = useCallback(
    async (values: Record<string, { file?: FileList }>): Promise<void> => {
      setIsEditing(false);

      const results = await Promise.all(
        _.map(
          _.omitBy(values, (evidence: { file?: FileList }): boolean =>
            _.isUndefined(evidence.file)
          ) as Record<string, { file: FileList }>,
          async (
            evidence,
            key
          ): Promise<FetchResult<IUpdateEventEvidenceResultAttr>> =>
            updateEvidence({
              variables: {
                eventId,
                evidenceType: _.snakeCase(key).toUpperCase(),
                file: evidence.file[0],
              },
            })
        )
      );
      const errors = getErrors<IUpdateEventEvidenceResultAttr>(results);
      if (!_.isEmpty(results) && _.isEmpty(errors)) {
        msgSuccess(
          t("group.events.evidence.alerts.update.success"),
          t("groupAlerts.updatedTitle")
        );
      }
      setCurrentImage(0);

      await refetch();
    },
    [t, eventId, refetch, updateEvidence]
  );

  if (_.isEmpty(data) || _.isUndefined(data)) {
    return <div />;
  }

  const handleIncomingEvidence = (
    evidence: IEventEvidenceAttr | null
  ): IEventEvidenceAttr => {
    return _.isNull(evidence)
      ? {
          date: "",
          fileName: "",
        }
      : evidence;
  };

  const evidenceImages: Record<string, IEventEvidenceAttr> = {
    image1: handleIncomingEvidence(data.event.evidences.image1),
    image2: handleIncomingEvidence(data.event.evidences.image2),
    image3: handleIncomingEvidence(data.event.evidences.image3),
    image4: handleIncomingEvidence(data.event.evidences.image4),
    image5: handleIncomingEvidence(data.event.evidences.image5),
    image6: handleIncomingEvidence(data.event.evidences.image6),
  };
  const imageList: string[] = Object.keys(evidenceImages).filter(
    (name: string): boolean =>
      _.isEmpty(evidenceImages[name].fileName) ? isEditing : true
  );
  const evidenceFiles: Record<string, IEventEvidenceAttr> = {
    file1: handleIncomingEvidence(data.event.evidences.file1),
  };
  const fileList: string[] = Object.keys(evidenceFiles).filter(
    (name: string): boolean =>
      _.isEmpty(evidenceFiles[name].fileName) ? isEditing : true
  );

  const MAX_FILE_SIZE = 10;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);
  const validEvidenceName: FieldValidator = isValidEvidenceName(
    organizationName,
    groupName
  );

  return (
    <React.StrictMode>
      <React.Fragment>
        <ButtonToolbarRow>
          <Can do={"api_mutations_update_event_evidence_mutate"}>
            <Tooltip
              id={t("group.events.evidence.editTooltip.id")}
              tip={t("group.events.evidence.editTooltip")}
            >
              <Button
                disabled={data.event.eventStatus === "SOLVED"}
                onClick={handleEditClick}
                variant={"secondary"}
              >
                <FontAwesomeIcon icon={faPen} />
                &nbsp;{t("group.events.evidence.edit")}
              </Button>
            </Tooltip>
          </Can>
        </ButtonToolbarRow>
        <br />
        {_.isEmpty(imageList) && _.isEmpty(fileList) && !isEditing ? (
          <div className={globalStyle["no-data"]}>
            <FontAwesomeIcon icon={faImage} size={"3x"} />
            <p>{t("group.events.evidence.noData")}</p>
          </div>
        ) : undefined}
        <Formik
          enableReinitialize={true}
          initialValues={{ ...evidenceImages, ...evidenceFiles }}
          name={"editEvidences"}
          onSubmit={handleUpdate}
        >
          {({ dirty }): JSX.Element => (
            <Form id={"editEvidences"}>
              {isEditing ? (
                <ButtonToolbarRow>
                  <Tooltip
                    id={t("searchFindings.tabEvidence.updateTooltip.id")}
                    tip={t("searchFindings.tabEvidence.updateTooltip")}
                  >
                    <Button
                      disabled={!dirty}
                      type={"submit"}
                      variant={"primary"}
                    >
                      <FontAwesomeIcon icon={faRotateRight} />
                      &nbsp;{t("searchFindings.tabEvidence.update")}
                    </Button>
                  </Tooltip>
                </ButtonToolbarRow>
              ) : undefined}
              <Row>
                {imageList.map((name: string, index: number): JSX.Element => {
                  const evidence: IEventEvidenceAttr = evidenceImages[name];
                  const handleRemove = async (): Promise<void> => {
                    setIsEditing(false);
                    await removeEvidence({
                      variables: {
                        eventId,
                        evidenceType: _.snakeCase(name).toUpperCase(),
                      },
                    });
                  };

                  const openImage = (): void => {
                    if (!isEditing && !isRefetching) {
                      setOpenImageViewer(index);
                    }
                  };

                  const showEmpty: boolean =
                    _.isEmpty(evidence.fileName) || isRefetching;

                  return (
                    <EvidenceImage
                      acceptedMimes={"image/gif,image/png"}
                      content={showContent(showEmpty, evidence)}
                      date={evidence.date}
                      description={""}
                      isDescriptionEditable={false}
                      isEditing={isEditing}
                      isRemovable={!_.isEmpty(evidence.fileName)}
                      key={name}
                      name={name}
                      // Next annotations needed due to nested callbacks
                      // eslint-disable-next-line react/jsx-no-bind
                      onClick={openImage}
                      onDelete={handleRemove} // eslint-disable-line react/jsx-no-bind
                      shouldPreview={false}
                      shouldPreviewValidation={[]}
                      validate={composeValidators([
                        validEvidenceImage,
                        maxFileSize,
                        validEvidenceName,
                      ])}
                    />
                  );
                })}
                {fileList.map((name: string): JSX.Element => {
                  const evidence: IEventEvidenceAttr = evidenceFiles[name];
                  const handleRemove = async (): Promise<void> => {
                    setIsEditing(false);
                    await removeEvidence({
                      variables: {
                        eventId,
                        evidenceType: _.snakeCase(name).toUpperCase(),
                      },
                    });
                  };

                  const handleDownload = async (): Promise<void> => {
                    if (!isEditing) {
                      await downloadEvidence({
                        variables: {
                          eventId,
                          fileName: evidence.fileName,
                        },
                      });
                    }
                  };

                  return (
                    <EvidenceImage
                      acceptedMimes={
                        "application/pdf,application/zip,text/csv,text/plain"
                      }
                      content={
                        <div>
                          <FontAwesomeIcon icon={faFile} size={"1x"} />
                        </div>
                      }
                      date={evidence.date}
                      description={""}
                      isDescriptionEditable={false}
                      isEditing={isEditing}
                      isRemovable={!_.isEmpty(evidence.fileName)}
                      key={name}
                      name={name}
                      // Next annotations needed due to nested callbacks
                      onClick={handleDownload} // eslint-disable-line react/jsx-no-bind
                      onDelete={handleRemove} // eslint-disable-line react/jsx-no-bind
                      shouldPreview={false}
                      shouldPreviewValidation={[]}
                      validate={composeValidators([
                        validEventFile,
                        maxFileSize,
                      ])}
                    />
                  );
                })}
              </Row>
            </Form>
          )}
        </Formik>
        {isViewerOpen && (
          <EvidenceLightbox
            currentImage={currentImage}
            evidenceImages={imageList.map((name: string): { url: string } => ({
              url: evidenceImages[name].fileName,
            }))}
            onClose={closeImageViewer} // eslint-disable-line react/jsx-no-bind
          />
        )}
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventEvidenceView };
