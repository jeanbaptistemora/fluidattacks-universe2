import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { array, object } from "yup";

import { REQUEST_GROUPS_UPGRADE_MUTATION } from "./queries";

import { ExternalLink } from "components/ExternalLink";
import { Checkbox } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import type {
  IGetUserOrganizationsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgSuccess } from "utils/notifications";

interface IUpgradeGroupsModalProps {
  onClose: () => void;
}

const UpgradeGroupsModal: React.FC<IUpgradeGroupsModalProps> = ({
  onClose,
}: IUpgradeGroupsModalProps): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
    }
  );
  const groups =
    data === undefined
      ? []
      : data.me.organizations.reduce<IOrganizationGroups["groups"]>(
          (previousValue, currentValue): IOrganizationGroups["groups"] => [
            ...previousValue,
            ...currentValue.groups,
          ],
          []
        );
  const upgradableGroups = groups
    .filter(
      (group): boolean =>
        !group.serviceAttributes.includes("has_squad") &&
        group.permissions.includes("request_group_upgrade")
    )
    .map((group): string => group.name);
  const canUpgrade = upgradableGroups.length > 0;

  const [requestGroupsUpgrade] = useMutation(REQUEST_GROUPS_UPGRADE_MUTATION, {
    onCompleted: (): void => {
      msgSuccess(t("upgrade.success.text"), t("upgrade.success.title"));
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't request groups upgrade", error);
      });
    },
  });

  const handleSubmit = useCallback(
    async (values: { groupNames: string[] }): Promise<void> => {
      onClose();
      await requestGroupsUpgrade({
        variables: { groupNames: values.groupNames },
      });
    },
    [onClose, requestGroupsUpgrade]
  );

  const validations = object().shape({
    groupNames: array().min(1, t("validations.someRequired")),
  });

  return (
    <Modal open={true} title={t("upgrade.title")}>
      <p>
        {t("upgrade.text")}&nbsp;
        <ExternalLink href={"https://fluidattacks.com/plans/"}>
          {t("upgrade.link")}
        </ExternalLink>
      </p>
      <Formik
        initialValues={{ groupNames: upgradableGroups }}
        name={"upgradeGroups"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <FormGroup>
            {canUpgrade ? (
              <React.Fragment>
                <ControlLabel>{t("upgrade.select")}</ControlLabel>
                <br />
                {upgradableGroups.map(
                  (groupName): JSX.Element => (
                    <Checkbox
                      key={groupName}
                      label={_.capitalize(groupName)}
                      name={"groupNames"}
                      value={groupName}
                    />
                  )
                )}
              </React.Fragment>
            ) : (
              <p>{t("upgrade.unauthorized")}</p>
            )}
          </FormGroup>
          <ModalConfirm
            disabled={canUpgrade}
            onCancel={onClose}
            txtConfirm={t("upgrade.upgrade")}
          />
        </Form>
      </Formik>
    </Modal>
  );
};

export { UpgradeGroupsModal };
