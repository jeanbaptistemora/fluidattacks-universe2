import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import type { FC, ReactNode } from "react";
import React, {
  Fragment,
  StrictMode,
  useCallback,
  useEffect,
  useState,
} from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import {
  DEACTIVATE_ROOT,
  GET_GROUPS,
  GET_ROOTS_VULNS,
  MOVE_ROOT,
} from "./queries";

import { Alert } from "components/Alert";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Input, Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { Can } from "utils/authz/Can";
import { FormikAutocompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IDeactivationModalProps {
  groupName: string;
  rootId: string;
  onClose: () => void;
  onUpdate: () => void;
}

interface IRootsVulnsData {
  group: {
    roots: {
      id: string;
      vulnerabilities: {
        id: string;
        vulnerabilityType: string;
      }[];
    }[];
  };
}

export const DeactivationModal: FC<IDeactivationModalProps> = ({
  groupName,
  rootId,
  onClose,
  onUpdate,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [sastVulnsToBeClosed, setSastVulnsToBeClosed] = useState<
    number | undefined
  >(0);
  const [dastVulnsToBeClosed, setDastVulnsToBeClosed] = useState<
    number | undefined
  >(0);

  const [deactivateRoot] = useMutation(DEACTIVATE_ROOT, {
    onCompleted: (): void => {
      onClose();
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (error.message === "Exception - Error empty value is not valid") {
          msgError(t("group.scope.common.deactivation.errors.changed"));
          onUpdate();
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't deactivate root", error);
        }
      });
    },
  });

  const [moveRoot] = useMutation(MOVE_ROOT, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.common.deactivation.success.message"),
        t("group.scope.common.deactivation.success.title")
      );
      onClose();
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        switch (error.message) {
          case "Exception - Active root with the same Nickname already exists":
            msgError(t("group.scope.common.errors.duplicateNickname"));
            break;
          case "Exception - Root with the same URL/branch already exists":
            msgError(t("group.scope.common.errors.duplicateUrlInTargetGroup"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't move root", error);
        }
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

  const { data: rootsVulnsData } = useQuery<IRootsVulnsData>(GET_ROOTS_VULNS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load root vulnerabilities", error);
      });
    },
    variables: { groupName },
  });

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
    targetGroupName: string().when("reason", {
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
            targetGroupName: values.targetGroupName,
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

  useEffect((): void => {
    const currentRootVulns = rootsVulnsData?.group.roots.find(
      (item): boolean => item.id === rootId
    );
    const currentRootSastVulns = currentRootVulns?.vulnerabilities.filter(
      (item): boolean => Object.values(item).includes("lines")
    );
    const currentRootDastVulns = currentRootVulns?.vulnerabilities.filter(
      (item): boolean => !Object.values(item).includes("lines")
    );
    setSastVulnsToBeClosed(currentRootSastVulns?.length);
    setDastVulnsToBeClosed(currentRootDastVulns?.length);
  }, [rootId, rootsVulnsData, setDastVulnsToBeClosed, setSastVulnsToBeClosed]);

  return (
    <StrictMode>
      <Modal
        onClose={onClose}
        open={true}
        title={t("group.scope.common.deactivation.title")}
      >
        <ConfirmDialog
          message={t("group.scope.common.deactivation.confirm")}
          title={t("group.scope.common.confirm")}
        >
          {(confirm): ReactNode => {
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
                initialValues={{ other: "", reason: "", targetGroupName: "" }}
                onSubmit={confirmAndSubmit}
                validationSchema={validations}
              >
                {({ dirty, isSubmitting, values }): JSX.Element => (
                  <Form>
                    <Gap disp={"block"} mv={12}>
                      <Select
                        label={t(
                          "group.scope.common.deactivation.reason.label"
                        )}
                        name={"reason"}
                      >
                        <option value={""} />
                        <option value={"REGISTERED_BY_MISTAKE"}>
                          {t("group.scope.common.deactivation.reason.mistake")}
                        </option>
                        <Can do={"api_mutations_move_root_mutate"}>
                          <option value={"MOVED_TO_ANOTHER_GROUP"}>
                            {t("group.scope.common.deactivation.reason.moved")}
                          </option>
                        </Can>
                        <option value={"OTHER"}>
                          {t("group.scope.common.deactivation.reason.other")}
                        </option>
                      </Select>
                      {values.reason === "OTHER" ? (
                        <Input
                          label={t("group.scope.common.deactivation.other")}
                          name={"other"}
                        />
                      ) : undefined}
                      {values.reason === "MOVED_TO_ANOTHER_GROUP" ? (
                        <div>
                          <Text mb={1}>
                            {t("group.scope.common.deactivation.targetGroup")}
                          </Text>
                          <Field
                            component={FormikAutocompleteText}
                            name={"targetGroupName"}
                            placeholder={t(
                              "group.scope.common.deactivation.targetPlaceholder"
                            )}
                            suggestions={suggestions}
                          />
                        </div>
                      ) : undefined}
                      {["OUT_OF_SCOPE", "REGISTERED_BY_MISTAKE"].includes(
                        values.reason
                      ) ? (
                        <Fragment>
                          <Alert>
                            {t("group.scope.common.deactivation.warning")}
                          </Alert>
                          <Alert>
                            <div>
                              {sastVulnsToBeClosed === undefined ? (
                                t("group.scope.common.deactivation.loading")
                              ) : (
                                <strong>{sastVulnsToBeClosed}</strong>
                              )}
                              {t(
                                "group.scope.common.deactivation.closedSastVulnsWarning"
                              )}
                              <br />
                              {dastVulnsToBeClosed === undefined ? (
                                t("group.scope.common.deactivation.loading")
                              ) : (
                                <strong>{dastVulnsToBeClosed}</strong>
                              )}
                              {t(
                                "group.scope.common.deactivation.closedDastVulnsWarning"
                              )}
                            </div>
                          </Alert>
                        </Fragment>
                      ) : undefined}
                      {values.reason === "MOVED_TO_ANOTHER_GROUP" ? (
                        <Alert>{t("group.scope.common.changeWarning")}</Alert>
                      ) : undefined}
                      <ModalConfirm
                        disabled={!dirty || isSubmitting}
                        onCancel={onClose}
                      />
                    </Gap>
                  </Form>
                )}
              </Formik>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </StrictMode>
  );
};