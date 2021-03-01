import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Modal } from "components/Modal";
import React from "react";
import { TextArea } from "utils/forms/fields";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  Row,
} from "styles/styledComponents";
import { msgError, msgSuccess } from "utils/notifications";
import {
  useGetAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/APITokenForcesModal/hooks";

interface IAPITokenForcesModalProps {
  groupName: string;
  open: boolean;
  onClose: () => void;
}

const APITokenForcesModal: React.FC<IAPITokenForcesModalProps> = (
  props: IAPITokenForcesModalProps
): JSX.Element => {
  const { open, onClose, groupName } = props;

  const [
    getApiToken,
    getTokenCalled,
    getTokenData,
    getTokenLoading,
  ] = useGetAPIToken(groupName);
  const [updateApiToken, updateResponse] = useUpdateAPIToken();

  const currentToken: string | undefined = updateResponse.data
    ? updateResponse.data.updateForcesAccessToken.sessionJwt
    : getTokenData?.project.forcesToken;

  const handleUpdateAPIToken: () => void = React.useCallback((): void => {
    void updateApiToken({ variables: { groupName } });
  }, [groupName, updateApiToken]);
  const handleReveal: () => void = React.useCallback((): void => {
    void getApiToken(); // eslint-disable-line @typescript-eslint/no-confusing-void-expression
  }, [getApiToken]);
  const handleCopy: () => Promise<void> = React.useCallback(async (): Promise<void> => {
    const clipboard: Clipboard = navigator.clipboard;

    if (!_.isUndefined(clipboard)) {
      await clipboard.writeText(getTokenData?.project.forcesToken ?? "");
      document.execCommand("copy");
      msgSuccess(
        translate.t("update_forces_token.copy.successfully"),
        translate.t("update_forces_token.copy.success")
      );
    } else {
      msgError(translate.t("update_forces_token.copy.failed"));
    }
  }, [getTokenData?.project.forcesToken]);
  if (
    !getTokenData?.project.forcesToken && // eslint-disable-line @typescript-eslint/strict-boolean-expressions
    getTokenCalled &&
    !getTokenLoading
  ) {
    msgError(translate.t("update_forces_token.token_no_exists"));
  }

  return (
    <Modal headerTitle={translate.t("update_forces_token.tittle")} open={open}>
      <GenericForm
        initialValues={{ sessionJwt: currentToken }}
        name={"updateForcesToken"}
        onSubmit={handleUpdateAPIToken}
      >
        <React.Fragment>
          <Row>
            <Col100>
              <ControlLabel>
                <b>{translate.t("update_forces_token.access_token")}</b>
              </ControlLabel>
              <Field
                className={"noresize"} // eslint-disable-line react/forbid-component-props
                component={TextArea}
                disabled={true}
                name={"sessionJwt"}
                rows={"7"}
                type={"text"}
              />
              {/* eslint-disable-next-line @typescript-eslint/strict-boolean-expressions */}
              <Button disabled={!currentToken} onClick={handleCopy}>
                {translate.t("update_forces_token.copy.copy")}
              </Button>
              <Button disabled={getTokenCalled} onClick={handleReveal}>
                {translate.t("update_forces_token.reveal_token")}
              </Button>
            </Col100>
          </Row>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={onClose}>
                  {translate.t("update_forces_token.close")}
                </Button>
                <Button
                  disabled={!getTokenCalled || getTokenLoading}
                  type={"submit"}
                >
                  {/* eslint-disable-next-line @typescript-eslint/strict-boolean-expressions */}
                  {currentToken
                    ? translate.t("update_forces_token.reset")
                    : translate.t("update_forces_token.generate")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </React.Fragment>
      </GenericForm>
    </Modal>
  );
};

export { IAPITokenForcesModalProps, APITokenForcesModal };
