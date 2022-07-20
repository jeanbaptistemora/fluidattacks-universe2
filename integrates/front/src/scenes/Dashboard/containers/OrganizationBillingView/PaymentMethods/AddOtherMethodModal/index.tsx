/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
import { Field, Form, Formik } from "formik";
import React, { Fragment, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { mixed, object, string } from "yup";

import { Button } from "components/Button";
import { Input, Select } from "components/Input";
import { Gap, Hr } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { countries } from "utils/countries";
import type { ICountries } from "utils/countries";
import { FormikFileInput } from "utils/forms/fields";

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

  function goToCreditCard(): void {
    onChangeMethod("CREDIT_CARD");
  }

  const [countriesData, setCountriesData] = useState<ICountries[] | undefined>(
    undefined
  );
  const [states, setStates] = useState<string[] | undefined>(undefined);
  const [cities, setCities] = useState<string[] | undefined>(undefined);

  const validations = object().shape({
    businessName: string().required(),
    city: string().test(
      "isRequired",
      t("validations.required"),
      (value): boolean => {
        if (cities === undefined) {
          return true;
        }

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
        if (states === undefined) {
          return true;
        }

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
    async function getData(): Promise<void> {
      await countries(setCountriesData);
    }
    getData().catch((): void => {
      setCountriesData(undefined);
    });
  }, [setCountriesData]);

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
            setCities(undefined);
            if (countriesData !== undefined && values.country !== "") {
              setStates(
                countriesData
                  .filter(
                    (country): boolean => country.name === values.country
                  )[0]
                  .states.map((state): string => state.name)
              );
            }
          }
          function changeState(): void {
            setFieldValue("city", "");
            if (
              countriesData !== undefined &&
              values.country !== "" &&
              values.state !== ""
            ) {
              setCities(
                countriesData
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
                    {countriesData === undefined
                      ? undefined
                      : countriesData.map(
                          (country): JSX.Element => (
                            <option key={country.id} value={country.name}>
                              {country.name}
                            </option>
                          )
                        )}
                  </Select>
                </div>
                {states === undefined || states.length === 0 ? undefined : (
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
                {cities === undefined || cities.length === 0 ? undefined : (
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
                        id={"rutList"}
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
