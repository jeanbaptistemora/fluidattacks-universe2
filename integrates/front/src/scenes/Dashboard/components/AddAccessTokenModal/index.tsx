/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
*/
import { ApolloError } from "apollo-client";
import { Button } from "../../../../components/Button";
import { GenericForm } from "../GenericForm";
import { GraphQLError } from "graphql";
import { Logger } from "../../../../utils/logger";
import { Modal } from "../../../../components/Modal";
import React from "react";
import _ from "lodash";
import globalStyle from "../../../../styles/global.css";
import store from "../../../../store";
import { translate } from "../../../../utils/translations/translate";
import {
  ButtonToolbar,
  Col,
  ControlLabel,
  FormGroup,
  Row,
} from "react-bootstrap";
import { Date as DateField, TextArea } from "../../../../utils/forms/fields";
import { Field, InjectedFormProps, change, reset } from "redux-form";
import {
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
  UPDATE_ACCESS_TOKEN_MUTATION,
} from "./queries";
import {
  IAccessTokenAttr,
  IGetAccessTokenAttr,
  IGetAccessTokenDictAttr,
  IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr,
} from "./types";
import { Mutation, Query } from "@apollo/react-components";
import {
  MutationFunction,
  MutationResult,
  QueryResult,
} from "@apollo/react-common";
import {
  isLowerDate,
  isValidDateAccessToken,
  required,
} from "../../../../utils/validations";
import { msgError, msgSuccess } from "../../../../utils/notifications";

interface IAddAccessTokenModalProps {
  open: boolean;
  onClose: () => void;
}

