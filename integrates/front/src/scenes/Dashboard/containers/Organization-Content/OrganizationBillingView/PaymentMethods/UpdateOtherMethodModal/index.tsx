/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
import { Field, Form, Formik } from "formik";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { mixed, object, string } from "yup";

import { Input, InputFile } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { getCountries } from "utils/countries";
import type { ICountry } from "utils/countries";
import { FormikDropdown, FormikText } from "utils/forms/fields";

interface IUpdateOtherMethodModalProps {
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
  initialValues: {
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
              <div>
                <ControlLabel>
                  <RequiredField>{"*"}&nbsp;</RequiredField>
                  {t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.businessName"
                  )}
                </ControlLabel>
                <Input name={"businessName"} type={"text"} />
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
                  {countries.map(
                    (country): JSX.Element => (
                      <option key={country.id} value={country.name}>
                        {country.name}
                      </option>
                    )
                  )}
                </Field>
              </div>
              {states.length > 0 ? (
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
              ) : undefined}
              {cities.length > 0 ? (
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
              ) : undefined}
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
                    <InputFile
                      accept={
                        "application/pdf,application/zip,image/gif,image/jpg,image/png"
                      }
                      id={"rut"}
                      label={t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.rut"
                      )}
                      name={"rutList"}
                      required={true}
                    />
                  </div>
                </React.Fragment>
              ) : (
                <div>
                  <InputFile
                    accept={
                      "application/pdf,application/zip,image/gif,image/jpg,image/png"
                    }
                    id={"taxId"}
                    label={t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.taxId"
                    )}
                    name={"taxIdList"}
                    required={true}
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
