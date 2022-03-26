import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import type { IFindingsQuery } from "../AffectedReattackAccordion/types";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";

interface IEventsDataset {
  group: {
    events: {
      detail: string;
      eventStatus: string;
      id: string;
    }[];
    name: string;
  };
}

interface IUpdateAffectedValues {
  eventId: string;
  affectedReattacks: string[];
}

interface IUpdateAffectedModalProps {
  eventsInfo: IEventsDataset;
  findingsInfo: IFindingsQuery;
  onClose: () => void;
  onSubmit: (values: IUpdateAffectedValues) => Promise<void>;
}

export const UpdateAffectedModal: React.FC<IUpdateAffectedModalProps> = ({
  eventsInfo,
  findingsInfo,
  onClose,
  onSubmit,
}: IUpdateAffectedModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    affectedReattacks: array().when("affectsReattacks", {
      is: true,
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
    eventId: string().required(),
  });

  const eventOptions = eventsInfo.group.events.map(
    ({ detail, eventStatus, id }): JSX.Element => {
      if (eventStatus !== "SOLVED") {
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
                  {t("group.events.form.affectedReattacks.description")}
                </ControlLabel>
                <AffectedReattackAccordion
                  findings={findingsInfo.group.findings}
                />
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
