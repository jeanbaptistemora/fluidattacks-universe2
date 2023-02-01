import type { MutationFunction } from "@apollo/client";
import dayjs, { extend } from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";
import { Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
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
const confirmTime: number = 60 * 60 * 24 * 7;

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
  const lastAccessTokenUse = useMemo((): number | string => {
    const value = accessToken?.lastAccessTokenUse;
    if (value === undefined || value === null) {
      return "No used";
    }

    const date = new Date(value);
    if (_.isEmpty(value) || isNaN(date.getTime())) return "-";
    extend(utc);

    return dayjs(dayjs.utc(value, "YYYY-MM-DD HH:mm:ss")).valueOf();
  }, [accessToken]);

  const lastAccessTokenUseFromNow = useMemo((): string => {
    if (typeof lastAccessTokenUse === "string") {
      return lastAccessTokenUse;
    }
    extend(relativeTime);
    extend(utc);
    extend(timezone);

    return dayjs(lastAccessTokenUse).tz(dayjs.tz.guess()).fromNow();
  }, [lastAccessTokenUse]);

  const hasAPIToken: boolean = accessToken?.hasAccessToken ?? false;
  const issuedAt: string = accessToken?.issuedAt ?? "0";

  const [updateAPIToken, mtResponse] = useUpdateAPIToken(refetch);
  const handleUpdateAPIToken = useCallback(
    async (values: IAccessTokenAttr): Promise<void> => {
      const expTimeStamp: number = Math.floor(
        new Date(values.expirationTime).getTime() / msToSec
      );
      mixpanel.track("GenerateAPIToken");
      await updateAPIToken({
        variables: { expirationTime: expTimeStamp },
      });
    },
    [updateAPIToken]
  );

  const invalidateAPIToken: MutationFunction = useInvalidateAPIToken(
    refetch,
    onClose
  );
  const handleInvalidateAPIToken = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        if (typeof lastAccessTokenUse === "string") {
          void invalidateAPIToken();

          return;
        }

        const currentTimeStamp: number = dayjs.utc().valueOf();
        if ((currentTimeStamp - lastAccessTokenUse) / msToSec > confirmTime) {
          void invalidateAPIToken();

          return;
        }

        confirm((): void => {
          void invalidateAPIToken();
        });
      },
    [invalidateAPIToken, lastAccessTokenUse]
  );

  const handleCopy = useCallback(async (): Promise<void> => {
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
  }, [mtResponse.data?.updateAccessToken.sessionJwt, t]);

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
                <ConfirmDialog
                  message={
                    <React.Fragment>
                      <label>
                        <b>{t("updateAccessToken.warning")}</b>
                      </label>
                      <Text mb={1}>
                        <Text disp={"inline"} fw={7}>
                          {t("updateAccessToken.tokenLastUsed")}
                        </Text>
                        &nbsp;
                        {lastAccessTokenUseFromNow}
                      </Text>
                    </React.Fragment>
                  }
                  title={t("updateAccessToken.invalidate")}
                >
                  {(confirm): JSX.Element => {
                    return (
                      <Button
                        onClick={handleInvalidateAPIToken(confirm)}
                        variant={"secondary"}
                      >
                        {t("updateAccessToken.invalidate")}
                      </Button>
                    );
                  }}
                </ConfirmDialog>
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
