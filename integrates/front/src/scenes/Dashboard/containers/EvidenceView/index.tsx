/* eslint-disable @typescript-eslint/no-unsafe-member-access
-- annotation needed as the DB handles "any" type */
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import type { ExecutionResult } from "@apollo/react-common";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { NetworkStatus } from "apollo-client";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { faImage } from "@fortawesome/free-solid-svg-icons";
import globalStyle from "styles/global.css";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import styles from "scenes/Dashboard/containers/EvidenceView/index.css";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import { ButtonToolbarRow, Row } from "styles/styledComponents";
import {
  GET_FINDING_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EvidenceView/queries";
import type { InjectedFormProps, Validator } from "redux-form";
import { isValidFileSize, validEvidenceImage } from "utils/validations";
import { useMutation, useQuery } from "@apollo/react-hooks";

const EvidenceView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: () => void = React.useCallback((): void => {
    setEditing(!isEditing);
  }, [isEditing]);

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);

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
            msgError(translate.t("validations.invalid_char"));
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
            msgError(translate.t("validations.file_size", { count: 10 }));
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
      description: translate.t(
        "search_findings.tab_evidence.animation_exploit"
      ),
    },
    exploitation: {
      ...data.finding.evidence.exploitation,
      description: translate.t("search_findings.tab_evidence.evidence_exploit"),
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
        const mtResult: ExecutionResult = await updateEvidence({
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
            id={"search_findings.tab_evidence.editable_tooltip.id"}
            message={translate.t(
              "search_findings.tab_evidence.editable_tooltip"
            )}
          >
            <Button onClick={handleEditClick}>
              <FluidIcon icon={"edit"} />
              &nbsp;{translate.t("search_findings.tab_evidence.editable")}
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
                      "search_findings.tab_evidence.update_tooltip.id"
                    )}
                    message={translate.t(
                      "search_findings.tab_evidence.update_tooltip"
                    )}
                  >
                    <Button disabled={pristine} type={"submit"}>
                      <FluidIcon icon={"loading"} />
                      &nbsp;{translate.t("search_findings.tab_evidence.update")}
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
                      mixpanel.track("RemoveEvidence");
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
                        description={evidence.description}
                        isDescriptionEditable={index > 1}
                        isEditing={isEditing}
                        isRemovable={!_.isEmpty(evidence.url)}
                        key={index} // eslint-disable-line react/no-array-index-key
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
