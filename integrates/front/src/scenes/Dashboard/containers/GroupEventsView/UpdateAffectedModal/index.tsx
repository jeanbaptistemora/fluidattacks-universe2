import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import type { IUpdateAffectedModalProps, IUpdateAffectedValues } from "./types";

import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";

export const UpdateAffectedModal: React.FC<IUpdateAffectedModalProps> = ({
  eventsInfo,
  findings,
  onClose,
  onSubmit,
}: IUpdateAffectedModalProps): JSX.Element => {
  const { t } = useTranslation();

  // Null check
  const events = eventsInfo?.group.events ?? [];

  const eventOptions = events.map(
    ({ detail, eventStatus, id }): JSX.Element => {
      if (eventStatus.toUpperCase() !== "SOLVED") {
        return <option value={id}>{detail}</option>;
      }

      return <div key={id} />;
    }
  );

  async function handleSubmit(values: IUpdateAffectedValues): Promise<void> {
    return onSubmit({
      ...values,
    });
  }

  const validations = object().shape({
    affectedReattacks: array().min(1, t("validations.someRequired")),
    eventId: string().required(t("validations.required")),
  });

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("group.events.form.affectedReattacks.title")}
    >
      <Formik
        initialValues={{
          affectedReattacks: [],
          eventId: "",
        }}
        name={"updateAffected"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <Row>
              <FormGroup>
                <ControlLabel>
                  {t("group.events.form.affectedReattacks.eventSection")}
                </ControlLabel>
                <Field component={FormikDropdown} name={"eventId"}>
                  <option value={""} />
                  {eventOptions}
                </Field>
              </FormGroup>
              <FormGroup>
                <ControlLabel>
                  {t("group.events.form.affectedReattacks.sectionTitle")}
                </ControlLabel>
                <br />
                {t("group.events.form.affectedReattacks.selection")}
                <br />
                <br />
                <AffectedReattackAccordion findings={findings} />
              </FormGroup>
            </Row>
            <ModalFooter>
              <Button onClick={onClose} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Button
                disabled={!dirty || isSubmitting}
                type={"submit"}
                variant={"primary"}
              >
                {t("confirmmodal.proceed")}
              </Button>
            </ModalFooter>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
