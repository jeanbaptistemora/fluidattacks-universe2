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
  IEditionFormValues,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IUpdateStakeholderPhoneResultAttr,
  IVerifyAdditionCodeFormValues,
  IVerifyEditionFormValues,
  IVerifyStakeholderResultAttr,
} from "./types";
import { VerificationCodeField } from "./VerificationCodeField";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { GET_USER } from "scenes/Dashboard/queries";
import { Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const MobileModal: React.FC<IMobileModalProps> = (
  props: IMobileModalProps
): JSX.Element => {
  const { onClose } = props;
  const { t } = useTranslation();
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isOpenEdit, setIsOpenEdit] = useState(false);
  const [isCodeInCurrentMobile, setIsCodeInCurrentMobile] = useState(false);
  const [isCodeInNewMobile, setIsCodeInNewMobile] = useState(false);
  const [currentMobileVerificationCode, setCurrentMobileVerificationCode] =
    useState("");
  const [phoneToAdd, setPhoneToAdd] = useState<IPhoneData | undefined>(
    undefined
  );
  const [phoneToEdit, setPhoneToEdit] = useState<IPhoneData | undefined>(
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
            setIsCodeInNewMobile(false);
            setPhoneToAdd(undefined);
          }
          if (data.updateStakeholderPhone.success && isEditing) {
            msgSuccess(
              t("profile.mobileModal.alerts.editionSuccess"),
              t("groupAlerts.titleSuccess")
            );
            setIsOpenEdit(false);
            setIsEditing(false);
            setIsCodeInCurrentMobile(false);
            setIsCodeInNewMobile(false);
            setPhoneToEdit(undefined);
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
        refetchQueries: [GET_STAKEHOLDER_PHONE, GET_USER],
      }
    );
  const [handleVerifyStakeholder] = useMutation<IVerifyStakeholderResultAttr>(
    VERIFY_STAKEHOLDER_MUTATION,
    {
      onCompleted: (data: IVerifyStakeholderResultAttr): void => {
        if (data.verifyStakeholder.success && isAdding) {
          msgSuccess(
            t("profile.mobileModal.alerts.sendNewMobileVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInNewMobile(true);
        }
        if (data.verifyStakeholder.success && isOpenEdit && !isEditing) {
          msgSuccess(
            t(
              "profile.mobileModal.alerts.sendCurrentMobileVerificationSuccess"
            ),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInCurrentMobile(true);
        }
        if (data.verifyStakeholder.success && isEditing) {
          msgSuccess(
            t("profile.mobileModal.alerts.sendNewMobileVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInNewMobile(true);
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
    setIsAdding(true);
    setIsCodeInNewMobile(false);
    void handleVerifyStakeholder({
      variables: {
        newPhone: {
          callingCountryCode: values.phone.callingCountryCode,
          nationalNumber: values.phone.nationalNumber,
        },
      },
    });
  }
  function handleVerifyAdditionCode(
    values: IVerifyAdditionCodeFormValues
  ): void {
    void handleUpdateStakeholderPhone({
      variables: {
        newPhone: {
          callingCountryCode: phoneToAdd?.callingCountryCode,
          nationalNumber: phoneToAdd?.nationalNumber,
        },
        verificationCode: values.newVerificationCode,
      },
    });
  }
  function handleOpenEdit(): void {
    setIsOpenEdit(true);
    setIsCodeInCurrentMobile(false);
    void handleVerifyStakeholder();
  }
  function handleEdit(values: IEditionFormValues): void {
    setPhoneToEdit(values.newPhone);
    setCurrentMobileVerificationCode(values.verificationCode);
    setIsEditing(true);
    setIsCodeInNewMobile(false);
    void handleVerifyStakeholder({
      variables: {
        newPhone: {
          callingCountryCode: values.newPhone.callingCountryCode,
          nationalNumber: values.newPhone.nationalNumber,
        },
        verificationCode: values.verificationCode,
      },
    });
  }
  function handleVerifyEditionCode(values: IVerifyEditionFormValues): void {
    void handleUpdateStakeholderPhone({
      variables: {
        newPhone: {
          callingCountryCode: phoneToEdit?.callingCountryCode,
          nationalNumber: phoneToEdit?.nationalNumber,
        },
        verificationCode: values.newVerificationCode,
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
    <Modal open={true} title={t("profile.mobileModal.title")}>
      {!(isAdding && isCodeInNewMobile) && _.isNull(phone) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            phone: {
              callingCountryCode: "57",
              countryCode: "co",
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
                  <Can do={"api_mutations_update_stakeholder_phone_mutate"}>
                    <Button type={"submit"} variant={"primary"}>
                      {t("profile.mobileModal.add")}
                    </Button>
                  </Can>
                </ModalFooter>
              </div>
            </div>
          </Form>
        </Formik>
      ) : undefined}
      {isAdding && isCodeInNewMobile && !_.isUndefined(phoneToAdd) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newVerificationCode: "",
            phone: phoneToAdd,
          }}
          name={"verifyAdditionCode"}
          onSubmit={handleVerifyAdditionCode}
        >
          <Form id={"verifyAdditionCode"}>
            <Row>
              <Col100>
                <PhoneField disabled={true} />
              </Col100>
            </Row>
            <Col100>
              <VerificationCodeField name={"newVerificationCode"} />
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
      {!_.isNull(phone) && !isCodeInNewMobile ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newPhone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: "",
            },
            phone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: phone.nationalNumber,
            },
            verificationCode: "",
          }}
          name={"editPhone"}
          onSubmit={handleEdit}
        >
          <Form id={"editPhone"}>
            <Row>
              <Col100>
                <PhoneField disabled={true} />
              </Col100>
            </Row>
            {isOpenEdit && isCodeInCurrentMobile ? (
              <React.Fragment>
                <Row>
                  <Col100>
                    <VerificationCodeField />
                  </Col100>
                </Row>
                <Row>
                  <Col100>
                    <PhoneField
                      label={"profile.mobileModal.fields.newPhoneNumber"}
                      name={"newPhone"}
                    />
                  </Col100>
                </Row>
              </React.Fragment>
            ) : undefined}
            <div>
              <div>
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("profile.mobileModal.close")}
                  </Button>
                  <Can do={"api_mutations_update_stakeholder_phone_mutate"}>
                    {isOpenEdit && isCodeInCurrentMobile ? (
                      <Button type={"submit"} variant={"primary"}>
                        {t("profile.mobileModal.edit")}
                      </Button>
                    ) : (
                      <Button onClick={handleOpenEdit} variant={"primary"}>
                        {t("profile.mobileModal.edit")}
                      </Button>
                    )}
                  </Can>
                </ModalFooter>
              </div>
            </div>
          </Form>
        </Formik>
      ) : undefined}
      {isEditing &&
      !_.isNull(phone) &&
      isCodeInNewMobile &&
      !_.isUndefined(phoneToEdit) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newPhone: {
              callingCountryCode: phoneToEdit.callingCountryCode,
              countryCode: phoneToEdit.countryCode.toLowerCase(),
              nationalNumber: phoneToEdit.nationalNumber,
            },
            newVerificationCode: "",
            phone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: phone.nationalNumber,
            },
            verificationCode: currentMobileVerificationCode,
          }}
          name={"verifyEditionCode"}
          onSubmit={handleVerifyEditionCode}
        >
          <Form id={"verifyEditionCode"}>
            <Row>
              <Col100>
                <PhoneField disabled={true} />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <VerificationCodeField disabled={true} />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <PhoneField
                  disabled={true}
                  label={"profile.mobileModal.fields.newPhoneNumber"}
                  name={"newPhone"}
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <VerificationCodeField name={"newVerificationCode"} />
              </Col100>
            </Row>
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
