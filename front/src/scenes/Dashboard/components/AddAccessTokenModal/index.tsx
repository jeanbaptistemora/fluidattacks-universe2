/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React, { useState } from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, ControlLabel, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { change, Field, InjectedFormProps, reset } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import globalStyle from "../../../../styles/global.css";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dateField, textAreaField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { isLowerDate, isValidDateAccessToken, required } from "../../../../utils/validations";
import { EditableField } from "../EditableField";
import { GenericForm } from "../GenericForm/index";
import { GET_ACCESS_TOKEN, INVALIDATE_ACCESS_TOKEN_MUTATION, UPDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import { IAccessTokenAttr, IGetAccessTokenAttr, IGetAccessTokenDictAttr, IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr } from "./types";

export interface IAddAccessTokenModalProps {
  expirationTime?: string;
  open: boolean;
  onClose(): void;
}

const renderAccessTokenForm: ((props: IAddAccessTokenModalProps) => JSX.Element) =
  (props: IAddAccessTokenModalProps): JSX.Element => {
      const [buttonDisable, setButtonDisable] = useState(false);
      const [dateSelectorVisibility, setDateSelectorVisibility] = useState(true);
      const handleMtUpdateTokenRes: ((mtResult: IUpdateAccessTokenAttr) => void) =
      (mtResult: IUpdateAccessTokenAttr): void => {
        if (!_.isUndefined(mtResult)) {
          if (mtResult.updateAccessToken.success) {
            hidePreloader();
            setButtonDisable(true);
            setDateSelectorVisibility(false);
            store.dispatch(change("updateAccessToken", "sessionJwt", mtResult.updateAccessToken.sessionJwt));
            msgSuccess(
              translate.t("update_access_token.successfully"),
              translate.t("update_access_token.success"),
            );
          }
        }
      };

      const handleMtUpdateTokenErr: ((mtError: ApolloError) => void) =
      (mtResult: ApolloError): void => {
        if (!_.isUndefined(mtResult)) {
          hidePreloader();
          handleGraphQLErrors("An error occurred adding access token", mtResult);
          store.dispatch(reset("updateAccessToken"));
        }
      };

      return (
        <Mutation
          mutation={UPDATE_ACCESS_TOKEN_MUTATION}
          onCompleted={handleMtUpdateTokenRes}
          onError={handleMtUpdateTokenErr}
        >
        { (updateAccessToken: MutationFn<IUpdateAccessTokenAttr, {expirationTime: number}>,
           mutationRes: MutationResult): React.ReactNode => {

            if (mutationRes.loading) {
              showPreloader();
            }

            const handleUpdateAccessToken: ((values: IAccessTokenAttr) => void) =
              (values: IAccessTokenAttr): void => {
                const expirationTimeStamp: number = Math.floor(new Date(values.expirationTime).getTime() / 1000);
                updateAccessToken({
                  variables: { expirationTime: expirationTimeStamp },
                  })
                  .catch();
              };

            const handleCopy: (() => void) = (): void => {
              !_.isUndefined(navigator.clipboard) ?
              navigator.clipboard.writeText(!_.isUndefined(mutationRes.data) ?
              mutationRes.data.updateAccessToken.sessionJwt : "")
              .then(() => {
                document.execCommand("copy");
                msgSuccess(
                  translate.t("update_access_token.copy.successfully"),
                  translate.t("update_access_token.copy.success"),
                );
              })
              /* tslint:disable-next-line: no-void-expression
               * NO-VOID-EXPRESSION: Disabling this rule is necessary because msgError is void type
               * and is necessary to show an error message when the browser has undefined or disable
               * clipboard's events
               */
              .catch() : msgError(translate.t("update_access_token.copy.failed"));
            };

            const handleQryResult: ((qrResult: IGetAccessTokenAttr) => void) =
            (qrResult: IGetAccessTokenAttr): void => {
              const accessToken: IGetAccessTokenDictAttr = JSON.parse(qrResult.me.accessToken);
              if (accessToken.hasAccessToken) {
                setButtonDisable(true);
                setDateSelectorVisibility(false);
              } else {
                setButtonDisable(false);
              }
              hidePreloader();
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
                          visible={dateSelectorVisibility}
                          validate={[isLowerDate, isValidDateAccessToken, required]}
                        />
                     </Col>
                    </Row>
                    { submitSucceeded ?
                    <Row>
                      <Col md={12}>
                        <ControlLabel>
                          <b>{translate.t("update_access_token.message")}</b>
                        </ControlLabel>
                        <ControlLabel>
                          <br />
                          <b>{translate.t("update_access_token.access_token")}</b>
                        </ControlLabel>
                        <Field
                          name="sessionJwt"
                          type="text"
                          className={globalStyle.noResize}
                          component={textAreaField}
                          disabled={true}
                          rows="7"
                        />
                        <Button bsStyle="default" onClick={handleCopy}>
                          {translate.t("update_access_token.copy.copy")}
                        </Button>
                      </Col>
                    </Row>
                    : undefined }
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
                                setDateSelectorVisibility(true);
                              }
                            }
                          };
                          const handleCloseModal: (() => void) = (): void => {
                            props.onClose();
                            setDateSelectorVisibility(true);
                          };

                          return (
                            <Mutation
                              mutation={INVALIDATE_ACCESS_TOKEN_MUTATION}
                              onCompleted={handleMtInvalidateTokenRes}
                            >
                            { (invalidateAccessToken: MutationFn<IInvalidateAccessTokenAttr, {}>,
                               mutationResult: MutationResult): React.ReactNode => {

                                if (mutationResult.loading) {
                                  showPreloader();
                                }
                                if (!_.isUndefined(mutationResult.error)) {
                                  hidePreloader();
                                  handleGraphQLErrors("An error occurred invalidating access token",
                                                      mutationResult.error);

                                  return <React.Fragment/>;
                                }

                                const handleInvalidateAccessToken: (() => void) = (): void => {
                                    invalidateAccessToken()
                                      .catch();
                                  };
                                const accessToken: IGetAccessTokenDictAttr = JSON.parse(data.me.accessToken);

                                return (
                                  <React.Fragment>
                                  <Row>
                                    {accessToken.hasAccessToken ?
                                    <Col md={12}>
                                      {!_.isEmpty(accessToken.issuedAt) ?
                                        <ControlLabel>
                                          <b>{translate.t("update_access_token.token_created")}</b>
                                          &nbsp;{new Date(accessToken.issuedAt * 1000).toString()
                                                                                      .substring(0, 15)}
                                        </ControlLabel>
                                      : undefined }
                                  </Col>
                                    : undefined }
                                  </Row>
                                  <ButtonToolbar className="pull-left">
                                    <br />
                                    {accessToken.hasAccessToken ?
                                    <Button bsStyle="default" onClick={handleInvalidateAccessToken}>
                                      {translate.t("update_access_token.invalidate")}
                                    </Button>
                                    : undefined }
                                  </ButtonToolbar>
                                  <ButtonToolbar className="pull-right">
                                    <br />
                                    <Button bsStyle="default" onClick={handleCloseModal}>
                                      {translate.t("update_access_token.close")}
                                    </Button>
                                    <Button bsStyle="primary" disabled={buttonDisable} type="submit">
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
