import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { array, object } from "yup";

import { REQUEST_GROUPS_UPGRADE_MUTATION } from "./queries";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Modal } from "components/Modal";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgSuccess } from "utils/notifications";

interface IUpgradeGroupsModalProps {
  groups: IOrganizationGroups["groups"];
  onClose: () => void;
}

const UpgradeGroupsModal: React.FC<IUpgradeGroupsModalProps> = ({
  groups,
  onClose,
}: IUpgradeGroupsModalProps): JSX.Element => {
  const { t } = useTranslation();
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
    <Modal headerTitle={t("upgrade.title")} open={true}>
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
                    <Field
                      component={FormikCheckbox}
                      key={groupName}
                      label={_.capitalize(groupName)}
                      name={"groupNames"}
                      type={"checkbox"}
                      value={groupName}
                    />
                  )
                )}
              </React.Fragment>
            ) : (
              <p>{t("upgrade.unauthorized")}</p>
            )}
          </FormGroup>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={onClose}>{t("upgrade.close")}</Button>
                {canUpgrade ? (
                  <Button type={"submit"}>{t("upgrade.upgrade")}</Button>
                ) : undefined}
              </ButtonToolbar>
            </Col100>
          </Row>
        </Form>
      </Formik>
    </Modal>
  );
};

export { UpgradeGroupsModal };
