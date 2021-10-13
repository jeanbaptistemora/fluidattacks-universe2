import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { DEACTIVATE_ROOT, GET_GROUPS, MOVE_ROOT } from "./queries";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import {
  Alert,
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

interface IDeactivationModalProps {
  groupName: string;
  rootId: string;
  onClose: () => void;
  onUpdate: () => void;
}

export const DeactivationModal: React.FC<IDeactivationModalProps> = ({
  groupName,
  rootId,
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

  interface IGroup {
    name: string;
    organization: string;
    service: string;
  }
  interface IOrganization {
    groups: IGroup[];
  }

  const { data } = useQuery<{ me: { organizations: IOrganization[] } }>(
    GET_GROUPS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load group names", error);
        });
      },
    }
  );
  const groups =
    data === undefined
      ? []
      : data.me.organizations.reduce<IGroup[]>(
          (previousValue, currentValue): IGroup[] => [
            ...previousValue,
            ...currentValue.groups,
          ],
          []
        );

  const currentGroup = groups.find(
    (group): boolean => group.name === groupName
  );
  const suggestions =
    currentGroup === undefined
      ? []
      : groups
          .filter(
            (group): boolean =>
              group.name !== currentGroup.name &&
              group.organization === currentGroup.organization &&
              group.service === currentGroup.service
          )
          .map((group): string => group.name);

  const validations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      then: string().required(t("validations.required")),
    }),
    reason: string().required(t("validations.required")),
    targetRoot: string().when("reason", {
      is: "MOVED_TO_ANOTHER_GROUP",
      then: string()
        .required(t("validations.required"))
        .oneOf(suggestions, t("validations.oneOf")),
    }),
  });

  const handleSubmit = useCallback(
    async (values: Record<string, string>): Promise<void> => {
      if (values.reason === "MOVED_TO_ANOTHER_GROUP") {
        await moveRoot({
          variables: {
            groupName,
            id: rootId,
            targetId: values.targetGroup,
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
    [deactivateRoot, groupName, moveRoot, rootId]
  );

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("group.scope.common.deactivation.title")}
        onEsc={onClose}
        open={true}
      >
        <ConfirmDialog
          message={t("group.scope.common.deactivation.confirm")}
          title={t("group.scope.common.confirm")}
        >
          {(confirm): React.ReactNode => {
            async function confirmAndSubmit(
              values: Record<string, string>
            ): Promise<void> {
              if (
                ["OUT_OF_SCOPE", "REGISTERED_BY_MISTAKE"].includes(
                  values.reason
                )
              ) {
                return new Promise((resolve): void => {
                  confirm(
                    (): void => {
                      resolve(handleSubmit(values));
                    },
                    (): void => {
                      resolve();
                    }
                  );
                });
              }

              return handleSubmit(values);
            }

            return (
              <Formik
                initialValues={{ other: "", reason: "", targetRoot: "" }}
                onSubmit={confirmAndSubmit}
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
                              {t(
                                "group.scope.common.deactivation.reason.scope"
                              )}
                            </option>
                            <option value={"REGISTERED_BY_MISTAKE"}>
                              {t(
                                "group.scope.common.deactivation.reason.mistake"
                              )}
                            </option>
                            <option value={"OTHER"}>
                              {t(
                                "group.scope.common.deactivation.reason.other"
                              )}
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
                        {values.reason === "MOVED_TO_ANOTHER_GROUP" ? (
                          <FormGroup>
                            <ControlLabel>
                              {t("group.scope.common.deactivation.targetGroup")}
                            </ControlLabel>
                            <Field
                              component={FormikAutocompleteText}
                              name={"targetGroup"}
                              placeholder={t(
                                "group.scope.common.deactivation.targetPlaceholder"
                              )}
                              suggestions={suggestions}
                            />
                          </FormGroup>
                        ) : undefined}
                        {["OUT_OF_SCOPE", "REGISTERED_BY_MISTAKE"].includes(
                          values.reason
                        ) ? (
                          <Alert>
                            {t("group.scope.common.deactivation.warning")}
                          </Alert>
                        ) : undefined}
                        {values.reason === "MOVED_TO_ANOTHER_GROUP" ? (
                          <Alert>{t("group.scope.common.changeWarning")}</Alert>
                        ) : undefined}
                      </Col100>
                    </Row>
                    <Row>
                      <Col100>
                        <ButtonToolbar>
                          <Button onClick={onClose}>
                            {t("confirmmodal.cancel")}
                          </Button>
                          <Button
                            disabled={!dirty || isSubmitting}
                            type={"submit"}
                          >
                            {t("confirmmodal.proceed")}
                          </Button>
                        </ButtonToolbar>
                      </Col100>
                    </Row>
                  </Form>
                )}
              </Formik>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </React.StrictMode>
  );
};
