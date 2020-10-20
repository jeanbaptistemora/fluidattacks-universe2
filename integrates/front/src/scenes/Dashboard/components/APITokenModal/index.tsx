import { Button } from "components/Button";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Modal } from "components/Modal";
import { MutationFunction } from "@apollo/react-common";
import React from "react";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbar,
  ButtonToolbarLeft,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Date as DateField, TextArea } from "utils/forms/fields";
import { Field, InjectedFormProps } from "redux-form";
import {
  IAccessTokenAttr,
  IGetAccessTokenDictAttr,
} from "scenes/Dashboard/components/APITokenModal/types";
import {
  isLowerDate,
  isValidDateAccessToken,
  required,
} from "utils/validations";
import { msgError, msgSuccess } from "utils/notifications";
import {
  useGetAPIToken,
  useInvalidateAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/APITokenModal/hooks";

interface IAPITokenModalProps {
  open: boolean;
  onClose: () => void;
}

const APITokenModal: React.FC<IAPITokenModalProps> = (
  props: IAPITokenModalProps
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
    <Modal headerTitle={translate.t("update_access_token.title")} open={open}>
      <GenericForm name={"updateAccessToken"} onSubmit={handleUpdateAPIToken}>
        {({ submitSucceeded }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <Row>
              <Col100>
                {!hasAPIToken && (
                  <FormGroup>
                    <ControlLabel>
                      <b>
                        {translate.t("update_access_token.expiration_time")}
                      </b>
                    </ControlLabel>
                    <Field
                      component={DateField}
                      name={"expirationTime"}
                      type={"date"}
                      validate={[isLowerDate, isValidDateAccessToken, required]}
                    />
                  </FormGroup>
                )}
              </Col100>
            </Row>
            {submitSucceeded && (
              <Row>
                <Col100>
                  <ControlLabel>
                    <b>{translate.t("update_access_token.message")}</b>
                  </ControlLabel>
                  <ControlLabel>
                    <b>{translate.t("update_access_token.access_token")}</b>
                  </ControlLabel>
                  <Field
                    //Allow to block resizing the TextArea
                    //eslint-disable-next-line react/forbid-component-props
                    className={"noresize"}
                    component={TextArea}
                    disabled={true}
                    name={"sessionJwt"}
                    rows={"7"}
                    type={"text"}
                  />
                  <Button onClick={handleCopy}>
                    {translate.t("update_access_token.copy.copy")}
                  </Button>
                </Col100>
              </Row>
            )}
            <Row>
              {!submitSucceeded && hasAPIToken && (
                <Col100>
                  <ControlLabel>
                    <b>{translate.t("update_access_token.token_created")}</b>
                    &nbsp;
                    {new Date(Number.parseInt(issuedAt, 10) * msToSec)
                      .toISOString()
                      .substring(0, yyyymmdd)}
                  </ControlLabel>
                </Col100>
              )}
            </Row>
            <ButtonToolbarLeft>
              {!submitSucceeded && hasAPIToken && (
                <Button onClick={handleInvalidateAPIToken}>
                  {translate.t("update_access_token.invalidate")}
                </Button>
              )}
            </ButtonToolbarLeft>
            <ButtonToolbar>
              <Button onClick={onClose}>
                {translate.t("update_access_token.close")}
              </Button>
              <Button disabled={hasAPIToken} type={"submit"}>
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { IAPITokenModalProps, APITokenModal };
