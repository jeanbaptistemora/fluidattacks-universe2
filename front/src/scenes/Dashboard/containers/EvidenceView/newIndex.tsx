/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, Query, QueryResult } from "react-apollo";
import { Col, Glyphicon, Row } from "react-bootstrap";
import Lightbox from "react-image-lightbox";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that ReactImageLightbox needs
 * to display properly even if some of them are overridden later
 */
import "react-image-lightbox/style.css";
import { RouteComponentProps } from "react-router";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import translate from "../../../../utils/translations/translate";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import styles from "./index.css";
import { GET_FINDING_EVIDENCES, UPDATE_DESCRIPTION_MUTATION, UPDATE_EVIDENCE_MUTATION } from "./queries";

type EventEvidenceProps = RouteComponentProps<{ findingId: string }>;

const evidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { findingId } = props.match.params;

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightBoxIndex, setLightboxIndex] = React.useState(-1);
  const closeImage: (() => void) = (): void => {
    document.body.style.removeProperty("overflow");
    setLightboxIndex(-1);
  };

  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_EVIDENCES} variables={{ findingId }}>
        {({ data, loading, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }

          interface IEvidenceItem { description: string; url: string; }
          const {
            animation, exploitation, evidence1, evidence2, evidence3, evidence4, evidence5,
          } = data.finding.evidence;
          const evidenceImages: IEvidenceItem[] = [
            { ...animation, description: translate.t("search_findings.tab_evidence.animation_exploit") },
            { ...exploitation, description: translate.t("search_findings.tab_evidence.evidence_exploit") },
            evidence1, evidence2, evidence3, evidence4, evidence5,
          ].filter((evidence: IEvidenceItem) => isEditing ? true : !_.isEmpty(evidence.url));

          const renderLightbox: (() => JSX.Element) = (): JSX.Element => {
            const adjustZoom: (() => void) = (): void => {
              /**
               * As a workaround to a bug in this component,
               * we need trigger the resize event for it to
               * properly calculate the image scale
               */
              setTimeout((): void => { window.dispatchEvent(new Event("resize")); }, 50);
              document.body.style.overflow = "hidden";
            };
            const nextIndex: number = (lightBoxIndex + 1) % evidenceImages.length;
            const previousIndex: number = (lightBoxIndex + evidenceImages.length - 1) % evidenceImages.length;
            const moveNext: (() => void) = (): void => { setLightboxIndex(nextIndex); };
            const movePrevious: (() => void) = (): void => { setLightboxIndex(previousIndex); };

            return (
              <Lightbox
                mainSrc={`${baseUrl}/${evidenceImages[lightBoxIndex].url}`}
                nextSrc={`${baseUrl}/${evidenceImages[nextIndex].url}`}
                prevSrc={`${baseUrl}/${evidenceImages[previousIndex].url}`}
                imagePadding={50}
                imageTitle={evidenceImages[lightBoxIndex].description}
                onAfterOpen={adjustZoom}
                onCloseRequest={closeImage}
                onMoveNextRequest={moveNext}
                onMovePrevRequest={movePrevious}
                reactModalStyle={{ overlay: { zIndex: "1200" } }}
              />
            );
          };

          const handleUpdateResult: (() => void) = (): void => {
            hidePreloader();
            refetch()
              .catch();
          };

          const { userRole } = (window as typeof window & { userRole: string });
          const canEdit: boolean = _.includes(["admin", "analyst"], userRole);

          return (
            <React.Fragment>
              <Row>
                <Col md={2} mdOffset={10} xs={12} sm={12}>
                  {canEdit ? (
                    <Button block={true} onClick={handleEditClick}>
                      <FluidIcon icon="edit" />&nbsp;{translate.t("project.findings.evidence.edit")}
                    </Button>
                  ) : undefined}
                </Col>
              </Row>
              {_.isEmpty(evidenceImages) && !isEditing
                ? (
                  <div className={styles.noData}>
                    <Glyphicon glyph="picture" />
                    <p>{translate.t("project.findings.evidence.no_data")}</p>
                  </div>
                )
                : evidenceImages.map((evidence: IEvidenceItem, index: number): JSX.Element => (
                  <Mutation mutation={UPDATE_DESCRIPTION_MUTATION} onCompleted={handleUpdateResult}>
                    {(updateDescription: MutationFn): React.ReactNode => (
                      <Mutation mutation={UPDATE_EVIDENCE_MUTATION}>
                        {(updateEvidence: MutationFn): React.ReactNode => {

                          const handleUpdate: ((values: { description: string; filename: FileList }) => void) = (
                            values: { description: string; filename: FileList },
                          ): void => {
                            showPreloader();
                            setEditing(false);

                            if (_.isUndefined(values.filename) && !_.isEmpty(evidenceImages[index].url)) {
                              updateDescription({
                                variables: {
                                  description: values.description, field: `evidence${index}_description`, findingId,
                                },
                              })
                                .catch();
                            } else {
                              updateEvidence({
                                variables: { evidenceId: index, file: values.filename[0], findingId },
                              })
                                .then((mtResult: void | {}): void => {
                                  interface IMutationResult { data: { updateEvidence: { success: boolean } }; }
                                  hidePreloader();
                                  const { success } = (mtResult as IMutationResult).data.updateEvidence;
                                  if (success) {
                                    if (index > 1) {
                                      showPreloader();
                                      updateDescription({
                                        variables: {
                                          description: values.description,
                                          field: `evidence${index}_description`,
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

                          const openImage: (() => void) = (): void => { if (!isEditing) { setLightboxIndex(index); } };

                          return (
                            <EvidenceImage
                              acceptedMimes="image/png,image/gif"
                              content={_.isEmpty(evidence.url) ? <div /> : `${baseUrl}/${evidence.url}`}
                              description={evidence.description}
                              isDescriptionEditable={index > 1}
                              isEditing={isEditing}
                              key={index}
                              name={`evidence${index}`}
                              onClick={openImage}
                              onUpdate={handleUpdate}
                            />
                          );
                        }}
                      </Mutation>
                    )}
                  </Mutation>
                ))
              }
              {lightBoxIndex > -1 ? renderLightbox() : undefined}
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { evidenceView as EvidenceView };
