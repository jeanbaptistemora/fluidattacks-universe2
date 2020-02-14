/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { default as globalStyle } from "../../../../styles/global.css";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { validEventFile, validEvidenceImage } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import { EvidenceLightbox } from "../../components/EvidenceLightbox";
import {
  DOWNLOAD_FILE_MUTATION, GET_EVENT_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "./queries";

type EventEvidenceProps = RouteComponentProps<{ eventId: string }>;

const eventEvidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { eventId } = props.match.params;
  const { userRole } = window as typeof window & Dictionary<string>;
  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);
  const openImage: (() => void) = (): void => {
    if (!isEditing) { setLightboxIndex(0); }
  };

  // GraphQL operations
  const { data, refetch } = useQuery(GET_EVENT_EVIDENCES, { variables: { eventId } });
  const [downloadEvidence] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadEventFile: { url: string } }): void => {
      const newTab: Window | null = window.open(downloadData.downloadEventFile.url);
      (newTab as Window).opener = undefined;
    },
  });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, { onCompleted: refetch });
  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onCompleted: refetch,
    onError: (updateError: ApolloError): void => {
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
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  const handleDownload: (() => void) = (): void => {
    if (!isEditing) {
      downloadEvidence({ variables: { eventId, fileName: data.event.evidenceFile } })
        .catch();
    }
  };

  const removeImage: (() => void) = (): void => {
    setEditing(false);
    removeEvidence({ variables: { eventId, evidenceType: "IMAGE" } })
      .catch();
  };

  const removeFile: (() => void) = (): void => {
    setEditing(false);
    removeEvidence({ variables: { eventId, evidenceType: "FILE" } })
      .catch();
  };

  const updateImage: ((values: { filename: FileList }) => void) = (values: { filename: FileList }): void => {
    setEditing(false);

    updateEvidence({
      variables: { eventId, evidenceType: "IMAGE", file: values.filename[0] },
    })
      .catch();
  };

  const updateFile: ((values: { filename: FileList }) => void) = (values: { filename: FileList }): void => {
    setEditing(false);

    updateEvidence({
      variables: { eventId, evidenceType: "FILE", file: values.filename[0] },
    })
      .catch();
  };

  const canEdit: boolean = _.includes(["admin", "analyst"], userRole) && data.event.eventStatus !== "CLOSED";

  return (
    <React.StrictMode>
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
              {!_.isEmpty(data.event.evidence) || isEditing ? (
                            <EvidenceImage
                              acceptedMimes="image/jpeg,image/gif,image/png"
                              content={_.isEmpty(data.event.evidence) ? <div /> : `${baseUrl}/${data.event.evidence}`}
                              description="Evidence"
                              isDescriptionEditable={false}
                              isEditing={isEditing}
                              isRemovable={!_.isEmpty(data.event.evidence)}
                              name="image"
                              onClick={openImage}
                              onDelete={removeImage}
                              onUpdate={updateImage}
                              validate={validEvidenceImage}
                            />
              ) : undefined}
              {!_.isEmpty(data.event.evidenceFile) || isEditing ? (
                                  <EvidenceImage
                                    acceptedMimes="application/pdf,application/zip,text/csv,text/plain"
                                    content={<Glyphicon glyph="file" />}
                                    description="File"
                                    isDescriptionEditable={false}
                                    isEditing={isEditing}
                                    isRemovable={!_.isEmpty(data.event.evidenceFile)}
                                    name="file"
                                    onClick={handleDownload}
                                    onDelete={removeFile}
                                    onUpdate={updateFile}
                                    validate={validEventFile}
                                  />
              ) : undefined}
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
