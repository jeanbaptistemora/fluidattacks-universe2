import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_STAKEHOLDER_PHONE, VERIFY_STAKEHOLDER_MUTATION } from "./queries";
import type {
  IGetStakeholderPhoneAttr,
  IVerifyDialogProps,
  IVerifyFn,
  IVerifyFormValues,
  IVerifyStakeholderResultAttr,
} from "./types";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { BaseStep, Tour } from "components/Tour";
import { Col100, ControlLabel, Row } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { required } from "utils/validations";

const VerifyDialog: React.FC<IVerifyDialogProps> = ({
  isOpen,
  children,
  message,
}: Readonly<IVerifyDialogProps>): JSX.Element => {
  const { t } = useTranslation();
  const [verifyCallback, setVerifyCallback] = useState(
    (): ((verificationCode: string) => void) =>
      (_verificationCode: string): void =>
        undefined
  );
  const [cancelCallback, setCancelCallback] = useState(
    (): (() => void) => (): void => undefined
  );

  const [handleVerifyStakeholder] = useMutation<IVerifyStakeholderResultAttr>(
    VERIFY_STAKEHOLDER_MUTATION,
    {
      onCompleted: (data: IVerifyStakeholderResultAttr): void => {
        if (data.verifyStakeholder.success) {
          msgSuccess(
            t("verifyDialog.alerts.sendMobileVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Stakeholder verification could not be started":
              msgError(t("verifyDialog.alerts.nonSentVerificationCode"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred sending a verification code",
                error
              );
          }
          cancelCallback();
        });
      },
    }
  );

  const { data } = useQuery<IGetStakeholderPhoneAttr>(GET_STAKEHOLDER_PHONE, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder's phone", error);
      });
    },
  });

  if (_.isUndefined(data)) {
    return <div />;
  }
  const { phone } = data.me;

  const setVerifyCallbacks: IVerifyFn = (
    verifyFn: (verificationCode: string) => void,
    cancelFn: () => void
  ): void => {
    setVerifyCallback((): ((verificationCode: string) => void) => verifyFn);
    setCancelCallback((): (() => void) => cancelFn);
    if (!_.isNil(phone)) {
      void handleVerifyStakeholder();
    }
  };

  function handleClose(): void {
    cancelCallback();
  }

  function handleProceed(values: IVerifyFormValues): void {
    verifyCallback(values.verificationCode);
  }

  return (
    <React.Fragment>
      {isOpen && _.isNil(phone) ? (
        <Tour
          onFinish={handleClose}
          run={true}
          steps={[
            {
              ...BaseStep,
              content: t("verifyDialog.tour.addMobile.profile"),
              disableBeacon: true,
              hideFooter: true,
              target: "#navbar-user-profile",
            },
          ]}
        />
      ) : undefined}
      <Modal
        onClose={handleClose}
        open={isOpen}
        title={t("verifyDialog.title")}
      >
        {message}
        <Formik
          enableReinitialize={true}
          initialValues={{
            verificationCode: "",
          }}
          name={"verify"}
          onSubmit={handleProceed}
        >
          <Form id={"verify"}>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{t("verifyDialog.fields.verificationCode")}</b>
                </ControlLabel>
                <Field
                  component={FormikText}
                  name={"verificationCode"}
                  type={"text"}
                  validate={required}
                />
              </Col100>
            </Row>
            <br />
            <ModalFooter>
              <Button
                id={"verifymodal-proceed"}
                type={"submit"}
                variant={"primary"}
              >
                {t("verifyDialog.verify")}
              </Button>
            </ModalFooter>
          </Form>
        </Formik>
      </Modal>
      {children(setVerifyCallbacks)}
    </React.Fragment>
  );
};

export { VerifyDialog };
