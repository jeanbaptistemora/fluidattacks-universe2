/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { default as globalStyle } from "../../../../styles/global.css";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { validEventFile, validEvidenceImage } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import { EvidenceLightbox } from "../../components/EvidenceLightbox";
import { GenericForm } from "../../components/GenericForm";
import {
  DOWNLOAD_FILE_MUTATION, GET_EVENT_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "./queries";

type EventEvidenceProps = RouteComponentProps<{ eventId: string }>;

const eventEvidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { eventId } = props.match.params;
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;
  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("EventEvidence", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);
  const openImage: (() => void) = (): void => {
    if (!isEditing) { setLightboxIndex(0); }
  };

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery(GET_EVENT_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    variables: { eventId },
  });
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [downloadEvidence] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadEventFile: { url: string } }): void => {
      const newTab: Window | null = window.open(downloadData.downloadEventFile.url);
      (newTab as Window).opener = undefined;
    },
  });
  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, { onCompleted: refetch });
  const [updateEvidence, { loading: updating }] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid File Size":
            msgError(translate.t("validations.file_size", { count: 10 }));
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

  const handleUpdate: ((values: {}) => void) = (values: {}): void => {
    setEditing(false);

    const updateChanges: ((evidence: { file?: FileList }, key: string) => Promise<void>) = async (
      evidence: { file?: FileList }, key: string): Promise<void> => {
      const { file } = evidence;

      if (!_.isUndefined(file)) {
        await updateEvidence({ variables: { eventId, evidenceType: key.toUpperCase(), file: file[0] } });
      }
    };

    Promise.all(_.map(values, updateChanges))
      .then(() => {
        refetch()
          .catch();
      })
      .catch();
  };

  const canEdit: boolean = _.includes(["admin", "analyst"], userRole) && data.event.eventStatus !== "CLOSED";
  const showEmpty: boolean = _.isEmpty(data.event.evidence) || isRefetching;

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col md={2} mdOffset={10} xs={12} sm={12}>
            {canEdit ? (
              <Button block={true} onClick={handleEditClick} disabled={updating}>
                <FluidIcon icon="edit" />&nbsp;{translate.t("project.events.evidence.edit")}
              </Button>
            ) : undefined}
          </Col>
        </Row>
        <br />
        {_.isEmpty(data.event.evidence) && _.isEmpty(data.event.evidenceFile) && !isEditing ? (
          <div className={globalStyle.noData}>
            <Glyphicon glyph="picture" />
            <p>{translate.t("project.events.evidence.no_data")}</p>
          </div>
        ) : undefined}
        <GenericForm name="editEvidences" onSubmit={handleUpdate}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              {isEditing ? (
                <Row>
                  <Col md={2} mdOffset={10}>
                    <Button block={true} type="submit" disabled={pristine}>
                      <FluidIcon icon="loading" />&nbsp;{translate.t("search_findings.tab_evidence.update")}
                    </Button>
                  </Col>
                </Row>
              ) : undefined}
              {!_.isEmpty(data.event.evidence) || isEditing ? (
                <EvidenceImage
                  acceptedMimes="image/jpeg,image/gif,image/png"
                  content={showEmpty ? <div /> : `${baseUrl}/${data.event.evidence}`}
                  description="Evidence"
                  isDescriptionEditable={false}
                  isEditing={isEditing}
                  isRemovable={!_.isEmpty(data.event.evidence)}
                  name="image"
                  onClick={openImage}
                  onDelete={removeImage}
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
                  validate={validEventFile}
                />
              ) : undefined}
            </React.Fragment>
          )}</GenericForm>
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
