import { Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import type { IUpdateAffectedModalProps, IUpdateAffectedValues } from "./types";

import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";

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
        return (
          <option key={id} value={id}>
            {detail}
          </option>
        );
      }

      return <div key={id} />;
    }
  );

  const handleSubmit = useCallback(
    async (values: IUpdateAffectedValues): Promise<void> => {
      return onSubmit({
        ...values,
      });
    },
    [onSubmit]
  );

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
            <Select
              label={t("group.events.form.affectedReattacks.eventSection")}
              name={"eventId"}
            >
              <option value={""} />
              {eventOptions}
            </Select>
            <Text mb={2} mt={2}>
              {t("group.events.form.affectedReattacks.selection")}
            </Text>
            <AffectedReattackAccordion findings={findings} />
            <ModalConfirm
              disabled={!dirty || isSubmitting}
              onCancel={onClose}
            />
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
