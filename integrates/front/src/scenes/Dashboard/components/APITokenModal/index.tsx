import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import type { MutationFunction } from "@apollo/react-common";
import React from "react";
import _ from "lodash";
import { track } from "mixpanel-browser";
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
import type {
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
    track("GenerateAPIToken");
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
    const { clipboard } = navigator;

    if (_.isUndefined(clipboard)) {
      msgError(translate.t("updateAccessToken.copy.failed"));
    } else {
      await clipboard.writeText(
        mtResponse.data?.updateAccessToken.sessionJwt ?? ""
      );
      document.execCommand("copy");
      msgSuccess(
        translate.t("updateAccessToken.copy.successfully"),
        translate.t("updateAccessToken.copy.success")
      );
    }
  }

  return (
    <Modal headerTitle={translate.t("updateAccessToken.title")} open={open}>
      <GenericForm name={"updateAccessToken"} onSubmit={handleUpdateAPIToken}>
        {({ submitSucceeded }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <Row>
              <Col100>
                {!hasAPIToken && (
                  <FormGroup>
                    <ControlLabel>
                      <b>{translate.t("updateAccessToken.expirationTime")}</b>
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
                    <b>{translate.t("updateAccessToken.message")}</b>
                  </ControlLabel>
                  <ControlLabel>
                    <b>{translate.t("updateAccessToken.accessToken")}</b>
                  </ControlLabel>
                  <Field
                    // Allow to block resizing the TextArea
                    // eslint-disable-next-line react/forbid-component-props
                    className={"noresize"}
                    component={TextArea}
                    disabled={true}
                    name={"sessionJwt"}
                    rows={"7"}
                    type={"text"}
                  />
                  <Button onClick={handleCopy}>
                    {translate.t("updateAccessToken.copy.copy")}
                  </Button>
                </Col100>
              </Row>
            )}
            <Row>
              {!submitSucceeded && hasAPIToken && (
                <Col100>
                  <ControlLabel>
                    <b>{translate.t("updateAccessToken.tokenCreated")}</b>
                    &nbsp;
                    {new Date(Number.parseInt(issuedAt, 10) * msToSec)
                      .toISOString()
                      .substring(0, yyyymmdd)}
                  </ControlLabel>
                </Col100>
              )}
              <Col100>
                <ButtonToolbarLeft>
                  {!submitSucceeded && hasAPIToken && (
                    <Button onClick={handleInvalidateAPIToken}>
                      {translate.t("updateAccessToken.invalidate")}
                    </Button>
                  )}
                </ButtonToolbarLeft>
              </Col100>
            </Row>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>
                    {translate.t("updateAccessToken.close")}
                  </Button>
                  <Button disabled={hasAPIToken} type={"submit"}>
                    {translate.t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { IAPITokenModalProps, APITokenModal };
