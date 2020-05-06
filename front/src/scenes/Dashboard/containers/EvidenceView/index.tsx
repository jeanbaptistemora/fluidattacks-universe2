/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { ExecutionResult } from "@apollo/react-common";
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { InjectedFormProps, Validator } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidFileSize, validEvidenceImage } from "../../../../utils/validations";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import { EvidenceLightbox } from "../../components/EvidenceLightbox";
import { GenericForm } from "../../components/GenericForm";
import styles from "./index.css";
import {
  GET_FINDING_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_DESCRIPTION_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "./queries";

type EventEvidenceProps = RouteComponentProps<{ findingId: string }>;

const evidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { findingId } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

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
  const { data, networkStatus, refetch } = useQuery(GET_FINDING_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred loading finding evidences", error);
    },
    variables: { findingId },
  });
  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, { onCompleted: refetch });
  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION);
  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid File Size":
            msgError(translate.t("validations.file_size", { count: 10 }));
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

  const handleUpdate: ((values: Dictionary<IEvidenceItem>) => void) = async (
    values: Dictionary<IEvidenceItem>,
  ): Promise<void> => {
    setEditing(false);

    const updateChanges: ((evidence: IEvidenceItem & { file?: FileList }, key: string) => Promise<void>) = async (
      evidence: IEvidenceItem & { file?: FileList }, key: string): Promise<void> => {
      const { description, file } = evidence;
      const descriptionChanged: boolean = description !== evidenceImages[key].description;

      if (file !== undefined) {
        const mtResult: ExecutionResult = await updateEvidence({
          variables: { evidenceId: key.toUpperCase(), file: file[0], findingId },
        });
        const { success } = (mtResult as { data: { updateEvidence: { success: boolean } } }).data.updateEvidence;

        if (success && descriptionChanged) {
          await updateDescription({ variables: { description, evidenceId: key.toUpperCase(), findingId } });
        }
      } else {
        if (descriptionChanged) {
          await updateDescription({ variables: { description, evidenceId: key.toUpperCase(), findingId } });
        }
      }
    };

    await Promise.all(_.map(values, updateChanges));
    setLightboxIndex(-1);
    await refetch();
  };

  const maxFileSize: Validator = isValidFileSize(10);

  return (
    <React.StrictMode>
      <Row>
        <Col md={2} mdOffset={10} xs={12} sm={12}>
          <Can do="backend_api_resolvers_finding__do_update_evidence">
            <Button block={true} onClick={handleEditClick}>
              <FluidIcon icon="edit" />&nbsp;{translate.t("project.findings.evidence.edit")}
            </Button>
          </Can>
        </Col>
      </Row>
      <br />
      {_.isEmpty(evidenceList)
        ? (
          <div className={globalStyle.noData}>
            <Glyphicon glyph="picture" />
            <p>{translate.t("project.findings.evidence.no_data")}</p>
          </div>
        )
        : (
          <GenericForm name="editEvidences" onSubmit={handleUpdate} initialValues={evidenceImages}>
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
                <Row className={styles.evidenceGrid}>
                  {evidenceList.map((name: string, index: number): JSX.Element => {
                    const evidence: IEvidenceItem = evidenceImages[name];

                    const handleRemove: (() => void) = (): void => {
                      mixpanel.track("RemoveEvidence", { Organization: userOrganization, User: userName });
                      setEditing(false);
                      removeEvidence({ variables: { evidenceId: name.toUpperCase(), findingId } })
                        .catch();
                    };

                    const openImage: (() => void) = (): void => {
                      if (!isEditing && !isRefetching) { setLightboxIndex(index); }
                    };

                    const showEmpty: boolean = _.isEmpty(evidence.url) || isRefetching;

                    return (
                      <EvidenceImage
                        acceptedMimes="image/jpeg,image/gif,image/png"
                        content={showEmpty ? <div /> : `${location.href}/${evidence.url}`}
                        description={evidence.description}
                        isDescriptionEditable={index > 1}
                        isEditing={isEditing}
                        isRemovable={!_.isEmpty(evidence.url)}
                        key={index}
                        name={name}
                        onClick={openImage}
                        onDelete={handleRemove}
                        validate={[validEvidenceImage, maxFileSize]}
                      />
                    );
                  })}
                </Row>
              </React.Fragment>
            )}
          </GenericForm>
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
