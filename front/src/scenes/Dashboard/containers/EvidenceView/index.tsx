/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { default as globalStyle } from "../../../../styles/global.css";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { validEvidenceImage } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import { EvidenceLightbox } from "../../components/EvidenceLightbox";
import styles from "./index.css";
import {
  GET_FINDING_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_DESCRIPTION_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "./queries";

type EventEvidenceProps = RouteComponentProps<{ findingId: string }>;

const evidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { findingId } = props.match.params;
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;
  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingEvidence", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FINDING_EVIDENCES, { variables: { findingId } });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, { onCompleted: refetch });
  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, { onCompleted: refetch });
  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid File Size":
            msgError(translate.t("proj_alerts.file_size"));
            break;
          case "Exception - Invalid File Type":
            msgError(translate.t("project.events.form.wrong_image_type"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred updating finding evidence", updateError);
        }
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  interface IEvidenceItem { description: string; url: string; }
  const evidenceImages: Dictionary<IEvidenceItem> = {
    ...data.finding.evidence,
    animation: {
      ...data.finding.evidence.animation,
      description: translate.t("search_findings.tab_evidence.animation_exploit"),
    },
    exploitation: {
      ...data.finding.evidence.exploitation,
      description: translate.t("search_findings.tab_evidence.evidence_exploit"),
    },
  };
  const evidenceList: string[] = _.uniq(["animation", "exploitation", ...Object.keys(evidenceImages)])
    .filter((name: string) => _.isEmpty(evidenceImages[name].url) ? isEditing : true);

  const canEdit: boolean = _.includes(["admin", "analyst"], userRole);

  return (
    <React.StrictMode>
              <Row>
                <Col md={2} mdOffset={10} xs={12} sm={12}>
                  {canEdit ? (
                    <Button block={true} onClick={handleEditClick}>
                      <FluidIcon icon="edit" />&nbsp;{translate.t("project.findings.evidence.edit")}
                    </Button>
                  ) : undefined}
                </Col>
              </Row>
              {_.isEmpty(evidenceList) && !isEditing
                ? (
                  <div className={globalStyle.noData}>
                    <Glyphicon glyph="picture" />
                    <p>{translate.t("project.findings.evidence.no_data")}</p>
                  </div>
                )
                : (
                <Row className={styles.evidenceGrid}>
                {evidenceList.map((name: string, index: number): JSX.Element => {
                          const evidence: IEvidenceItem = evidenceImages[name];

                          const handleUpdate: ((values: { description: string; filename: FileList }) => void) = (
                            values: { description: string; filename: FileList },
                          ): void => {
                            setEditing(false);

                            if (_.isUndefined(values.filename)) {
                              if (_.isEmpty(evidence.url)) {
                                msgError(translate.t("proj_alerts.no_file_selected"));
                              } else {
                                updateDescription({
                                  variables: {
                                    description: values.description, evidenceId: name.toUpperCase(), findingId,
                                  },
                                })
                                  .catch();
                              }
                            } else {
                              updateEvidence({
                                variables: { evidenceId: name.toUpperCase(), file: values.filename[0], findingId },
                              })
                                .then((mtResult: void | {}): void => {
                                  interface IMutationResult { data: { updateEvidence: { success: boolean } }; }
                                  const { success } = (mtResult as IMutationResult).data.updateEvidence;
                                  if (success) {
                                    if (index > 1) {
                                      updateDescription({
                                        variables: {
                                          description: values.description,
                                          evidenceId: name.toUpperCase(),
                                          findingId,
                                        },
                                      })
                                        .catch();
                                    } else {
                                      refetch()
                                        .catch();
                                    }
                                  }
                                })
                                .catch();
                            }
                          };

                          const handleRemove: (() => void) = (): void => {
                                  mixpanel.track("RemoveEvidence", { Organization: userOrganization, User: userName });
                                  setEditing(false);
                                  removeEvidence({ variables: { evidenceId: name.toUpperCase(), findingId } })
                                    .catch();
                                };

                          const openImage: (() => void) = (): void => {
                                  if (!isEditing) { setLightboxIndex(index); }
                                };

                          return (
                                  <EvidenceImage
                                    acceptedMimes="image/jpeg,image/gif,image/png"
                                    content={_.isEmpty(evidence.url) ? <div /> : `${baseUrl}/${evidence.url}`}
                                    description={evidence.description}
                                    isDescriptionEditable={index > 1}
                                    isEditing={isEditing}
                                    isRemovable={!_.isEmpty(evidence.url)}
                                    key={index}
                                    name={`evidence${index}`}
                                    onClick={openImage}
                                    onDelete={handleRemove}
                                    onUpdate={handleUpdate}
                                    validate={validEvidenceImage}
                                  />
                  );
                })}
              </Row>
              )}
      <EvidenceLightbox
        evidenceImages={evidenceList.map((name: string) => evidenceImages[name])}
        index={lightboxIndex}
        onChange={setLightboxIndex}
      />
    </React.StrictMode>
  );
};

export { evidenceView as EvidenceView };
