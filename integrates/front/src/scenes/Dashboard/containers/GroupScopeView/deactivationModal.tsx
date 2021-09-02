import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { DEACTIVATE_ROOT, MOVE_ROOT } from "./queries";
import type { Root } from "./types";
import { isGitRoot, isIPRoot } from "./utils";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import {
  FormikAutocompleteText,
  FormikDropdown,
  FormikText,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const getRootDisplayName = (root: Root): string => {
  if (isGitRoot(root)) {
    return `${root.nickname} - ${root.url}`;
  } else if (isIPRoot(root)) {
    return `${root.nickname} - ${root.address}`;
  }

  return `${root.nickname} - ${root.host}`;
};

interface IDeactivationModalProps {
  groupName: string;
  rootId: string;
  roots: Root[];
  onClose: () => void;
  onUpdate: () => void;
}

export const DeactivationModal: React.FC<IDeactivationModalProps> = ({
  groupName,
  rootId,
  roots,
  onClose,
  onUpdate,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [deactivateRoot] = useMutation(DEACTIVATE_ROOT, {
    onCompleted: (): void => {
      onClose();
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (
          error.message ===
          "Exception - A root with open vulns can't be deactivated"
        ) {
          msgError(t("group.scope.common.errors.hasOpenVulns"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't deactivate root", error);
        }
      });
    },
  });

  const [moveRoot] = useMutation(MOVE_ROOT, {
    onCompleted: (): void => {
      onClose();
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't move root", error);
      });
    },
  });

  const suggestions = roots
    .filter((root): boolean => root.id !== rootId && root.state === "ACTIVE")
    .map(getRootDisplayName);

  const validations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      then: string().required(t("validations.required")),
    }),
    reason: string().required(t("validations.required")),
    targetRoot: string().when("reason", {
      is: "MOVED_TO_ANOTHER_ROOT",
      then: string()
        .required(t("validations.required"))
        .oneOf(suggestions, t("validations.oneOf")),
    }),
  });

  const handleSubmit = useCallback(
    async (values: Record<string, string>): Promise<void> => {
      const matchingSuggestion = roots.find(
        (root): boolean => values.targetRoot === getRootDisplayName(root)
      ) as Root;

      if (values.reason === "MOVED_TO_ANOTHER_ROOT") {
        await moveRoot({
          variables: {
            groupName,
            id: rootId,
            targetId: matchingSuggestion.id,
          },
        });
      } else {
        await deactivateRoot({
          variables: {
            groupName,
            id: rootId,
            other: values.other,
            reason: values.reason,
          },
        });
      }
    },
    [deactivateRoot, groupName, moveRoot, rootId, roots]
  );

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("group.scope.common.deactivation.title")}
        onEsc={onClose}
        open={true}
      >
        <Formik
          initialValues={{ other: "", reason: "", targetRoot: "" }}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          {({ dirty, isSubmitting, values }): JSX.Element => (
            <Form>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.scope.common.deactivation.reason.label")}
                    </ControlLabel>
                    <Field component={FormikDropdown} name={"reason"}>
                      <option value={""} />
                      <option value={"OUT_OF_SCOPE"}>
                        {t("group.scope.common.deactivation.reason.scope")}
                      </option>
                      <option value={"REGISTERED_BY_MISTAKE"}>
                        {t("group.scope.common.deactivation.reason.mistake")}
                      </option>
                      <option value={"OTHER"}>
                        {t("group.scope.common.deactivation.reason.other")}
                      </option>
                    </Field>
                  </FormGroup>
                  {values.reason === "OTHER" ? (
                    <FormGroup>
                      <ControlLabel>
                        {t("group.scope.common.deactivation.other")}
                      </ControlLabel>
                      <Field component={FormikText} name={"other"} />
                    </FormGroup>
                  ) : undefined}
                  {values.reason === "MOVED_TO_ANOTHER_ROOT" ? (
                    <FormGroup>
                      <ControlLabel>
                        {t("group.scope.common.deactivation.targetRoot")}
                      </ControlLabel>
                      <Field
                        component={FormikAutocompleteText}
                        name={"targetRoot"}
                        placeholder={t(
                          "group.scope.common.deactivation.targetPlaceholder"
                        )}
                        suggestions={suggestions}
                      />
                    </FormGroup>
                  ) : undefined}
                </Col100>
              </Row>
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={onClose}>
                      {t("confirmmodal.cancel")}
                    </Button>
                    <Button disabled={!dirty || isSubmitting} type={"submit"}>
                      {t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};
