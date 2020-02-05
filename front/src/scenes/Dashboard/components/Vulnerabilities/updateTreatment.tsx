/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { ApolloError } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult } from "react-apollo";
import { ButtonToolbar } from "react-bootstrap";
import { submit } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import store from "../../../../store";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import TreatmentFieldsView from "../../components/treatmentFields";
import { IDescriptionViewProps } from "../../containers/DescriptionView";
import { GenericForm } from "../GenericForm";
import { DELETE_TAGS_MUTATION, GET_VULNERABILITIES, UPDATE_TREATMENT_MUTATION } from "./queries";
import { IDeleteTagAttr, IDeleteTagResult, IUpdateTreatmentVulnAttr, IUpdateVulnTreatment } from "./types";

export interface IUpdateTreatmentModal {
  descriptParam?: IDescriptionViewProps;
  findingId: string;
  isOpen: boolean;
  numberRowSelected: boolean;
  userRole: string;
  vulnsSelected: string[];
  handleCloseModal(): void;
}

const updateTreatmentModal: ((props: IUpdateTreatmentModal) => JSX.Element) =
(props: IUpdateTreatmentModal): JSX.Element => {
  const canDisplayAnalyst: boolean = _.includes(["analyst", "admin"], props.userRole);
  const handleUpdateTreatError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
    msgError(translate.t("proj_alerts.error_textsad"));
  };
  const handleClose: (() => void) = (): void => { props.handleCloseModal(); };
  const handleUpdateResult: ((mtResult: IUpdateVulnTreatment) => void) = (mtResult: IUpdateVulnTreatment): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateTreatmentVuln.success) {
        mixpanel.track(
          "UpdatedTreatmentVulnerabilities", {
            Organization: (window as typeof window & { userOrganization: string }).userOrganization,
            User: (window as typeof window & { userName: string }).userName,
          });
        msgSuccess(
          translate.t("search_findings.tab_description.update_vulnerabilities"),
          translate.t("proj_alerts.title_success"));
        props.handleCloseModal();
      }
    }
  };

  return(
    <Mutation
      mutation={UPDATE_TREATMENT_MUTATION}
      onCompleted={handleUpdateResult}
      onError={handleUpdateTreatError}
      refetchQueries={[{ query: GET_VULNERABILITIES,
                         variables: { analystField: canDisplayAnalyst, identifier: props.findingId } }]}
    >
      {(updateTreatmentVuln: MutationFn<IUpdateVulnTreatment, IUpdateTreatmentVulnAttr>,
        mutationResVuln: MutationResult): React.ReactNode => {

          const handleUpdateTreatmentVuln: ((dataTreatment: IDescriptionViewProps["dataset"]) => void) =
            (dataTreatment: IDescriptionViewProps["dataset"]): void => {
              if (props.vulnsSelected.length === 0) {
                msgError(translate.t("search_findings.tab_resources.no_selection"));
              } else {
                updateTreatmentVuln({variables: {
                  acceptanceDate: dataTreatment.acceptanceDate,
                  btsUrl: dataTreatment.btsUrl,
                  findingId: props.findingId,
                  severity: !_.isEmpty(dataTreatment.severity) ? dataTreatment.severity : "-1",
                  tag: dataTreatment.tag,
                  treatment: dataTreatment.treatment,
                  treatmentJustification: dataTreatment.justification,
                  treatmentManager: dataTreatment.treatmentManager,
                  vulnerabilities: props.vulnsSelected,
                }})
                .catch();
              }
          };
          const handleEditTreatment: (() => void) = (): void => {
            store.dispatch(submit("editTreatmentVulnerability"));
          };

          const handleUpdateTreatment: ((values: IDescriptionViewProps["dataset"]) => void) =
          (values: IDescriptionViewProps["dataset"]): void => {
            handleUpdateTreatmentVuln(values);
          };
          const handleDeleteError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            msgError(translate.t("proj_alerts.error_textsad"));
          };
          const handleDeleteResult: ((mtResult: IDeleteTagResult) => void) =
          (mtResult: IDeleteTagResult): void => {
            if (!_.isUndefined(mtResult)) {
              if (mtResult.deleteTags.success) {
                msgSuccess(
                  translate.t("search_findings.tab_description.update_vulnerabilities"),
                  translate.t("proj_alerts.title_success"));
                props.handleCloseModal();
              }
            }
          };

          return (
            <Mutation
              mutation={DELETE_TAGS_MUTATION}
              onCompleted={handleDeleteResult}
              onError={handleDeleteError}
              refetchQueries={[{ query: GET_VULNERABILITIES,
                                 variables: { analystField: canDisplayAnalyst, identifier: props.findingId } }]}
            >
            {(deleteTagVuln: MutationFn<IDeleteTagResult, IDeleteTagAttr>,
              mutationResult: MutationResult): React.ReactNode => {
                const handleDeleteTag: (() => void) = (): void => {
                  if (props.vulnsSelected.length === 0) {
                    msgError(translate.t("search_findings.tab_resources.no_selection"));
                  } else {
                    deleteTagVuln({variables: {
                      findingId: props.findingId,
                      vulnerabilities: props.vulnsSelected,
                    }})
                    .catch();
                  }
                };

                return (
                  <Modal
                    open={props.isOpen}
                    footer={
                      <ButtonToolbar className="pull-right">
                        <Button onClick={handleClose}>
                          {translate.t("project.findings.report.modal_close")}
                        </Button>
                        <Button
                          bsStyle="primary"
                          onClick={handleEditTreatment}
                        >
                          {translate.t("confirmmodal.proceed")}
                        </Button>
                      </ButtonToolbar>
                    }
                    headerTitle={translate.t("search_findings.tab_description.editVuln")}
                  >
                  <GenericForm
                    name="editTreatmentVulnerability"
                    onSubmit={handleUpdateTreatment}
                    initialValues={
                      props.numberRowSelected ? (!_.isUndefined(props.descriptParam) ?
                      props.descriptParam.dataset : undefined) : undefined
                    }
                  >
                    {!_.isUndefined(props.descriptParam) ?
                    <TreatmentFieldsView
                      isTreatmentModal={true}
                      onDeleteTag={handleDeleteTag}
                      {...props.descriptParam}
                    />
                    : undefined}
                  </GenericForm>
                  </Modal>
                );
              }}
            </Mutation>
          );
      }}
    </Mutation>
  );
};

export { updateTreatmentModal as UpdateTreatmentModal };
