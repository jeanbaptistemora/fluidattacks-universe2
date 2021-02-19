import { Button } from "components/Button";
import { Modal } from "components/Modal";
import _ from "lodash";
import React from "react";
import { Field } from "redux-form";
import {
  useGetAPIToken, useUpdateAPIToken,
} from "scenes/Dashboard/components/APITokenForcesModal/hooks";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  Row,
} from "styles/styledComponents";
import { TextArea } from "utils/forms/fields";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IAPITokenForcesModalProps {
  groupName: string;
  open: boolean;
  onClose(): void;
}

const apiTokenForcesModal: React.FC<IAPITokenForcesModalProps> = (
  props: IAPITokenForcesModalProps,
): JSX.Element => {
  const { open, onClose, groupName } = props;

  const [getApiToken, getTokenCalled, getTokenData, getTokenLoading] = useGetAPIToken(groupName);
  const [updateApiToken, updateResponse] = useUpdateAPIToken();

  const currentToken: string | undefined = Boolean(getTokenData?.project.forcesToken) ?
    getTokenData?.project.forcesToken :
    updateResponse.data?.updateForcesAccessToken.sessionJwt;

  const handleUpdateAPIToken: () => void = () => {
    void updateApiToken({ variables: { groupName } });
  };
  const handleReveal: () => void = () => {
    // tslint:disable-next-line: no-void-expression
    void getApiToken();
  };
  const handleCopy: () => Promise<void> = async () => {
    const clipboard: Clipboard = navigator.clipboard;

    if (!_.isUndefined(clipboard)) {
      await clipboard.writeText(
        getTokenData?.project.forcesToken ?? "",
      );
      document.execCommand("copy");
      msgSuccess(
        translate.t("update_forces_token.copy.successfully"),
        translate.t("update_forces_token.copy.success"),
      );
    } else {
      msgError(translate.t("update_forces_token.copy.failed"));
    }
  };
  if (!Boolean(getTokenData?.project.forcesToken) && getTokenCalled && !getTokenLoading) {
    msgError(translate.t("update_forces_token.token_no_exists"));
  }

  return (
    <Modal headerTitle={translate.t("update_forces_token.tittle")} open={open}>
      <GenericForm
        name={"updateForcesToken"}
        onSubmit={handleUpdateAPIToken}
        initialValues={{ sessionJwt: currentToken }}>
        <React.Fragment>
          <Row>
            <Col100>
              <ControlLabel>
                <b>{translate.t("update_forces_token.access_token")}</b>
              </ControlLabel>
              <Field
                className={"noresize"}
                component={TextArea}
                disabled={true}
                name={"sessionJwt"}
                rows={"7"}
                type={"text"}
              />
              <Button onClick={handleCopy} disabled={!Boolean(currentToken)}>
                {translate.t("update_forces_token.copy.copy")}
              </Button>
              <Button
                onClick={handleReveal}
                disabled={getTokenCalled}>
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
                  {Boolean(currentToken) ? translate.t("update_forces_token.reset") : translate.t("update_forces_token.generate")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </React.Fragment>
      </GenericForm>
    </Modal>
  );
};

export { IAPITokenForcesModalProps, apiTokenForcesModal as APITokenForcesModal };
