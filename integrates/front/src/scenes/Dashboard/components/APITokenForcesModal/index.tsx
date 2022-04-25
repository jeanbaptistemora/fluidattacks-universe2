import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import {
  useGetAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/APITokenForcesModal/hooks";
import { Col100, ControlLabel, Row } from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import { msgError, msgSuccess } from "utils/notifications";

interface IAPITokenForcesModalProps {
  groupName: string;
  open: boolean;
  onClose: () => void;
}

const APITokenForcesModal: React.FC<IAPITokenForcesModalProps> = ({
  open,
  onClose,
  groupName,
}: IAPITokenForcesModalProps): JSX.Element => {
  const { t } = useTranslation();
  const [getApiToken, getTokenCalled, getTokenData, getTokenLoading] =
    useGetAPIToken(groupName);
  const [updateApiToken] = useUpdateAPIToken(groupName);

  const currentToken: string | undefined = getTokenData?.group.forcesToken;

  const handleUpdateAPIToken = useCallback(async (): Promise<void> => {
    await updateApiToken({ variables: { groupName } });
  }, [groupName, updateApiToken]);

  const handleReveal = useCallback((): void => {
    getApiToken();
  }, [getApiToken]);
  const handleCopy: () => Promise<void> =
    useCallback(async (): Promise<void> => {
      const { clipboard } = navigator;

      if (_.isUndefined(clipboard)) {
        msgError(t("updateForcesToken.copy.failed"));
      } else {
        await clipboard.writeText(currentToken ?? "");
        document.execCommand("copy");
        msgSuccess(
          t("updateForcesToken.copy.successfully"),
          t("updateForcesToken.copy.success")
        );
      }
    }, [currentToken, t]);
  if (
    !getTokenData?.group.forcesToken && // eslint-disable-line @typescript-eslint/strict-boolean-expressions
    getTokenCalled &&
    !getTokenLoading
  ) {
    msgError(t("updateForcesToken.tokenNoExists"));
  }

  return (
    <Modal open={open} title={t("updateForcesToken.title")}>
      <Formik
        enableReinitialize={true}
        initialValues={{ sessionJwt: currentToken ?? "" }}
        name={"updateForcesToken"}
        onSubmit={handleUpdateAPIToken}
      >
        <Form>
          <Row>
            <Col100>
              <ControlLabel>
                <b>{t("updateForcesToken.accessToken")}</b>
              </ControlLabel>
              <Field
                className={"noresize"} // eslint-disable-line react/forbid-component-props
                component={FormikTextArea}
                disabled={true}
                name={"sessionJwt"}
                rows={"7"}
                type={"text"}
              />
              <Button
                disabled={_.isEmpty(currentToken)}
                onClick={handleCopy}
                variant={"secondary"}
              >
                {t("updateForcesToken.copy.copy")}
              </Button>
              <Button
                disabled={getTokenCalled}
                onClick={handleReveal}
                variant={"secondary"}
              >
                {t("updateForcesToken.revealToken")}
              </Button>
            </Col100>
          </Row>
          <ModalFooter>
            <Button onClick={onClose} variant={"secondary"}>
              {t("updateForcesToken.close")}
            </Button>
            <Button
              disabled={!getTokenCalled || getTokenLoading}
              type={"submit"}
              variant={"primary"}
            >
              {_.isEmpty(currentToken)
                ? t("updateForcesToken.generate")
                : t("updateForcesToken.reset")}
            </Button>
          </ModalFooter>
        </Form>
      </Formik>
    </Modal>
  );
};

export type { IAPITokenForcesModalProps };
export { APITokenForcesModal };
