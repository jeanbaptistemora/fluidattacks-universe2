import { Form, useFormikContext } from "formik";
import React from "react";

import { FilenameField } from "./FilenameField";
import { LastAuthorField } from "./LastAuthorField";
import { LastCommitField } from "./LastCommitField";
import { LinesOfCodeField } from "./LinesOfCodeField";
import { ModifiedDateField } from "./ModifiedDateField";
import { RootField } from "./RootField";
import type { IFormValues, IHandleAdditionModalFormProps } from "./types";

import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";

const HandleAdditionModalForm: React.FC<IHandleAdditionModalFormProps> = (
  props: IHandleAdditionModalFormProps
): JSX.Element => {
  const { handleCloseModal, roots } = props;

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"addToeLines"}>
      <Row>
        <Col>
          <RootField roots={roots} />
        </Col>
      </Row>
      <Row>
        <Col>
          <FilenameField />
        </Col>
      </Row>
      <Row>
        <Col>
          <LinesOfCodeField />
        </Col>
      </Row>
      <Row>
        <Col>
          <LastAuthorField />
        </Col>
      </Row>
      <Row>
        <Col>
          <LastCommitField />
        </Col>
      </Row>
      <Row>
        <Col>
          <ModifiedDateField />
        </Col>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleAdditionModalForm };
