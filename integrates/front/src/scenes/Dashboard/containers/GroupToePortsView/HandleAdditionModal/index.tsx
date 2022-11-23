import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { GET_ROOTS } from "./queries";
import type { IHandleAdditionModalProps, IIPRootAttr, Root } from "./types";
import { isActiveIPRoot, isIPRoot } from "./utils";

import { Input } from "components/Input/Fields/Input";
import { Select } from "components/Input/Fields/Select";
import { Col } from "components/Layout";
import { Row } from "components/Layout/Row";
import { Modal, ModalConfirm } from "components/Modal";
import { Logger } from "utils/logger";
import { regExps } from "utils/validations";

const HandleAdditionModal: React.FC<IHandleAdditionModalProps> = ({
  groupName,
  handleCloseModal,
}: IHandleAdditionModalProps): JSX.Element => {
  const { t } = useTranslation();

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
  const activeIPRoots =
    rootsData === undefined
      ? []
      : rootsData.group.roots.filter(isIPRoot).filter(isActiveIPRoot);

  function handleSubmit(): void {
    // HandleSubmit
  }

  return (
    <React.StrictMode>
      {rootsData === undefined ? undefined : (
        <Modal open={true} title={t("group.toe.ports.addModal.title")}>
          <Formik
            initialValues={{
              port: undefined,
              rootId: undefined,
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
            {({ isSubmitting, dirty }): JSX.Element => {
              function handleInteger(
                event: React.KeyboardEvent<HTMLInputElement>
              ): void {
                if (event.key.length > 1 || /\d/u.test(event.key)) return;
                event.preventDefault();
              }

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
