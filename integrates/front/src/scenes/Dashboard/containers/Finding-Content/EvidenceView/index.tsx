import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faImage,
  faPen,
  faRotateRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import {
  handleUpdateDescriptionError,
  handleUpdateEvidenceError,
  setAltDescription,
  setPreffix,
  updateChangesHelper,
} from "./helpers";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import {
  GET_FINDING_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/queries";
import type {
  IEvidenceItem,
  IGetFindingEvidences,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/types";
import { ButtonToolbarRow, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import {
  composeValidators,
  isValidEvidenceName,
  isValidFileSize,
  validEvidenceImage,
} from "utils/validations";

const EvidenceView: React.FC = (): JSX.Element => {
  const { findingId, groupName, organizationName } = useParams<{
    findingId: string;
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

  const closeImageViewer = useCallback(
    (index: number, isOpen: boolean): void => {
      setCurrentImage(index);
      setIsViewerOpen(isOpen);
    },
    []
  );

  const setOpenImageViewer: (index: number) => void = useCallback(
    (index): void => {
      setCurrentImage(index);
      setIsViewerOpen(true);
    },
    []
  );

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery<IGetFindingEvidences>(
    GET_FINDING_EVIDENCES,
    {
      notifyOnNetworkStatusChange: true,
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding evidences", error);
        });
      },
      variables: { findingId },
    }
  );
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: async (): Promise<void> => {
      await refetch({ findingId });
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing finding evidences", error);
      });
    },
  });
  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onError: (updateError: ApolloError): void => {
      handleUpdateDescriptionError(updateError);
    },
  });

  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      handleUpdateEvidenceError(updateError);
    },
  });

  const openImage = useCallback(
    (index: number): (() => void) =>
      (): void => {
        if (!isEditing && !isRefetching) {
          setOpenImageViewer(index);
        }
      },
    [isEditing, isRefetching, setOpenImageViewer]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const handleIncomingEvidence = (
    evidence: Record<string, string | null>
  ): IEvidenceItem => {
    return {
      date: evidence.date ?? "",
      description: evidence.description ?? "",
      url: evidence.url ?? "",
    };
  };

  const evidenceImages: Record<string, IEvidenceItem> = {
    animation: handleIncomingEvidence(data.finding.evidence.animation),
    evidence1: handleIncomingEvidence(data.finding.evidence.evidence1),
    evidence2: handleIncomingEvidence(data.finding.evidence.evidence2),
    evidence3: handleIncomingEvidence(data.finding.evidence.evidence3),
    evidence4: handleIncomingEvidence(data.finding.evidence.evidence4),
    evidence5: handleIncomingEvidence(data.finding.evidence.evidence5),
    exploitation: handleIncomingEvidence(data.finding.evidence.exploitation),
  };
  const evidenceList: string[] = _.uniq([
    "animation",
    "exploitation",
    ...Object.keys(evidenceImages),
  ]).filter((name: string): boolean =>
    _.isEmpty(evidenceImages[name].url) ? isEditing : true
  );

  const handleUpdate: (values: Record<string, IEvidenceItem>) => Promise<void> =
    async (values: Record<string, IEvidenceItem>): Promise<void> => {
      setIsEditing(false);

      const updateChanges: (
        evidence: IEvidenceItem & { file?: FileList },
        key: string
      ) => Promise<void> = async (
        evidence: IEvidenceItem & { file?: FileList },
        key: string
      ): Promise<void> => {
        const { description, file } = evidence;
        const descriptionChanged: boolean =
          description !== evidenceImages[key].description;

        await updateChangesHelper(
          updateEvidence,
          updateDescription,
          file,
          key,
          description,
          findingId,
          descriptionChanged
        );
      };

      await Promise.all(_.map(values, updateChanges));
      setCurrentImage(0);

      await refetch();
    };

  const MAX_FILE_SIZE = 10;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);
  const validEvidenceName: FieldValidator = isValidEvidenceName(
    organizationName,
    groupName
  );

  return (
    <React.StrictMode>
      <ButtonToolbarRow>
        <Can do={"api_mutations_update_evidence_mutate"}>
          <Tooltip
            id={"searchFindings.tabEvidence.editableTooltip.id"}
            tip={t("searchFindings.tabEvidence.editableTooltip")}
          >
            <Button onClick={handleEditClick} variant={"secondary"}>
              <FontAwesomeIcon icon={faPen} />
              &nbsp;{t("searchFindings.tabEvidence.editable")}
            </Button>
          </Tooltip>
        </Can>
      </ButtonToolbarRow>
      <br />
      {_.isEmpty(evidenceList) ? (
        <div className={"no-data"}>
          <FontAwesomeIcon icon={faImage} size={"3x"} />
          <p>{t("group.findings.evidence.noData")}</p>
        </div>
      ) : (
        <Formik
          enableReinitialize={true}
          initialValues={evidenceImages}
          name={"editEvidences"}
          // eslint-disable-next-line
          onSubmit={handleUpdate} // NOSONAR
        >
          {({ dirty }): JSX.Element => (
            <Form>
              <React.Fragment>
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
                  {evidenceList.map(
                    (name: string, index: number): JSX.Element => {
                      const evidence: IEvidenceItem = evidenceImages[name];
                      const handleRemove = async (): Promise<void> => {
                        mixpanel.track("RemoveEvidence");
                        setIsEditing(false);
                        await removeEvidence({
                          variables: {
                            evidenceId: name.toUpperCase(),
                            findingId,
                          },
                        });
                      };

                      const content =
                        _.isEmpty(evidence.url) || isRefetching
                          ? ""
                          : `${location.href}/${evidence.url}`;

                      const preffix: string = setPreffix(name);
                      const altDescription = setAltDescription(
                        preffix,
                        evidence
                      );

                      return (
                        <EvidenceImage
                          acceptedMimes={"image/png,video/webm"}
                          content={content}
                          date={evidence.date ?? ""}
                          description={altDescription}
                          isDescriptionEditable={true}
                          isEditing={isEditing}
                          isRemovable={!_.isEmpty(evidence.url)}
                          key={name}
                          name={name}
                          onClick={openImage(index)}
                          // Next annotations needed due to nested callbacks
                          // eslint-disable-next-line
                          onDelete={handleRemove} // NOSONAR
                          validate={composeValidators([
                            validEvidenceImage,
                            maxFileSize,
                            validEvidenceName,
                          ])}
                        />
                      );
                    }
                  )}
                </Row>
              </React.Fragment>
            </Form>
          )}
        </Formik>
      )}
      {isViewerOpen && (
        <EvidenceLightbox
          currentImage={currentImage}
          evidenceImages={evidenceList.map((name: string): { url: string } => ({
            url: evidenceImages[name].url,
          }))}
          onClose={closeImageViewer}
        />
      )}
    </React.StrictMode>
  );
};

export type { IEvidenceItem };
export { EvidenceView };
