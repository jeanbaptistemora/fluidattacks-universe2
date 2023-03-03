import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useEffect } from "react";

import { ComponentField } from "./ComponentField";
import { EntryPointField } from "./EntryPointField";
import { EnvironmentUrlField } from "./EnvironmentUrlField";
import { RootField } from "./RootField";
import type { IFormValues, IHandleAdditionModalFormProps, Root } from "./types";
import { getGitRootHost, getUrlRootHost, isGitRoot, isURLRoot } from "./utils";

import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";

const HandleAdditionModalForm: React.FC<IHandleAdditionModalFormProps> = (
  props: IHandleAdditionModalFormProps
): JSX.Element => {
  const { handleCloseModal, host, roots, setHost } = props;

  const {
    values: { environmentUrl, rootNickname },
    submitForm,
    setFieldValue,
  } = useFormikContext<IFormValues>();

  const selectedRoot = _.isUndefined(rootNickname)
    ? undefined
    : roots.filter((root: Root): boolean => root.nickname === rootNickname)[0];

  useEffect((): void => {
    function getNewHost(): string | undefined {
      if (_.isUndefined(selectedRoot)) {
        return undefined;
      } else if (isGitRoot(selectedRoot) && !_.isUndefined(environmentUrl)) {
        return getGitRootHost(environmentUrl);
      } else if (isURLRoot(selectedRoot)) {
        return getUrlRootHost(selectedRoot);
      }

      return undefined;
    }
    const newHost: string | undefined = getNewHost();
    setHost(newHost);
  }, [environmentUrl, selectedRoot, setHost]);
  useEffect((): void => {
    if (!_.isUndefined(selectedRoot)) {
      setFieldValue("environmentUrl", "");
    }
  }, [selectedRoot, setFieldValue]);

  return (
    <Form id={"addToeInput"}>
      <Row>
        <Col>
          <RootField roots={roots} />
        </Col>
        <Col>
          <EnvironmentUrlField selectedRoot={selectedRoot} />
        </Col>
      </Row>
      <Row>
        <Col>
          <ComponentField host={host} />
        </Col>
      </Row>
      <Row>
        <Col>
          <EntryPointField />
        </Col>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleAdditionModalForm };
