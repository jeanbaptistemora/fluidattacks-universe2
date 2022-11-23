import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";

import { GET_ROOTS } from "./queries";
import type { IHandleAdditionModalProps, IIPRootAttr, Root } from "./types";
import { isActiveIPRoot, isIPRoot } from "./utils";

import { Select } from "components/Input/Fields/Select";
import { Col } from "components/Layout";
import { Row } from "components/Layout/Row";
import { Modal, ModalConfirm } from "components/Modal";
import { Logger } from "utils/logger";

const HandleAdditionModal: React.FC<IHandleAdditionModalProps> = ({
  groupName,
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
              port: "",
              rootId: "",
            }}
            name={"addToePort"}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting, dirty }): JSX.Element => {
              return (
                <Form id={"addToePort"}>
                  <Row justify={"start"}>
                    <Col lg={100} md={100} sm={100}>
                      <Select
                        label={t("group.toe.ports.addModal.fields.IPRoot")}
                        name={"rootId"}
                      >
                        {activeIPRoots.map(
                          (root: IIPRootAttr): JSX.Element => (
                            <option key={root.id} value={root.id}>
                              {root.address} {"-"} {root.nickname}
                            </option>
                          )
                        )}
                      </Select>
                    </Col>
                  </Row>
                  <br />
                  <ModalConfirm disabled={isSubmitting || !dirty} />
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
