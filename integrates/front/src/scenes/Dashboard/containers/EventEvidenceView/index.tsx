import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFile, faImage } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import {
  checkNotEmptyOrEditing,
  getUpdateChanges,
  handleUpdateEvidenceError,
  showContent,
} from "./helpers";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import type { IGetEventEvidences } from "scenes/Dashboard/containers/EventEvidenceView/types";
import globalStyle from "styles/global.css";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import {
  composeValidators,
  isValidFileSize,
  validEventFile,
  validEvidenceImage,
} from "utils/validations";

const EventEvidenceView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { t } = useTranslation();

  // State management
  const [isEditing, setEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setEditing(!isEditing);
  }, [isEditing]);

  const [lightboxIndex, setLightboxIndex] = useState(-1);

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
    onCompleted: refetch,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing event evidence", error);
      });
    },
  });
  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      handleUpdateEvidenceError(updateError);
    },
  });

  const handleUpdate: (values: Record<string, unknown>) => void = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      setEditing(false);

      const updateChanges = getUpdateChanges(eventId, updateEvidence);

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

  const removeImage = useCallback(async (): Promise<void> => {
    setEditing(false);
    await removeEvidence({ variables: { eventId, evidenceType: "IMAGE" } });
  }, [eventId, removeEvidence]);

  const removeFile = useCallback(async (): Promise<void> => {
    setEditing(false);
    await removeEvidence({ variables: { eventId, evidenceType: "FILE" } });
  }, [eventId, removeEvidence]);

  const handleDownload = useCallback(async (): Promise<void> => {
    if (!isEditing) {
      await downloadEvidence({
        variables: { eventId, fileName: data?.event.evidenceFile },
      });
    }
  }, [data, downloadEvidence, eventId, isEditing]);

  if (_.isEmpty(data) || _.isUndefined(data)) {
    return <div />;
  }

  const showEmpty: boolean = _.isEmpty(data.event.evidence) || isRefetching;
  const MAX_FILE_SIZE = 10;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);

  return (
    <React.StrictMode>
      <React.Fragment>
        <ButtonToolbarRow>
          <Can do={"api_mutations_update_event_evidence_mutate"}>
            <TooltipWrapper
              id={t("group.events.evidence.editTooltip.id")}
              message={t("group.events.evidence.editTooltip")}
            >
              <Button
                disabled={data.event.eventStatus === "SOLVED"}
                onClick={handleEditClick}
                variant={"secondary"}
              >
                <FluidIcon icon={"edit"} />
                &nbsp;{t("group.events.evidence.edit")}
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
            <p>{t("group.events.evidence.noData")}</p>
          </div>
        ) : undefined}
        <Formik
          enableReinitialize={true}
          initialValues={data.event}
          name={"editEvidences"}
          onSubmit={handleUpdate}
        >
          {({ dirty }): JSX.Element => (
            <Form id={"editEvidences"}>
              {isEditing ? (
                <ButtonToolbarRow>
                  <TooltipWrapper
                    id={t("searchFindings.tabEvidence.updateTooltip.id")}
                    message={t("searchFindings.tabEvidence.updateTooltip")}
                  >
                    <Button
                      disabled={!dirty}
                      type={"submit"}
                      variant={"primary"}
                    >
                      <FluidIcon icon={"loading"} />
                      &nbsp;{t("searchFindings.tabEvidence.update")}
                    </Button>
                  </TooltipWrapper>
                </ButtonToolbarRow>
              ) : undefined}
              {checkNotEmptyOrEditing(data.event.evidence, isEditing) ? (
                <EvidenceImage
                  acceptedMimes={"image/gif,image/png"}
                  content={showContent(showEmpty, data)}
                  date={data.event.evidenceDate}
                  description={"Evidence"}
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidence)}
                  name={"image"}
                  onClick={openImage}
                  onDelete={removeImage}
                  validate={composeValidators([
                    validEvidenceImage,
                    maxFileSize,
                  ])}
                />
              ) : undefined}
              {checkNotEmptyOrEditing(data.event.evidenceFile, isEditing) ? (
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
                  validate={composeValidators([validEventFile, maxFileSize])}
                />
              ) : undefined}
            </Form>
          )}
        </Formik>
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
