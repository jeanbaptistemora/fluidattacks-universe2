import { Form, useFormikContext } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { SeenFirstTimeByField } from "./SeenFirstTimeByField";
import type { IFormValues, IHandleEnumerationModalFormProps } from "./types";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

const HandleEnumerationModalForm: React.FC<IHandleEnumerationModalFormProps> = (
  props: IHandleEnumerationModalFormProps
): JSX.Element => {
  const { handleCloseModal, validStakeholders } = props;

  const { t } = useTranslation();

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"enumerateToeInput"}>
      <Row>
        <Col100>
          <SeenFirstTimeByField validStakeholders={validStakeholders} />
        </Col100>
      </Row>
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button onClick={handleCloseModal}>
              {t("group.toe.inputs.enumerateModal.close")}
            </Button>
            <Button disabled={false} onClick={submitForm}>
              {t("group.toe.inputs.enumerateModal.procced")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </Row>
    </Form>
  );
};

export { HandleEnumerationModalForm };
