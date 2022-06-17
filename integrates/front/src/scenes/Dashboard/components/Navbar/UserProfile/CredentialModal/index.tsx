/* eslint-disable jsx-a11y/no-autofocus */
import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { GET_STAKEHOLDER_CREDENTIALS } from "./queries";
import type {
  ICredentialAttr,
  ICredentialData,
  ICredentialModalProps,
} from "./types";

import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { editAndDeleteActionFormatter } from "components/Table/formatters/editAndDeleteActionFormatter";
import type { IHeaderConfig } from "components/Table/types";
import { Logger } from "utils/logger";

const CredentialModal: React.FC<ICredentialModalProps> = (
  props: ICredentialModalProps
): JSX.Element => {
  const { isOpen, onClose } = props;
  const { t } = useTranslation();

  const { data } = useQuery<{
    me: { credentials: ICredentialAttr[] };
  }>(GET_STAKEHOLDER_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder credentials", error);
      });
    },
  });
  const credentialsAttrs = _.isUndefined(data) ? [] : data.me.credentials;
  const credentials: ICredentialData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialAttr): ICredentialData => ({
      ...credentialAttr,
      organizationName: credentialAttr.organization.name,
    })
  );

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: t("profile.credentialModal.table.columns.name"),
      wrapped: true,
    },
    {
      dataField: "type",
      header: t("profile.credentialModal.table.columns.type"),
      wrapped: true,
    },
    {
      dataField: "organizationName",
      header: t("profile.credentialModal.table.columns.organization"),
      wrapped: true,
    },
    {
      dataField: "id",
      formatter: editAndDeleteActionFormatter,
      header: t("profile.credentialModal.table.columns.action"),
      width: "60px",
    },
  ];

  return (
    <Modal
      minWidth={600}
      onClose={onClose}
      open={isOpen}
      title={t("profile.credentialModal.title")}
    >
      <Table
        dataset={credentials}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblCredentials"}
        pageSize={10}
        search={false}
      />
    </Modal>
  );
};

export { CredentialModal };
