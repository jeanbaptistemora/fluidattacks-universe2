/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */
import _ from "lodash";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { ButtonToolbar, FormGroup } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dateField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { isLowerDate, isValidDateAccessToken, required } from "../../../../utils/validations";
import { EditableField } from "../EditableField";
import { GenericForm } from "../GenericForm/index";
import { GET_ACCESS_TOKEN } from "./queries";
import { IGetAccessTokenAttr } from "./types";

export interface IAddAccessTokenModalProps {
  expirationTime?: string;
  open: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}
const handleQryResult: ((qrResult: IGetAccessTokenAttr) => void) = (qrResult: IGetAccessTokenAttr): void => {
  hidePreloader();
};

const renderFooter: ((props: IAddAccessTokenModalProps) => JSX.Element) =
  (props: IAddAccessTokenModalProps): JSX.Element => (
    <Query query={GET_ACCESS_TOKEN} fetchPolicy="network-only" onCompleted={handleQryResult}>
      {
        ({loading, error, data}: QueryResult<IGetAccessTokenAttr>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting access token", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {

            return (
              <React.Fragment>
                <ButtonToolbar className="pull-right">
                  {data.me.accessToken ?
                  <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
                    {translate.t("update_access_token.invalidate")}
                  </Button>
                  : undefined }
                  <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
                    {translate.t("confirmmodal.cancel")}
                  </Button>
                  <Button bsStyle="primary" type="submit">
                    {translate.t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </React.Fragment>
            );
          }
        }}
    </Query>
);

const renderAccessTokenForm: ((props: IAddAccessTokenModalProps) => JSX.Element) =
  (props: IAddAccessTokenModalProps): JSX.Element => {
      const handleProceedClick: ((values: {}) => void) = (values: {}): void => { props.onSubmit(values); };

      return (
      <GenericForm name="updateAccessToken" onSubmit={handleProceedClick}>
        <FormGroup>
            <EditableField
              component={dateField}
              currentValue={!_.isUndefined(props.expirationTime) ? props.expirationTime : ""}
              label={translate.t("update_access_token.expiration_time")}
              name="expirationTime"
              renderAsEditable={true}
              type="date"
              validate={[isLowerDate, isValidDateAccessToken, required]}
            />
          </FormGroup>
        {renderFooter(props)}
      </GenericForm>);
  };

export const updateAccessTokenModal: React.FC<IAddAccessTokenModalProps> =
  (props: IAddAccessTokenModalProps): JSX.Element => (
    <React.StrictMode>

        <Modal
          open={props.open}
          headerTitle={translate.t("update_access_token.title")}
          content={renderAccessTokenForm(props)}
          footer={<div />}
        />

    </React.StrictMode>
  );
