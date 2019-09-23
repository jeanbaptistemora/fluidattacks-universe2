/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, ControlLabel, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { change, Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import globalStyle from "../../../../styles/global.css";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dateField, textAreaField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { isLowerDate, isValidDateAccessToken, required } from "../../../../utils/validations";
import { EditableField } from "../EditableField";
import { GenericForm } from "../GenericForm/index";
import { GET_ACCESS_TOKEN, INVALIDATE_ACCESS_TOKEN_MUTATION, UPDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import { IAccessTokenAttr, IGetAccessTokenAttr, IInvalidateAccessTokenAttr, IUpdateAccessTokenAttr } from "./types";

export interface IAddAccessTokenModalProps {
  expirationTime?: string;
  open: boolean;
  onClose(): void;
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
            const handleMtInvalidateTokenRes: ((mtResult: IInvalidateAccessTokenAttr) => void) =
            (mtResult: IInvalidateAccessTokenAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.invalidateAccessToken.success) {
                  props.onClose();

                  hidePreloader();
                  msgSuccess(
                    translate.t("update_access_token.delete"),
                    translate.t("update_access_token.invalidated"),
                  );
                }
              }
            };
            const handleCloseModal: (() => void) = (): void => { props.onClose(); };

            return (
              <Mutation mutation={INVALIDATE_ACCESS_TOKEN_MUTATION} onCompleted={handleMtInvalidateTokenRes}>
              { (invalidateAccessToken: MutationFn<IInvalidateAccessTokenAttr, {}>,
                 mutationRes: MutationResult): React.ReactNode => {

                  if (mutationRes.loading) {
                    showPreloader();
                  }
                  if (!_.isUndefined(mutationRes.error)) {
                    hidePreloader();
                    handleGraphQLErrors("An error occurred invalidating access token", mutationRes.error);

                    return <React.Fragment/>;
                  }

                  const handleInvalidateAccessToken: (() => void) = (): void => {
                      invalidateAccessToken()
                        .catch();
                    };

                  return (
                  <React.Fragment>
                    <ButtonToolbar className="pull-left">
                      {data.me.accessToken ?
                      <Button bsStyle="default" onClick={handleInvalidateAccessToken}>
                        {translate.t("update_access_token.invalidate")}
                      </Button>
                      : undefined }
                    </ButtonToolbar>
                    <ButtonToolbar className="pull-right">
                      <Button bsStyle="default" onClick={handleCloseModal}>
                        {translate.t("update_access_token.close")}
                      </Button>
                      <Button bsStyle="primary" type="submit">
                        {translate.t("confirmmodal.proceed")}
                      </Button>
                    </ButtonToolbar>
                  </React.Fragment>
                  );
                }}
                </Mutation>
            );
          }
        }}
    </Query>
);

const renderAccessTokenForm: ((props: IAddAccessTokenModalProps) => JSX.Element) =
  (props: IAddAccessTokenModalProps): JSX.Element => {
      const handleMtUpdateTokenRes: ((mtResult: IUpdateAccessTokenAttr) => void) =
      (mtResult: IUpdateAccessTokenAttr): void => {
        if (!_.isUndefined(mtResult)) {
          if (mtResult.updateAccessToken.success) {
            hidePreloader();
            store.dispatch(change("updateAccessToken", "sessionJwt", mtResult.updateAccessToken.sessionJwt));
            msgSuccess(
              translate.t("update_access_token.successfully"),
              translate.t("update_access_token.success"),
            );
          }
        }
      };

      return (
        <Mutation mutation={UPDATE_ACCESS_TOKEN_MUTATION} onCompleted={handleMtUpdateTokenRes}>
        { (updateAccessToken: MutationFn<IUpdateAccessTokenAttr, {expirationTime: number}>,
           mutationRes: MutationResult): React.ReactNode => {

            if (mutationRes.loading) {
              showPreloader();
            }
            if (!_.isUndefined(mutationRes.error)) {
              hidePreloader();
              handleGraphQLErrors("An error occurred adding access token", mutationRes.error);

              return <React.Fragment/>;
            }

            const handleUpdateAccessToken: ((values: IAccessTokenAttr) => void) =
              (values: IAccessTokenAttr): void => {
                const expirationTimeStamp: number = Math.floor(new Date(values.expirationTime).getTime() / 1000);
                updateAccessToken({
                  variables: { expirationTime: expirationTimeStamp },
                  })
                  .catch();
              };

            return (
              <GenericForm name="updateAccessToken" onSubmit={handleUpdateAccessToken} >
                 {({ submitSucceeded }: InjectedFormProps): JSX.Element => (
                  <React.Fragment>
                    <Row>
                      <Col md={12}>
                        <EditableField
                          component={dateField}
                          currentValue=""
                          label={translate.t("update_access_token.expiration_time")}
                          name="expirationTime"
                          renderAsEditable={true}
                          type="date"
                          validate={[isLowerDate, isValidDateAccessToken, required]}
                        />
                     </Col>
                    </Row>
                    { submitSucceeded ?
                    <Row>
                      <Col md={12}>
                        <ControlLabel>
                          <b>{translate.t("update_access_token.access_token")}</b>
                        </ControlLabel>
                        <Field
                          name="sessionJwt"
                          type="text"
                          className={globalStyle.noResize}
                          component={textAreaField}
                          disabled={false}
                          rows="7"
                        />
                      </Col>
                    </Row>
                    : undefined }
                    {renderFooter(props)}
                  </React.Fragment>
                 )}
              </GenericForm>
              );
          }}
        </Mutation>
      );
  };

export const updateAccessTokenModal: React.FC<IAddAccessTokenModalProps> =
  (props: IAddAccessTokenModalProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.open}
          headerTitle={translate.t("update_access_token.title")}
          content={renderAccessTokenForm(props)}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
