/* eslint-disable jsx-a11y/no-autofocus */
import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { PhoneField } from "./PhoneField";
import {
  GET_STAKEHOLDER_PHONE,
  UPDATE_STAKEHOLDER_PHONE_MUTATION,
  VERIFY_STAKEHOLDER_MUTATION,
} from "./queries";
import type {
  IAdditionFormValues,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IUpdateStakeholderPhoneResultAttr,
  IVerificationFormValues,
  IVerifyStakeholderResultAttr,
} from "./types";
import { VerificationCodeField } from "./VerificationCodeField";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Col100, Row } from "styles/styledComponents";
import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const MobileModal: React.FC<IMobileModalProps> = (
  props: IMobileModalProps
): JSX.Element => {
  const { onClose } = props;
  const { t } = useTranslation();
  const [isAdding, setIsAdding] = useState(false);
  const [phoneToAdd, setPhoneToAdd] = useState<IPhoneData | undefined>(
    undefined
  );

  // GraphQL operations
  const [handleUpdateStakeholderPhone] =
    useMutation<IUpdateStakeholderPhoneResultAttr>(
      UPDATE_STAKEHOLDER_PHONE_MUTATION,
      {
        onCompleted: (data: IUpdateStakeholderPhoneResultAttr): void => {
          if (data.updateStakeholderPhone.success && isAdding) {
            msgSuccess(
              t("profile.mobileModal.alerts.additionSuccess"),
              t("groupAlerts.titleSuccess")
            );
            setIsAdding(false);
          }
        },
        onError: (errors: ApolloError): void => {
          errors.graphQLErrors.forEach((error: GraphQLError): void => {
            switch (error.message) {
              case "Exception - A mobile number is required with the international format":
                msgError(t("profile.mobileModal.alerts.requiredMobile"));
                break;
              case "Exception - Stakeholder could not be verified":
                msgError(
                  t("profile.mobileModal.alerts.nonVerifiedStakeholder")
                );
                break;
              case "Exception - The verification code is invalid":
                msgError(
                  t("profile.mobileModal.alerts.invalidVerificationCode")
                );
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.warning(
                  "An error occurred updating stakeholder phone",
                  error
                );
            }
          });
        },
        refetchQueries: [GET_STAKEHOLDER_PHONE],
      }
    );
  const [handleVerifyStakeholder] = useMutation<IVerifyStakeholderResultAttr>(
    VERIFY_STAKEHOLDER_MUTATION,
    {
      onCompleted: (data: IVerifyStakeholderResultAttr): void => {
        if (data.verifyStakeholder.success) {
          msgSuccess(
            t("profile.mobileModal.alerts.additionVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setIsAdding(true);
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A mobile number is required with the international format":
            case "Exception - A new phone number is required":
              msgError(t("profile.mobileModal.alerts.requiredMobile"));
              break;
            case "Exception - Stakeholder could not be verified":
              msgError(t("profile.mobileModal.alerts.nonVerifiedStakeholder"));
              break;
            case "Exception - The verification code is invalid":
              msgError(t("profile.mobileModal.alerts.invalidVerificationCode"));
              break;
            case "Exception - The verification code is required":
              msgError(
                t("profile.mobileModal.alerts.requiredVerificationCode")
              );
              break;
            case "Exception - Stakeholder verification could not be started":
              msgError(t("profile.mobileModal.alerts.nonSentVerificationCode"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating stakeholder phone",
                error
              );
          }
        });
      },
    }
  );

  function handleAdd(values: IAdditionFormValues): void {
    setPhoneToAdd(values.phone);
    void handleVerifyStakeholder({
      variables: {
        newPhone: {
          countryCode: values.phone.countryDialCode,
          nationalNumber: values.phone.nationalNumber,
        },
      },
    });
  }

  function handleVerifyAdditionCode(values: IVerificationFormValues): void {
    void handleUpdateStakeholderPhone({
      variables: {
        countryCode: phoneToAdd?.countryDialCode,
        nationalNumber: phoneToAdd?.nationalNumber,
        verificationCode: values.verificationCode,
      },
    });
  }

  const { data } = useQuery<IGetStakeholderPhoneAttr>(GET_STAKEHOLDER_PHONE, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder's phone", error);
      });
    },
  });

  const phone = _.isUndefined(data) ? null : data.me.phone;

  return (
    <Modal open={true} title={translate.t("profile.mobileModal.title")}>
      {isAdding || !_.isNull(phone) ? undefined : (
        <Formik
          enableReinitialize={true}
          initialValues={{
            phone: {
              countryDialCode: "57",
              countryIso2: "co",
              nationalNumber: "",
            },
          }}
          name={"addPhone"}
          onSubmit={handleAdd}
        >
          <Form id={"addPhone"}>
            <Row>
              <Col100>
                <PhoneField autoFocus={true} />
              </Col100>
            </Row>
            <div>
              <div>
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("profile.mobileModal.close")}
                  </Button>
                  <Button type={"submit"} variant={"primary"}>
                    {t("profile.mobileModal.add")}
                  </Button>
                </ModalFooter>
              </div>
            </div>
          </Form>
        </Formik>
      )}
      {isAdding && !_.isUndefined(phoneToAdd) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            phone: phoneToAdd,
            verificationCode: "",
          }}
          name={"addPhoneVerification"}
          onSubmit={handleVerifyAdditionCode}
        >
          <Form id={"addPhoneVerification"}>
            <Row>
              <Col100>
                <PhoneField disabled={true} />
              </Col100>
            </Row>
            <Col100>
              <VerificationCodeField />
            </Col100>
            <div>
              <div>
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("profile.mobileModal.close")}
                  </Button>
                  <Button type={"submit"} variant={"primary"}>
                    {t("profile.mobileModal.verify")}
                  </Button>
                </ModalFooter>
              </div>
            </div>
          </Form>
        </Formik>
      ) : undefined}
    </Modal>
  );
};

export { MobileModal };
