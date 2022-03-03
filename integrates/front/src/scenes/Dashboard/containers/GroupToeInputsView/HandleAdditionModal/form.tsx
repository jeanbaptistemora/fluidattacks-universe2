import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { ComponentField } from "./ComponentField";
import { EntryPointField } from "./EntryPointField";
import { EnvironmentUrlField } from "./EnvironmentUrlField";
import { RootField } from "./RootField";
import type { IFormValues, IHandleAdditionModalFormProps, Root } from "./types";
import {
  getGitRootHost,
  getIpRootHost,
  getUrlRootHost,
  isGitRoot,
  isIPRoot,
  isURLRoot,
} from "./utils";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";

const HandleAdditionModalForm: React.FC<IHandleAdditionModalFormProps> = (
  props: IHandleAdditionModalFormProps
): JSX.Element => {
  const { handleCloseModal, host, roots, setHost } = props;

  const { t } = useTranslation();

  const {
    values: { environmentUrl, rootId },
    submitForm,
    setFieldValue,
  } = useFormikContext<IFormValues>();

  const selectedRoot = _.isUndefined(rootId)
    ? undefined
    : roots.filter((root: Root): boolean => root.id === rootId)[0];

  useEffect((): void => {
    const newHost = _.isUndefined(selectedRoot)
      ? undefined
      : isGitRoot(selectedRoot) && !_.isUndefined(environmentUrl)
      ? getGitRootHost(environmentUrl)
      : isIPRoot(selectedRoot)
      ? getIpRootHost(selectedRoot)
      : isURLRoot(selectedRoot)
      ? getUrlRootHost(selectedRoot)
      : undefined;
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
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button onClick={handleCloseModal} variant={"secondary"}>
              {t("group.toe.inputs.addModal.close")}
            </Button>
            <Button onClick={submitForm} variant={"primary"}>
              {t("group.toe.inputs.addModal.procced")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </Row>
    </Form>
  );
};

export { HandleAdditionModalForm };
