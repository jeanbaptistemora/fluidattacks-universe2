import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useEffect } from "react";

import { ComponentField } from "./ComponentField";
import { EntryPointField } from "./EntryPointField";
import { EnvironmentUrlField } from "./EnvironmentUrlField";
import { RootField } from "./RootField";
import type { IFormValues, IHandleAdditionModalFormProps, Root } from "./types";
import { getGitRootHost, getUrlRootHost, isGitRoot, isURLRoot } from "./utils";

import { ModalConfirm } from "components/Modal";
import { Col100, Col50, Row } from "styles/styledComponents";

const HandleAdditionModalForm: React.FC<IHandleAdditionModalFormProps> = (
  props: IHandleAdditionModalFormProps
): JSX.Element => {
  const { handleCloseModal, host, roots, setHost } = props;

  const {
    values: { environmentUrl, rootId },
    submitForm,
    setFieldValue,
  } = useFormikContext<IFormValues>();

  const selectedRoot = _.isUndefined(rootId)
    ? undefined
    : roots.filter((root: Root): boolean => root.id === rootId)[0];

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
        <Col50>
          <RootField roots={roots} />
        </Col50>
        <Col50>
          <EnvironmentUrlField selectedRoot={selectedRoot} />
        </Col50>
      </Row>
      <Row>
        <Col100>
          <ComponentField host={host} />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <EntryPointField />
        </Col100>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleAdditionModalForm };
