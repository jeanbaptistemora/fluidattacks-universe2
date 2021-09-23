import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  useGetAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/APITokenForcesModal/hooks";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  Row,
} from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IAPITokenForcesModalProps {
  groupName: string;
  open: boolean;
  onClose: () => void;
}

const APITokenForcesModal: React.FC<IAPITokenForcesModalProps> = (
  props: IAPITokenForcesModalProps
): JSX.Element => {
  const { open, onClose, groupName } = props;

  const [getApiToken, getTokenCalled, getTokenData, getTokenLoading] =
    useGetAPIToken(groupName);
  const [updateApiToken] = useUpdateAPIToken();

  const currentToken: string | undefined = getTokenData?.group.forcesToken;

  const handleUpdateAPIToken: () => void = useCallback((): void => {
    void updateApiToken({ variables: { groupName } });
  }, [groupName, updateApiToken]);
  const handleReveal: () => void = useCallback((): void => {
    void getApiToken(); // eslint-disable-line @typescript-eslint/no-confusing-void-expression
  }, [getApiToken]);
  const handleCopy: () => Promise<void> =
    useCallback(async (): Promise<void> => {
      const { clipboard } = navigator;

      if (_.isUndefined(clipboard)) {
        msgError(translate.t("updateForcesToken.copy.failed"));
      } else {
        await clipboard.writeText(currentToken ?? "");
        document.execCommand("copy");
        msgSuccess(
          translate.t("updateForcesToken.copy.successfully"),
          translate.t("updateForcesToken.copy.success")
        );
      }
    }, [currentToken]);
  if (
    !getTokenData?.group.forcesToken && // eslint-disable-line @typescript-eslint/strict-boolean-expressions
    getTokenCalled &&
    !getTokenLoading
  ) {
    msgError(translate.t("updateForcesToken.tokenNoExists"));
  }

  return (
    <Modal headerTitle={translate.t("updateForcesToken.title")} open={open}>
      <Formik
        enableReinitialize={true}
        initialValues={{ sessionJwt: currentToken }}
        name={"updateForcesToken"}
        onSubmit={handleUpdateAPIToken}
      >
        <Form>
          <Row>
            <Col100>
              <ControlLabel>
                <b>{translate.t("updateForcesToken.accessToken")}</b>
              </ControlLabel>
              <Field
                className={"noresize"} // eslint-disable-line react/forbid-component-props
                component={FormikTextArea}
                disabled={true}
                name={"sessionJwt"}
                rows={"7"}
                type={"text"}
              />
              {/* eslint-disable-next-line @typescript-eslint/strict-boolean-expressions */}
              <Button disabled={!currentToken} onClick={handleCopy}>
                {translate.t("updateForcesToken.copy.copy")}
              </Button>
              <Button disabled={getTokenCalled} onClick={handleReveal}>
                {translate.t("updateForcesToken.revealToken")}
              </Button>
            </Col100>
          </Row>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={onClose}>
                  {translate.t("updateForcesToken.close")}
                </Button>
                <Button
                  disabled={!getTokenCalled || getTokenLoading}
                  type={"submit"}
                >
                  {/* eslint-disable-next-line @typescript-eslint/strict-boolean-expressions */}
                  {currentToken
                    ? translate.t("updateForcesToken.reset")
                    : translate.t("updateForcesToken.generate")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </Form>
      </Formik>
    </Modal>
  );
};

export { IAPITokenForcesModalProps, APITokenForcesModal };
