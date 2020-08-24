/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
*/
import { Button } from "../../../../components/Button";
import { GenericForm } from "../GenericForm";
import { Modal } from "../../../../components/Modal";
import { MutationFunction } from "@apollo/react-common";
import React from "react";
import _ from "lodash";
import globalStyle from "../../../../styles/global.css";
import { translate } from "../../../../utils/translations/translate";
import {
  ButtonToolbar,
  Col,
  ControlLabel,
  FormGroup,
  Row,
} from "react-bootstrap";
import { Date as DateField, TextArea } from "../../../../utils/forms/fields";
import { Field, InjectedFormProps } from "redux-form";
import { IAccessTokenAttr, IGetAccessTokenDictAttr } from "./types";
import {
  isLowerDate,
  isValidDateAccessToken,
  required,
} from "../../../../utils/validations";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import {
  useGetAPIToken,
  useInvalidateAPIToken,
  useUpdateAPIToken,
} from "./hooks";

interface IAddAccessTokenModalProps {
  open: boolean;
  onClose: () => void;
}

const UpdateAccessTokenModal: React.FC<IAddAccessTokenModalProps> = (
  props: IAddAccessTokenModalProps
): JSX.Element => {
  const { open, onClose } = props;

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  const [data, refetch] = useGetAPIToken();
  const accessToken: IGetAccessTokenDictAttr | undefined = _.isUndefined(data)
    ? undefined
    : JSON.parse(data.me.accessToken);
  const hasAPIToken: boolean = accessToken?.hasAccessToken ?? false;
  const issuedAt: string = accessToken?.issuedAt ?? "0";

  const [updateAPIToken, mtResponse] = useUpdateAPIToken(refetch);
  function handleUpdateAPIToken(values: IAccessTokenAttr): void {
    const expTimeStamp: number = Math.floor(
      new Date(values.expirationTime).getTime() / msToSec
    );
    void updateAPIToken({
      variables: { expirationTime: expTimeStamp },
    });
  }

  const invalidateAPIToken: MutationFunction = useInvalidateAPIToken(
    refetch,
    onClose
  );
  function handleInvalidateAPIToken(): void {
    void invalidateAPIToken();
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
                {!hasAPIToken && (
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
            <Row>
              {!submitSucceeded && hasAPIToken && (
                <Col md={12}>
                  <ControlLabel>
                    <b>{translate.t("update_access_token.token_created")}</b>
                    &nbsp;
                    {new Date(Number.parseInt(issuedAt, 10) * msToSec)
                      .toISOString()
                      .substring(0, yyyymmdd)}
                  </ControlLabel>
                </Col>
              )}
            </Row>
            <ButtonToolbar className={"pull-left"}>
              <br />
              {!submitSucceeded && hasAPIToken && (
                <Button bsStyle={"default"} onClick={handleInvalidateAPIToken}>
                  {translate.t("update_access_token.invalidate")}
                </Button>
              )}
            </ButtonToolbar>
            <ButtonToolbar className={"pull-right"}>
              <br />
              <Button bsStyle={"default"} onClick={onClose}>
                {translate.t("update_access_token.close")}
              </Button>
              <Button
                bsStyle={"primary"}
                disabled={hasAPIToken}
                type={"submit"}
              >
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { IAddAccessTokenModalProps, UpdateAccessTokenModal };
