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
import { useUpdateAPIToken } from "./hooks";
import {
  ButtonToolbar,
  Col,
  ControlLabel,
  FormGroup,
  Row,
} from "react-bootstrap";
import { Date as DateField, TextArea } from "../../../../utils/forms/fields";
import { Field, InjectedFormProps, reset } from "redux-form";
import { GET_ACCESS_TOKEN, INVALIDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import {
  IAccessTokenAttr,
  IGetAccessTokenAttr,
  IGetAccessTokenDictAttr,
  IInvalidateAccessTokenAttr,
} from "./types";
import { Mutation, Query } from "@apollo/react-components";
import { MutationFunction, QueryResult } from "@apollo/react-common";
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

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  const {
    canSubmit: [canSubmit, setCanSubmit],
    canSelectDate: [canSelectDate, setCanSelectDate],
    mtResult: [updateAPIToken, mtResponse],
  } = useUpdateAPIToken();
  function handleUpdateAPIToken(values: IAccessTokenAttr): void {
    const expTimeStamp: number = Math.floor(
      new Date(values.expirationTime).getTime() / msToSec
    );
    void updateAPIToken({
      variables: { expirationTime: expTimeStamp },
    });
  }

  async function handleCopy(): Promise<void> {
    const clipboard: Clipboard = navigator.clipboard;

    if (!_.isUndefined(clipboard)) {
      await clipboard.writeText(
        mtResponse.data?.updateAccessToken.sessionJwt ?? ""
      );
      document.execCommand("copy");
      msgSuccess(
        translate.t("update_access_token.copy.successfully"),
        translate.t("update_access_token.copy.success")
      );
    } else {
      msgError(translate.t("update_access_token.copy.failed"));
    }
  }

  function handleQryResult(qrResult: IGetAccessTokenAttr): void {
    const accessToken: IGetAccessTokenDictAttr = JSON.parse(
      qrResult.me.accessToken
    );
    if (accessToken.hasAccessToken) {
      setCanSubmit(true);
      setCanSelectDate(false);
    } else {
      setCanSubmit(false);
    }
  }
  function handleQueryErrors({ graphQLErrors }: ApolloError): void {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred getting access token", error);
      msgError(translate.t("group_alerts.error_textsad"));
    });
  }

  return (
    <Modal
      footer={<div />}
      headerTitle={translate.t("update_access_token.title")}
      open={open}
    >
      <GenericForm name={"updateAccessToken"} onSubmit={handleUpdateAPIToken}>
        {({ submitSucceeded }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <Row>
              <Col md={12}>
                {canSelectDate && (
                  <FormGroup>
                    <ControlLabel>
                      <b>
                        {translate.t("update_access_token.expiration_time")}
                      </b>
                    </ControlLabel>
                    <br />
                    <Field
                      component={DateField}
                      name={"expirationTime"}
                      type={"date"}
                      validate={[isLowerDate, isValidDateAccessToken, required]}
                    />
                  </FormGroup>
                )}
              </Col>
            </Row>
            {submitSucceeded && (
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
            )}
            <Query
              fetchPolicy={"network-only"}
              onCompleted={handleQryResult}
              onError={handleQueryErrors}
              query={GET_ACCESS_TOKEN}
            >
              {({ data }: QueryResult<IGetAccessTokenAttr>): JSX.Element => {
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
                      setCanSelectDate(true);
                    }
                  }
                }
                function handleCloseModal(): void {
                  props.onClose();
                  setCanSelectDate(true);
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
                                {translate.t("update_access_token.invalidate")}
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
                              disabled={canSubmit}
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
    </Modal>
  );
};

export { IAddAccessTokenModalProps, UpdateAccessTokenModal };
