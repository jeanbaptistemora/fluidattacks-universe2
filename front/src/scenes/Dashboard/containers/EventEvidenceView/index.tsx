/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
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
import { default as globalStyle } from "../../../../styles/global.css";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { validEventFile, validEvidenceImage } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import {
  DOWNLOAD_FILE_MUTATION, GET_EVENT_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "./queries";

type EventEvidenceProps = RouteComponentProps<{ eventId: string }>;

const eventEvidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { eventId } = props.match.params;

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [isImageOpen, setImageOpen] = React.useState(false);
  const closeImage: (() => void) = (): void => { setImageOpen(false); };
  const openImage: (() => void) = (): void => { if (!isEditing) { setImageOpen(true); } };

  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  return (
    <React.StrictMode>
      <Query query={GET_EVENT_EVIDENCES} variables={{ eventId }}>
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          const renderLightbox: (() => JSX.Element) = (): JSX.Element => {
            const adjustZoom: (() => void) = (): void => {
              /**
               * As a workaround to a bug in this component,
               * we need trigger the resize event for it to
               * properly calculate the image scale
               */
              setTimeout((): void => { window.dispatchEvent(new Event("resize")); }, 50);
            };

            return (
              <Lightbox
                mainSrc={`${baseUrl}/${data.event.evidence}`}
                imagePadding={50}
                onAfterOpen={adjustZoom}
                onCloseRequest={closeImage}
                reactModalStyle={{ overlay: { zIndex: "1200" } }}
              />
            );
          };

          const handleUpdateResult: (() => void) = (): void => {
            refetch()
              .catch();
          };
          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - Invalid File Size":
                  msgError(translate.t("proj_alerts.file_size"));
                  break;
                case "Exception - Invalid File Type: EVENT_IMAGE":
                  msgError(translate.t("project.events.form.wrong_image_type"));
                  break;
                case "Exception - Invalid File Type: EVENT_FILE":
                  msgError(translate.t("project.events.form.wrong_file_type"));
                  break;
                default:
                  msgError(translate.t("proj_alerts.error_textsad"));
                  rollbar.error("An error occurred updating event evidence", updateError);
              }
            });
          };

          const { userRole } = (window as typeof window & { userRole: string });
          const canEdit: boolean = _.includes(["admin", "analyst"], userRole)
            && data.event.eventStatus !== "CLOSED";

          return (
            <React.Fragment>
              <Row>
                <Col md={2} mdOffset={10} xs={12} sm={12}>
                  {canEdit
                    ? (
                      <Button block={true} onClick={handleEditClick}>
                        <FluidIcon icon="edit" />&nbsp;{translate.t("project.events.evidence.edit")}
                      </Button>
                    )
                    : undefined}
                </Col>
              </Row>
              {_.isEmpty(data.event.evidence) && _.isEmpty(data.event.evidenceFile) && !isEditing ? (
                <div className={globalStyle.noData}>
                  <Glyphicon glyph="picture" />
                  <p>{translate.t("project.events.evidence.no_data")}</p>
                </div>
              ) : undefined}
              {!_.isEmpty(data.event.evidence) || isEditing
                ? <Mutation
                  mutation={UPDATE_EVIDENCE_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleUpdateError}
                >
                  {(updateEvidence: MutationFn): React.ReactNode => {
                    const handleUpdate: ((values: { filename: FileList }) => void) = (
                      values: { filename: FileList },
                    ): void => {
                      updateEvidence({
                        variables: { eventId, evidenceType: "IMAGE", file: values.filename[0] },
                      })
                        .catch();
                      setEditing(false);
                    };

                    return (
                      <Mutation mutation={REMOVE_EVIDENCE_MUTATION} onCompleted={handleUpdateResult}>
                        {(removeImage: MutationFn): React.ReactNode => {
                          const handleRemove: (() => void) = (): void => {
                            removeImage({ variables: { eventId, evidenceType: "IMAGE" } })
                              .catch();
                            setEditing(false);
                          };

                          return (
                            <EvidenceImage
                              acceptedMimes="image/jpeg,image/gif,image/png"
                              content={_.isEmpty(data.event.evidence) ? <div /> : `${baseUrl}/${data.event.evidence}`}
                              description="Evidence"
                              isDescriptionEditable={false}
                              isEditing={isEditing}
                              isRemovable={!_.isEmpty(data.event.evidence)}
                              name="evidence"
                              onClick={openImage}
                              onDelete={handleRemove}
                              onUpdate={handleUpdate}
                              validate={validEvidenceImage}
                            />
                          );
                        }}
                      </Mutation>
                    );
                  }}
                </Mutation>
                : undefined}
              {!_.isEmpty(data.event.evidenceFile) || isEditing
                ? <Mutation
                  mutation={UPDATE_EVIDENCE_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleUpdateError}
                >
                  {(updateEvidence: MutationFn): React.ReactNode => {
                    const handleUpdate: ((values: { filename: FileList }) => void) = (
                      values: { filename: FileList },
                    ): void => {
                      updateEvidence({
                        variables: { eventId, evidenceType: "FILE", file: values.filename[0] },
                      })
                        .catch();
                      setEditing(false);
                    };

                    const handleDownload: ((downloadData: { downloadEventFile: { url: string } }) => void) = (
                      downloadData: { downloadEventFile: { url: string } },
                    ): void => {
                      const newTab: Window | null = window.open(downloadData.downloadEventFile.url);
                      (newTab as Window).opener = undefined;
                    };

                    return (
                      <Mutation mutation={DOWNLOAD_FILE_MUTATION} onCompleted={handleDownload}>
                        {(downloadEvidence: MutationFn): React.ReactNode => {
                          const handleClick: (() => void) = (): void => {
                            if (!isEditing) {
                              downloadEvidence({ variables: { eventId, fileName: data.event.evidenceFile } })
                                .catch();
                            }
                          };

                          return (
                            <Mutation mutation={REMOVE_EVIDENCE_MUTATION} onCompleted={handleUpdateResult}>
                              {(removeFile: MutationFn): React.ReactNode => {
                                const handleRemove: (() => void) = (): void => {
                                  removeFile({ variables: { eventId, evidenceType: "FILE" } })
                                    .catch();
                                  setEditing(false);
                                };

                                return (
                                  <EvidenceImage
                                    acceptedMimes="application/pdf,application/zip,text/csv,text/plain"
                                    content={<Glyphicon glyph="file" />}
                                    description="File"
                                    isDescriptionEditable={false}
                                    isEditing={isEditing}
                                    isRemovable={!_.isEmpty(data.event.evidenceFile)}
                                    name="file"
                                    onClick={handleClick}
                                    onDelete={handleRemove}
                                    onUpdate={handleUpdate}
                                    validate={validEventFile}
                                  />
                                );
                              }}
                            </Mutation>
                          );
                        }}
                      </Mutation>
                    );
                  }}
                </Mutation>
                : undefined}
              {isImageOpen ? renderLightbox() : undefined}
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { eventEvidenceView as EventEvidenceView };
