/* eslint-disable @typescript-eslint/no-unsafe-member-access
-- annotation needed as the DB handles "any" type */
import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faImage } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router";
import type { InjectedFormProps, Validator } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import styles from "scenes/Dashboard/containers/EvidenceView/index.css";
import {
  GET_FINDING_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EvidenceView/queries";
import globalStyle from "styles/global.css";
import { ButtonToolbarRow, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { isValidFileSize, validEvidenceImage } from "utils/validations";

const EvidenceView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  // State management
  const [isEditing, setEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setEditing(!isEditing);
  }, [isEditing]);

  const [lightboxIndex, setLightboxIndex] = useState(-1);

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery(GET_FINDING_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding evidences", error);
      });
    },
    variables: { findingId },
  });
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: refetch,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing finding evidences", error);
      });
    },
  });
  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalidChar"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating finding evidence",
              updateError
            );
        }
      });
    },
  });

  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid File Size":
            msgError(translate.t("validations.fileSize", { count: 10 }));
            break;
          case "Exception - Invalid File Type":
            msgError(translate.t("group.events.form.wrongImageType"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating finding evidence",
              updateError
            );
        }
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  interface IEvidenceItem {
    date?: string;
    description: string;
    url: string;
  }
  const evidenceImages: Dictionary<IEvidenceItem> = {
    ...data.finding.evidence,
    animation: {
      ...data.finding.evidence.animation,
    },
    exploitation: {
      ...data.finding.evidence.exploitation,
    },
  };
  const evidenceList: string[] = _.uniq([
    "animation",
    "exploitation",
    ...Object.keys(evidenceImages),
  ]).filter((name: string): boolean =>
    _.isEmpty(evidenceImages[name].url) ? isEditing : true
  );

  const handleUpdate: (values: Dictionary<IEvidenceItem>) => void = async (
    values: Dictionary<IEvidenceItem>
  ): Promise<void> => {
    setEditing(false);

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

      if (file !== undefined) {
        const mtResult = await updateEvidence({
          variables: {
            evidenceId: key.toUpperCase(),
            file: file[0],
            findingId,
          },
        });
        const { success } = (mtResult as {
          data: { updateEvidence: { success: boolean } };
        }).data.updateEvidence;

        if (success && descriptionChanged) {
          await updateDescription({
            variables: {
              description,
              evidenceId: key.toUpperCase(),
              findingId,
            },
          });
        }
      } else if (descriptionChanged) {
        await updateDescription({
          variables: {
            description,
            evidenceId: key.toUpperCase(),
            findingId,
          },
        });
      }
    };

    await Promise.all(_.map(values, updateChanges));
    setLightboxIndex(-1);
    await refetch();
  };

  const MAX_FILE_SIZE = 10;
  const maxFileSize: Validator = isValidFileSize(MAX_FILE_SIZE);

  return (
    <React.StrictMode>
      <ButtonToolbarRow>
        <Can do={"backend_api_mutations_update_evidence_mutate"}>
          <TooltipWrapper
            id={"searchFindings.tabEvidence.editableTooltip.id"}
            message={translate.t("searchFindings.tabEvidence.editableTooltip")}
          >
            <Button onClick={handleEditClick}>
              <FluidIcon icon={"edit"} />
              &nbsp;{translate.t("searchFindings.tabEvidence.editable")}
            </Button>
          </TooltipWrapper>
        </Can>
      </ButtonToolbarRow>
      <br />
      {_.isEmpty(evidenceList) ? (
        <div className={globalStyle["no-data"]}>
          <FontAwesomeIcon icon={faImage} size={"3x"} />
          <p>{translate.t("group.findings.evidence.noData")}</p>
        </div>
      ) : (
        <GenericForm
          initialValues={evidenceImages}
          name={"editEvidences"}
          onSubmit={handleUpdate} // eslint-disable-line react/jsx-no-bind
        >
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
              {/* eslint-disable-next-line react/forbid-component-props */}
              <Row className={styles.evidenceGrid}>
                {evidenceList.map(
                  (name: string, index: number): JSX.Element => {
                    const evidence: IEvidenceItem = evidenceImages[name];

                    const handleRemove: () => void = (): void => {
                      track("RemoveEvidence");
                      setEditing(false);
                      void removeEvidence({
                        variables: {
                          evidenceId: name.toUpperCase(),
                          findingId,
                        },
                      });
                    };

                    const openImage: () => void = (): void => {
                      if (!isEditing && !isRefetching) {
                        setLightboxIndex(index);
                      }
                    };

                    const showEmpty: boolean =
                      _.isEmpty(evidence.url) || isRefetching;

                    const preffix: string =
                      name === "animation"
                        ? translate.t(
                            "searchFindings.tabEvidence.animationExploit"
                          )
                        : name === "exploitation"
                        ? translate.t(
                            "searchFindings.tabEvidence.evidenceExploit"
                          )
                        : "";
                    const altDescription: string =
                      preffix !== "" && evidence.description !== ""
                        ? `${preffix}: ${evidence.description}`
                        : `${preffix}${evidence.description}`;

                    return (
                      <EvidenceImage
                        acceptedMimes={"image/gif,image/png"}
                        content={
                          showEmpty ? (
                            <div />
                          ) : (
                            `${location.href}/${evidence.url}`
                          )
                        }
                        date={evidence.date}
                        description={altDescription}
                        isDescriptionEditable={true}
                        isEditing={isEditing}
                        isRemovable={!_.isEmpty(evidence.url)}
                        key={index.toString()}
                        name={name}
                        // Next annotations needed due to nested callbacks
                        onClick={openImage} // eslint-disable-line react/jsx-no-bind
                        onDelete={handleRemove} // eslint-disable-line react/jsx-no-bind
                        validate={[validEvidenceImage, maxFileSize]}
                      />
                    );
                  }
                )}
              </Row>
            </React.Fragment>
          )}
        </GenericForm>
      )}
      <EvidenceLightbox
        evidenceImages={evidenceList.map(
          (name: string): IEvidenceItem => evidenceImages[name]
        )}
        index={lightboxIndex}
        onChange={setLightboxIndex}
      />
    </React.StrictMode>
  );
};

export { EvidenceView };
