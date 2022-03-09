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
} from "./queries";
import type {
  IAdditionFormValues,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IPhone,
  IUpdateStakeholderPhoneAttr,
  IVerificationFormValues,
} from "./types";
import { VerificationCodeField } from "./VerificationCodeField";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const MobileModal: React.FC<IMobileModalProps> = (
  props: IMobileModalProps
): JSX.Element => {
  const { onClose } = props;
  const { t } = useTranslation();
  const [isAdding, setIsAdding] = useState(false);
  const [phoneToAdd, setPhoneToAdd] = useState<IPhone | undefined>(undefined);

  // GraphQL operations
  const [handleUpdateStakeholderPhone] =
    useMutation<IUpdateStakeholderPhoneAttr>(UPDATE_STAKEHOLDER_PHONE_MUTATION);

  function handleAdd(values: IAdditionFormValues): void {
    setIsAdding(true);
    setPhoneToAdd(values.phone);
  }

  function handleVerifyAdditionCode(values: IVerificationFormValues): void {
    void handleUpdateStakeholderPhone({
      variables: {
        countryCode: phoneToAdd?.countryDialCode,
        localNumber: phoneToAdd?.localNumber,
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
              localNumber: "",
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
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("profile.mobileModal.close")}
                  </Button>
                  <Button type={"submit"} variant={"primary"}>
                    {t("profile.mobileModal.add")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
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
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("profile.mobileModal.close")}
                  </Button>
                  <Button type={"submit"} variant={"primary"}>
                    {t("profile.mobileModal.verify")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        </Formik>
      ) : undefined}
    </Modal>
  );
};

export { MobileModal };
