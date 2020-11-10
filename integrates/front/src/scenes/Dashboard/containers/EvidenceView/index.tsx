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
import { Glyphicon } from "react-bootstrap";
import { useParams } from "react-router";
import { InjectedFormProps, Validator } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { evidenceImage as EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import styles from "scenes/Dashboard/containers/EvidenceView/index.css";
import {
  GET_FINDING_EVIDENCES, REMOVE_EVIDENCE_MUTATION, UPDATE_DESCRIPTION_MUTATION, UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/EvidenceView/queries";
import { default as globalStyle } from "styles/global.css";
import { ButtonToolbarRow, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { isValidFileSize, validEvidenceImage } from "utils/validations";

const evidenceView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingEvidence", { User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const [lightboxIndex, setLightboxIndex] = React.useState(-1);

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery(GET_FINDING_EVIDENCES, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
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
        msgError(translate.t("group_alerts.error_textsad"));
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
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating finding evidence", updateError);
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
            msgError(translate.t("group.events.form.wrong_image_type"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating finding evidence", updateError);
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

  const maxFileSize: Validator = isValidFileSize(15);

  return (
    <React.StrictMode>
      <ButtonToolbarRow>
        <Can do="backend_api_mutations_update_evidence_mutate">
          <Button onClick={handleEditClick}>
            <FluidIcon icon="edit" />&nbsp;{translate.t("group.findings.evidence.edit")}
          </Button>
        </Can>
      </ButtonToolbarRow>
      <br />
      {_.isEmpty(evidenceList)
        ? (
          <div className={globalStyle.noData}>
            <Glyphicon glyph="picture" />
            <p>{translate.t("group.findings.evidence.no_data")}</p>
          </div>
        )
        : (
          <GenericForm name="editEvidences" onSubmit={handleUpdate} initialValues={evidenceImages}>
            {({ pristine }: InjectedFormProps): JSX.Element => (
              <React.Fragment>
                {isEditing ? (
                  <ButtonToolbarRow>
                    <Button type="submit" disabled={pristine}>
                      <FluidIcon icon="loading" />&nbsp;{translate.t("search_findings.tab_evidence.update")}
                    </Button>
                  </ButtonToolbarRow>
                ) : undefined}
                <Row className={styles.evidenceGrid}>
                  {evidenceList.map((name: string, index: number): JSX.Element => {
                    const evidence: IEvidenceItem = evidenceImages[name];

                    const handleRemove: (() => void) = (): void => {
                      mixpanel.track("RemoveEvidence", { User: userName });
                      setEditing(false);
                      void removeEvidence({ variables: { evidenceId: name.toUpperCase(), findingId } });
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
