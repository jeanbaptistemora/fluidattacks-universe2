import { Form, useFormikContext } from "formik";
import React from "react";

import { FilenameField } from "./FilenameField";
import { LastAuthorField } from "./LastAuthorField";
import { LastCommitField } from "./LastCommitField";
import { LinesOfCodeField } from "./LinesOfCodeField";
import { ModifiedDateField } from "./ModifiedDateField";
import { RootField } from "./RootField";
import type { IFormValues, IHandleAdditionModalFormProps } from "./types";

import { ModalConfirm } from "components/Modal";
import { Col100, Row } from "styles/styledComponents";

const HandleAdditionModalForm: React.FC<IHandleAdditionModalFormProps> = (
  props: IHandleAdditionModalFormProps
): JSX.Element => {
  const { handleCloseModal, roots } = props;

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"addToeLines"}>
      <Row>
        <Col100>
          <RootField roots={roots} />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <FilenameField />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <LinesOfCodeField />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <LastAuthorField />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <LastCommitField />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <ModifiedDateField />
        </Col100>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleAdditionModalForm };
