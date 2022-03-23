import type { MutationFunction } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import {
  useGetAPIToken,
  useInvalidateAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/hooks";
import type {
  IAccessTokenAttr,
  IGetAccessTokenDictAttr,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/types";
import {
  ButtonToolbarLeft,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikDate, FormikTextArea } from "utils/forms/fields";
import { msgError, msgSuccess } from "utils/notifications";
import {
  composeValidators,
  isLowerDate,
  isValidDateAccessToken,
  required,
} from "utils/validations";

interface IAPITokenModalProps {
  open: boolean;
  onClose: () => void;
}

const APITokenModal: React.FC<IAPITokenModalProps> = ({
  open,
  onClose,
}: IAPITokenModalProps): JSX.Element => {
  const { t } = useTranslation();
  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  const [data, refetch] = useGetAPIToken();
  const accessToken: IGetAccessTokenDictAttr | undefined = _.isUndefined(data)
    ? undefined
    : JSON.parse(data.me.accessToken);
  const hasAPIToken: boolean = accessToken?.hasAccessToken ?? false;
  const issuedAt: string = accessToken?.issuedAt ?? "0";

  const [updateAPIToken, mtResponse] = useUpdateAPIToken(refetch);
  async function handleUpdateAPIToken(values: IAccessTokenAttr): Promise<void> {
    const expTimeStamp: number = Math.floor(
      new Date(values.expirationTime).getTime() / msToSec
    );
    mixpanel.track("GenerateAPIToken");
    await updateAPIToken({
      variables: { expirationTime: expTimeStamp },
    });
  }

  const invalidateAPIToken: MutationFunction = useInvalidateAPIToken(
    refetch,
    onClose
  );
  async function handleInvalidateAPIToken(): Promise<void> {
    await invalidateAPIToken();
  }

  async function handleCopy(): Promise<void> {
    const { clipboard } = navigator;

    if (_.isUndefined(clipboard)) {
      msgError(t("updateAccessToken.copy.failed"));
    } else {
      await clipboard.writeText(
        mtResponse.data?.updateAccessToken.sessionJwt ?? ""
      );
      document.execCommand("copy");
      msgSuccess(
        t("updateAccessToken.copy.successfully"),
        t("updateAccessToken.copy.success")
      );
    }
  }

  return (
    <Modal onClose={onClose} open={open} title={t("updateAccessToken.title")}>
      <Formik
        enableReinitialize={true}
        initialValues={{
          expirationTime: "",
          sessionJwt: mtResponse.data?.updateAccessToken.sessionJwt ?? "",
        }}
        name={"updateAccessToken"}
        onSubmit={handleUpdateAPIToken}
      >
        <Form>
          <Row>
            <Col100>
              {!hasAPIToken && (
                <FormGroup>
                  <ControlLabel>
                    <b>{t("updateAccessToken.expirationTime")}</b>
                  </ControlLabel>
                  <Field
                    component={FormikDate}
                    dataTestId={"expiration-time-input"}
                    name={"expirationTime"}
                    type={"date"}
                    validate={composeValidators([
                      isLowerDate,
                      isValidDateAccessToken,
                      required,
                    ])}
                  />
                </FormGroup>
              )}
            </Col100>
          </Row>
          {!_.isUndefined(mtResponse.data) && (
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{t("updateAccessToken.message")}</b>
                </ControlLabel>
                <ControlLabel>
                  <b>{t("updateAccessToken.accessToken")}</b>
                </ControlLabel>
                <Field
                  // Allow to block resizing the TextArea
                  // eslint-disable-next-line react/forbid-component-props
                  className={"noresize"}
                  component={FormikTextArea}
                  disabled={true}
                  name={"sessionJwt"}
                  rows={"7"}
                  type={"text"}
                />
                <Button onClick={handleCopy} variant={"secondary"}>
                  {t("updateAccessToken.copy.copy")}
                </Button>
              </Col100>
            </Row>
          )}
          <Row>
            {_.isUndefined(mtResponse.data) && hasAPIToken && (
              <Col100>
                <ControlLabel>
                  <b>{t("updateAccessToken.tokenCreated")}</b>
                  &nbsp;
                  {new Date(Number.parseInt(issuedAt, 10) * msToSec)
                    .toISOString()
                    .substring(0, yyyymmdd)}
                </ControlLabel>
              </Col100>
            )}
            <Col100>
              <ButtonToolbarLeft>
                {_.isUndefined(mtResponse.data) && hasAPIToken && (
                  <Button
                    onClick={handleInvalidateAPIToken}
                    variant={"secondary"}
                  >
                    {t("updateAccessToken.invalidate")}
                  </Button>
                )}
              </ButtonToolbarLeft>
            </Col100>
          </Row>
          <ModalFooter>
            <Button onClick={onClose} variant={"secondary"}>
              {t("updateAccessToken.close")}
            </Button>
            <Button disabled={hasAPIToken} type={"submit"} variant={"primary"}>
              {t("confirmmodal.proceed")}
            </Button>
          </ModalFooter>
        </Form>
      </Formik>
    </Modal>
  );
};

export { IAPITokenModalProps, APITokenModal };
