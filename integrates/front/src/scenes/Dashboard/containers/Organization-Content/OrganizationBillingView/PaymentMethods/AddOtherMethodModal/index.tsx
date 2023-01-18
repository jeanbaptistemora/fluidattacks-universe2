/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
import { Field, Form, Formik } from "formik";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { mixed, object, string } from "yup";

import { Button } from "components/Button";
import { Input, Select } from "components/Input";
import { Gap, Hr } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { getCountries } from "utils/countries";
import type { ICountry } from "utils/countries";
import { FormikFileInput } from "utils/forms/fields";
import { validEmail } from "utils/validations";

interface IAddOtherMethodModalProps {
  onClose: () => void;
  onSubmit: (values: {
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  }) => Promise<void>;
  onChangeMethod: React.Dispatch<
    React.SetStateAction<"CREDIT_CARD" | "OTHER_METHOD" | false>
  >;
}

export const AddOtherMethodModal = ({
  onClose,
  onSubmit,
  onChangeMethod,
}: IAddOtherMethodModalProps): JSX.Element => {
  const { t } = useTranslation();

  const goToCreditCard = useCallback((): void => {
    onChangeMethod("CREDIT_CARD");
  }, [onChangeMethod]);

  const [countries, setCountries] = useState<ICountry[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);

  const validations = object().shape({
    businessName: string()
      .required()
      .max(60)
      .matches(
        /^[a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>][a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>=]+$/u
      ),
    city: string().test(
      "isRequired",
      t("validations.required"),
      (value): boolean => {
        return cities.length === 0 || value !== undefined;
      }
    ),
    country: string().required(),
    email: string().email().when("country", {
      is: "Colombia",
      otherwise: string(),
      then: string().email().required(),
    }),
    rutList: mixed().when("country", {
      is: "Colombia",
      otherwise: mixed(),
      then: mixed().required(),
    }),
    state: string().test(
      "isRequired",
      t("validations.required"),
      (value): boolean => {
        return states.length === 0 || value !== undefined;
      }
    ),
    taxIdList: mixed().when("country", {
      is: "Colombia",
      otherwise: mixed().required(),
      then: mixed(),
    }),
  });

  useEffect((): void => {
    const loadCountries = async (): Promise<void> => {
      setCountries(await getCountries());
    };
    void loadCountries();
  }, [setCountries]);

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.otherMethods.add")}
    >
      <Formik
        initialValues={{
          businessName: "",
          city: "",
          country: "",
          email: "",
          rutList: undefined,
          state: "",
          taxIdList: undefined,
        }}
        name={"addOtherMethods"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting, setFieldValue, values }): JSX.Element => {
          function changeCountry(): void {
            setFieldValue("state", "");
            setFieldValue("city", "");
            setCities([]);
            if (values.country !== "") {
              setStates(
                countries
                  .filter(
                    (country): boolean => country.name === values.country
                  )[0]
                  .states.map((state): string => state.name)
              );
            }
          }
          function changeState(): void {
            setFieldValue("city", "");
            if (values.country !== "" && values.state !== "") {
              setCities(
                countries
                  .filter(
                    (country): boolean => country.name === values.country
                  )[0]
                  .states.filter(
                    (state): boolean => state.name === values.state
                  )[0]
                  .cities.map((city): string => city.name)
              );
            }
          }

          return (
            <Form>
              <Gap disp={"block"} mh={0} mv={12}>
                <Input
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.businessName"
                  )}
                  name={"businessName"}
                  required={true}
                />
                <div
                  onClick={changeCountry}
                  onKeyDown={changeCountry}
                  role={"listitem"}
                >
                  <Select
                    label={t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.country"
                    )}
                    name={"country"}
                    required={true}
                  >
                    <option value={""}>{""}</option>
                    {countries.map(
                      (country): JSX.Element => (
                        <option key={country.id} value={country.name}>
                          {country.name}
                        </option>
                      )
                    )}
                  </Select>
                </div>
                {states.length === 0 ? undefined : (
                  <div
                    onClick={changeState}
                    onKeyDown={changeState}
                    role={"listitem"}
                  >
                    <Select
                      label={t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.state"
                      )}
                      name={"state"}
                      required={true}
                    >
                      <option value={""}>{""}</option>
                      {states.map(
                        (state): JSX.Element => (
                          <option key={state} value={state}>
                            {state}
                          </option>
                        )
                      )}
                    </Select>
                  </div>
                )}
                {cities.length === 0 ? undefined : (
                  <Select
                    label={t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.city"
                    )}
                    name={"city"}
                    required={true}
                  >
                    <option value={""}>{""}</option>
                    {cities.map(
                      (city): JSX.Element => (
                        <option key={city} value={city}>
                          {city}
                        </option>
                      )
                    )}
                  </Select>
                )}
                {values.country === "Colombia" ? (
                  <Fragment>
                    <Input
                      label={t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.email"
                      )}
                      name={"email"}
                      required={true}
                      type={"email"}
                      validate={validEmail}
                    />
                    <div>
                      <Text mb={1}>
                        <Text disp={"inline-block"} mr={1} tone={"red"}>
                          {"*"}
                        </Text>
                        {t(
                          "organization.tabs.billing.paymentMethods.add.otherMethods.rut"
                        )}
                      </Text>
                      <Field
                        accept={
                          "application/pdf,application/zip,image/gif,image/jpg,image/png"
                        }
                        component={FormikFileInput}
                        id={"rut"}
                        name={"rutList"}
                      />
                    </div>
                  </Fragment>
                ) : (
                  <div>
                    <Text mb={1}>
                      <Text disp={"inline-block"} mr={1} tone={"red"}>
                        {"*"}
                      </Text>
                      {t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.taxId"
                      )}
                    </Text>
                    <Field
                      accept={
                        "application/pdf,application/zip,image/gif,image/jpg,image/png"
                      }
                      component={FormikFileInput}
                      id={"taxId"}
                      name={"taxIdList"}
                    />
                  </div>
                )}
              </Gap>
              <ModalConfirm
                disabled={!dirty || isSubmitting}
                onCancel={onClose}
              />
              <Hr />
              <Button
                id={"other-payment-methods"}
                onClick={goToCreditCard}
                type={"button"}
              >
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.creditCard"
                )}
              </Button>
            </Form>
          );
        }}
      </Formik>
    </Modal>
  );
};
