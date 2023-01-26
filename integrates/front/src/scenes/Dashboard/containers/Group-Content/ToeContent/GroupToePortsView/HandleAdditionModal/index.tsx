import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { ADD_TOE_PORT, GET_ROOTS } from "./queries";
import type {
  IAddToePortResultAttr,
  IFormValues,
  IHandleAdditionModalProps,
  IIPRootAttr,
  Root,
} from "./types";
import { isActiveIPRoot, isIPRoot } from "./utils";

import { Input } from "components/Input/Fields/Input";
import { Select } from "components/Input/Fields/Select";
import { Col } from "components/Layout";
import { Row } from "components/Layout/Row";
import { Modal, ModalConfirm } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { regExps } from "utils/validations";

const HandleAdditionModal: React.FC<IHandleAdditionModalProps> = ({
  groupName,
  handleCloseModal,
  refetchData,
}: IHandleAdditionModalProps): JSX.Element => {
  const { t } = useTranslation();

  // States
  const [isSubmitting, setIsSubmitting] = useState(false);

  // GraphQL queries
  const { data: rootsData } = useQuery<{ group: { roots: Root[] } }>(
    GET_ROOTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );

  // Generate data
  const activeIPRoots =
    rootsData === undefined
      ? []
      : rootsData.group.roots.filter(isIPRoot).filter(isActiveIPRoot);
  const activeIPRootAddress = Object.fromEntries(
    activeIPRoots.map((root: IIPRootAttr): [string, string] => [
      root.id,
      root.address,
    ])
  );

  // GraphQL mutations
  const [handleAddToePort] = useMutation<IAddToePortResultAttr>(ADD_TOE_PORT, {
    onCompleted: (data: IAddToePortResultAttr): void => {
      setIsSubmitting(false);
      if (data.addToePort.success) {
        msgSuccess(
          t("group.toe.ports.addModal.alerts.success"),
          t("groupAlerts.titleSuccess")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: (errors: ApolloError): void => {
      setIsSubmitting(false);
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message === "Exception - Toe port already exists") {
          msgError(t("group.toe.ports.addModal.alerts.alreadyExists"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding toe port", error);
        }
      });
    },
  });

  // Handle actions
  const handleSubmit = useCallback(
    (values: IFormValues): void => {
      setIsSubmitting(true);
      void handleAddToePort({
        variables: {
          address: activeIPRootAddress[values.rootId],
          groupName,
          port: _.toInteger(values.port),
          rootId: values.rootId,
        },
      });
    },
    [activeIPRootAddress, groupName, handleAddToePort]
  );

  const handleInteger = useCallback(
    (event: React.KeyboardEvent<HTMLInputElement>): void => {
      if (
        event.key.length > 1 ||
        /\d/u.test(event.key) ||
        event.key === "Control" ||
        event.key.toLocaleLowerCase() === "c" ||
        event.key.toLocaleLowerCase() === "v"
      )
        return;
      event.preventDefault();
    },
    []
  );

  const handleIntegerPaste = useCallback(
    (event: React.ClipboardEvent<HTMLInputElement>): void => {
      const data = event.clipboardData.getData("Text");
      if (/^\d*$/u.test(data)) return;

      event.preventDefault();
    },
    []
  );

  return (
    <React.StrictMode>
      {rootsData === undefined ? undefined : (
        <Modal open={true} title={t("group.toe.ports.addModal.title")}>
          <Formik
            initialValues={{
              port: "",
              rootId: activeIPRoots.length > 0 ? activeIPRoots[0].id : "",
            }}
            name={"addToePort"}
            onSubmit={handleSubmit}
            validationSchema={object().shape({
              port: string()
                .required(t("validations.required"))
                .matches(regExps.numeric, t("validations.numeric"))
                .test(
                  "isValidPortRange",
                  t("validations.portRange"),
                  (value?: string): boolean => {
                    if (value === undefined || _.isEmpty(value)) {
                      return false;
                    }
                    const port = _.toInteger(value);

                    return port >= 0 && port <= 65535;
                  }
                ),
              rootId: string().required(t("validations.required")),
            })}
          >
            {({ dirty }): JSX.Element => {
              return (
                <Form id={"addToePort"}>
                  <Row>
                    <Col lg={100} md={100} sm={100}>
                      <Select
                        label={t("group.toe.ports.addModal.fields.IPRoot")}
                        name={"rootId"}
                      >
                        {activeIPRoots.map(
                          (root: IIPRootAttr): JSX.Element => (
                            <option key={root.id} value={root.id}>
                              {`${root.nickname} - ${root.address}`}
                            </option>
                          )
                        )}
                      </Select>
                    </Col>
                  </Row>
                  <Row>
                    <Col lg={100} md={100} sm={100}>
                      <Input
                        label={t("group.toe.ports.addModal.fields.port")}
                        name={"port"}
                        onKeyDown={handleInteger}
                        onPaste={handleIntegerPaste}
                        type={"number"}
                      />
                    </Col>
                  </Row>
                  <br />
                  <ModalConfirm
                    disabled={isSubmitting || !dirty}
                    onCancel={handleCloseModal}
                  />
                </Form>
              );
            }}
          </Formik>
        </Modal>
      )}
    </React.StrictMode>
  );
};

export { HandleAdditionModal };