const UpdateAccessTokenModal: React.FC<IAddAccessTokenModalProps> = (
  props: IAddAccessTokenModalProps
): JSX.Element => {
  const { open } = props;
  const [buttonDisable, setButtonDisable] = React.useState(false);
  const [dateSelectorVisibility, setDateSelectorVisibility] = React.useState(
    true
  );
  function handleMtUpdateTokenRes(mtResult: IUpdateAccessTokenAttr): void {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateAccessToken.success) {
        setButtonDisable(true);
        setDateSelectorVisibility(false);
        store.dispatch(
          change(
            "updateAccessToken",
            "sessionJwt",
            mtResult.updateAccessToken.sessionJwt
          )
        );
        msgSuccess(
          translate.t("update_access_token.successfully"),
          translate.t("update_access_token.success")
        );
      }
    }
  }

  function handleMtUpdateTokenErr({ graphQLErrors }: ApolloError): void {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Invalid Expiration Time":
          msgError(translate.t("update_access_token.invalid_exp_time"));
          break;
        default:
          Logger.warning("An error occurred adding access token", error);
          msgError(translate.t("group_alerts.error_textsad"));
      }
    });
    store.dispatch(reset("updateAccessToken"));
  }

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  return (
    <Modal
      footer={<div />}
      headerTitle={translate.t("update_access_token.title")}
      open={open}
    >
      <Mutation
        mutation={UPDATE_ACCESS_TOKEN_MUTATION}
        onCompleted={handleMtUpdateTokenRes}
        onError={handleMtUpdateTokenErr}
      >
        {(
          updateAccessToken: MutationFunction,
          mutationRes: MutationResult<{
            updateAccessToken: { sessionJwt: string };
          }>
        ): JSX.Element => {
          function handleUpdateAccessToken(values: IAccessTokenAttr): void {
            const expirationTimeStamp: number = Math.floor(
              new Date(values.expirationTime).getTime() / msToSec
            );
            void updateAccessToken({
              variables: { expirationTime: expirationTimeStamp },
            });
          }

          function handleCopy(): void {
            const clipboard: Clipboard = navigator.clipboard;

            return !_.isUndefined(clipboard)
              ? void clipboard
                  .writeText(
                    !_.isUndefined(mutationRes.data)
                      ? mutationRes.data.updateAccessToken.sessionJwt
                      : ""
                  )
                  .then((): void => {
                    document.execCommand("copy");
                    msgSuccess(
                      translate.t("update_access_token.copy.successfully"),
                      translate.t("update_access_token.copy.success")
                    );
                  })
              : msgError(translate.t("update_access_token.copy.failed"));
          }

          function handleQryResult(qrResult: IGetAccessTokenAttr): void {
            const accessToken: IGetAccessTokenDictAttr = JSON.parse(
              qrResult.me.accessToken
            );
            if (accessToken.hasAccessToken) {
              setButtonDisable(true);
              setDateSelectorVisibility(false);
            } else {
              setButtonDisable(false);
            }
          }

          function handleQueryErrors({ graphQLErrors }: ApolloError): void {
            graphQLErrors.forEach((error: GraphQLError): void => {
              Logger.warning("An error occurred getting access token", error);
              msgError(translate.t("group_alerts.error_textsad"));
            });
          }

          return (
            <GenericForm
              name={"updateAccessToken"}
              onSubmit={handleUpdateAccessToken}
            >
              {({ submitSucceeded }: InjectedFormProps): JSX.Element => (
                <React.Fragment>
                  <Row>
                    <Col md={12}>
                      {dateSelectorVisibility ? (
                        <FormGroup>
                          <ControlLabel>
                            <b>
                              {translate.t(
                                "update_access_token.expiration_time"
                              )}
                            </b>
                          </ControlLabel>
                          <br />
                          <Field
                            component={DateField}
                            name={"expirationTime"}
                            type={"date"}
                            validate={[
                              isLowerDate,
                              isValidDateAccessToken,
                              required,
                            ]}
                          />
                        </FormGroup>
                      ) : undefined}
                    </Col>
                  </Row>
                  {submitSucceeded ? (
                    <Row>
                      <Col md={12}>
                        <ControlLabel>
                          <b>{translate.t("update_access_token.message")}</b>
                        </ControlLabel>
                        <ControlLabel>
                          <br />
                          <b>
                            {translate.t("update_access_token.access_token")}
                          </b>
                        </ControlLabel>
                        <Field
                          className={globalStyle.noResize}
                          component={TextArea}
                          disabled={true}
                          name={"sessionJwt"}
                          rows={"7"}
                          type={"text"}
                        />
                        <Button bsStyle={"default"} onClick={handleCopy}>
                          {translate.t("update_access_token.copy.copy")}
                        </Button>
                      </Col>
                    </Row>
                  ) : undefined}
                  <Query
                    fetchPolicy={"network-only"}
                    onCompleted={handleQryResult}
                    onError={handleQueryErrors}
                    query={GET_ACCESS_TOKEN}
                  >
                    {({
                      data,
                    }: QueryResult<IGetAccessTokenAttr>): JSX.Element => {
                      if (_.isUndefined(data) || _.isEmpty(data)) {
                        // temporal
                        // eslint-disable-next-line react/jsx-no-useless-fragment
                        return <React.Fragment />;
                      }

                      function handleMtInvalidateTokenRes(
                        mtResult: IInvalidateAccessTokenAttr
                      ): void {
                        if (!_.isUndefined(mtResult)) {
                          if (mtResult.invalidateAccessToken.success) {
                            props.onClose();
                            msgSuccess(
                              translate.t("update_access_token.delete"),
                              translate.t("update_access_token.invalidated")
                            );
                            setDateSelectorVisibility(true);
                          }
                        }
                      }
                      function handleCloseModal(): void {
                        props.onClose();
                        setDateSelectorVisibility(true);
                      }

                      function handleMtInvalidateErrors({
                        graphQLErrors,
                      }: ApolloError): void {
                        graphQLErrors.forEach((error: GraphQLError): void => {
                          Logger.warning(
                            "An error occurred invalidating access token",
                            error
                          );
                          msgError(translate.t("group_alerts.error_textsad"));
                        });
                        store.dispatch(reset("updateAccessToken"));
                      }

                      return (
                        <Mutation
                          mutation={INVALIDATE_ACCESS_TOKEN_MUTATION}
                          onCompleted={handleMtInvalidateTokenRes}
                          onError={handleMtInvalidateErrors}
                        >
                          {(
                            invalidateAccessToken: MutationFunction<
                              IInvalidateAccessTokenAttr,
                              Record<string, unknown>
                            >
                          ): JSX.Element => {
                            function handleInvalidateAccessToken(): void {
                              void invalidateAccessToken();
                            }
                            const accessToken: IGetAccessTokenDictAttr = JSON.parse(
                              data.me.accessToken
                            );

                            return (
                              <React.Fragment>
                                <Row>
                                  {accessToken.hasAccessToken ? (
                                    <Col md={12}>
                                      {!_.isEmpty(accessToken.issuedAt) ? (
                                        <ControlLabel>
                                          <b>
                                            {translate.t(
                                              "update_access_token.token_created"
                                            )}
                                          </b>
                                          &nbsp;
                                          {new Date(
                                            Number.parseInt(
                                              accessToken.issuedAt,
                                              10
                                            ) * msToSec
                                          )
                                            .toISOString()
                                            .substring(0, yyyymmdd)}
                                        </ControlLabel>
                                      ) : undefined}
                                    </Col>
                                  ) : undefined}
                                </Row>
                                <ButtonToolbar className={"pull-left"}>
                                  <br />
                                  {accessToken.hasAccessToken ? (
                                    <Button
                                      bsStyle={"default"}
                                      onClick={handleInvalidateAccessToken}
                                    >
                                      {translate.t(
                                        "update_access_token.invalidate"
                                      )}
                                    </Button>
                                  ) : undefined}
                                </ButtonToolbar>
                                <ButtonToolbar className={"pull-right"}>
                                  <br />
                                  <Button
                                    bsStyle={"default"}
                                    onClick={handleCloseModal}
                                  >
                                    {translate.t("update_access_token.close")}
                                  </Button>
                                  <Button
                                    bsStyle={"primary"}
                                    disabled={buttonDisable}
                                    type={"submit"}
                                  >
                                    {translate.t("confirmmodal.proceed")}
                                  </Button>
                                </ButtonToolbar>
                              </React.Fragment>
                            );
                          }}
                        </Mutation>
                      );
                    }}
                  </Query>
                </React.Fragment>
              )}
            </GenericForm>
          );
        }}
      </Mutation>
    </Modal>
  );
};

export { IAddAccessTokenModalProps, UpdateAccessTokenModal };
