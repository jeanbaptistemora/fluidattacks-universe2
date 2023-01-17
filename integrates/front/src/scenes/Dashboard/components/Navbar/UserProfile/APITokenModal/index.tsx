import type { MutationFunction } from "@apollo/client";
import dayjs from "dayjs";
import { Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { InputDate, TextArea } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import {
  useGetAPIToken,
  useInvalidateAPIToken,
  useUpdateAPIToken,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/hooks";
import type {
  IAccessTokenAttr,
  IGetAccessTokenDictAttr,
} from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal/types";
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

  const sixMonthsLater: string = dayjs().add(6, "months").format("YYYY-MM-DD");

  const oneDayLater: string = dayjs().add(1, "day").format("YYYY-MM-DD");

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
          {hasAPIToken ? undefined : (
            <Fragment>
              <Text fw={7} mb={1}>
                {t("updateAccessToken.expirationTime")}
              </Text>
              <InputDate
                max={sixMonthsLater}
                min={oneDayLater}
                name={"expirationTime"}
                validate={composeValidators([
                  isLowerDate,
                  isValidDateAccessToken,
                  required,
                ])}
              />
            </Fragment>
          )}
          {mtResponse.data === undefined ? (
            hasAPIToken ? (
              <Fragment>
                <Text mb={1}>
                  <Text disp={"inline"} fw={7}>
                    {t("updateAccessToken.tokenCreated")}
                  </Text>
                  &nbsp;
                  {new Date(Number.parseInt(issuedAt, 10) * msToSec)
                    .toISOString()
                    .substring(0, yyyymmdd)}
                </Text>
                <Button
                  onClick={handleInvalidateAPIToken}
                  variant={"secondary"}
                >
                  {t("updateAccessToken.invalidate")}
                </Button>
              </Fragment>
            ) : undefined
          ) : (
            <Gap disp={"block"} mh={0}>
              <Text fw={7}>{t("updateAccessToken.message")}</Text>
              <TextArea disabled={true} name={"sessionJwt"} rows={5} />
              <Button onClick={handleCopy} variant={"secondary"}>
                {t("updateAccessToken.copy.copy")}
              </Button>
            </Gap>
          )}
          {hasAPIToken ? undefined : <ModalConfirm onCancel={onClose} />}
        </Form>
      </Formik>
    </Modal>
  );
};

export type { IAPITokenModalProps };
export { APITokenModal };
