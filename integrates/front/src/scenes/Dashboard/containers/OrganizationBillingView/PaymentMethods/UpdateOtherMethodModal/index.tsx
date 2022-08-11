/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
import { Field, Form, Formik } from "formik";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { boolean, mixed, object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { countries } from "utils/countries";
import type { ICountries } from "utils/countries";
import {
  FormikDropdown,
  FormikFileInput,
  FormikText,
} from "utils/forms/fields";

interface IUpdateOtherMethodModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardExpirationMonth: string;
    cardExpirationYear: string;
    makeDefault: boolean;
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  }) => Promise<void>;
  initialValues: {
    cardExpirationMonth: string;
    cardExpirationYear: string;
    makeDefault: boolean;
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  };
}

export const UpdateOtherMethodModal: React.FC<IUpdateOtherMethodModalProps> = ({
  onClose,
  onSubmit,
  initialValues,
}: IUpdateOtherMethodModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [countriesData, setCountriesData] = useState<ICountries[] | undefined>(
    undefined
  );

  const [states, setStates] = useState<string[] | undefined>(undefined);
  const [cities, setCities] = useState<string[] | undefined>(undefined);

  const validations = object().shape({
    businessName: string()
      .required()
      .max(60)
      .matches(
        /^[a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>][a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>=]+$/u
      ),
    cardExpirationMonth: string(),
    cardExpirationYear: string(),
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
    makeDefault: boolean(),
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
    if (countriesData) {
      setStates(
        countriesData
          .filter(
            (country): boolean => country.name === initialValues.country
          )[0]
          .states.map((state): string => state.name)
      );
      if ((states ?? []).length > 0) {
        setCities(
          countriesData
            .filter(
              (country): boolean => country.name === initialValues.country
            )[0]
            .states.filter(
              (state): boolean => state.name === initialValues.state
            )[0]
            .cities.map((city): string => city.name)
        );
      }
    }
  }, [
    countriesData,
    initialValues,
    setCities,
    setCountriesData,
    setStates,
    states,
  ]);

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.update.modal.update")}
    >
      <Formik
        initialValues={initialValues}
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
              <div>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.businessName"
                  )}
                </ControlLabel>
                <Field
                  component={FormikText}
                  name={"businessName"}
                  type={"text"}
                />
              </div>
              <div>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.country"
                  )}
                </ControlLabel>
              </div>
              <div
                onClick={changeCountry}
                onKeyDown={changeCountry}
                role={"listitem"}
              >
                <Field component={FormikDropdown} name={"country"}>
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
                </Field>
              </div>
              {states === undefined
                ? undefined
                : states.length > 0 && (
                    <React.Fragment>
                      <div>
                        <ControlLabel>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          {t(
                            "organization.tabs.billing.paymentMethods.add.otherMethods.state"
                          )}
                        </ControlLabel>
                      </div>
                      <div
                        onClick={changeState}
                        onKeyDown={changeState}
                        role={"listitem"}
                      >
                        <Field component={FormikDropdown} name={"state"}>
                          <option value={""}>{""}</option>
                          {states.map(
                            (state): JSX.Element => (
                              <option key={state} value={state}>
                                {state}
                              </option>
                            )
                          )}
                        </Field>
                      </div>
                    </React.Fragment>
                  )}
              {cities === undefined
                ? undefined
                : cities.length > 0 && (
                    <div>
                      <ControlLabel>
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                        {t(
                          "organization.tabs.billing.paymentMethods.add.otherMethods.city"
                        )}
                      </ControlLabel>
                      <Field component={FormikDropdown} name={"city"}>
                        <option value={""}>{""}</option>
                        {cities.map(
                          (city): JSX.Element => (
                            <option key={city} value={city}>
                              {city}
                            </option>
                          )
                        )}
                      </Field>
                    </div>
                  )}
              {values.country === "Colombia" ? (
                <React.Fragment>
                  <div>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.email"
                      )}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      name={"email"}
                      type={"text"}
                    />
                  </div>
                  <div>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.rut"
                      )}
                    </ControlLabel>
                    <Field
                      accept={
                        "application/pdf,application/zip,image/gif,image/jpg,image/png"
                      }
                      component={FormikFileInput}
                      id={"rut"}
                      name={"rutList"}
                    />
                  </div>
                </React.Fragment>
              ) : (
                <div>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.taxId"
                    )}
                  </ControlLabel>
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
              <ModalConfirm
                disabled={!dirty || isSubmitting}
                onCancel={onClose}
              />
            </Form>
          );
        }}
      </Formik>
    </Modal>
  );
};
