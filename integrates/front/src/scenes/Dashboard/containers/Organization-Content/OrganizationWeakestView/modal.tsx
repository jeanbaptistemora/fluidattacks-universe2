import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type {
  AddGitRootResult,
  IAddGitRootMutation,
  IIntegrationRepositoriesAttr,
  IPlusModalProps,
} from "./types";

import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ManagementModal } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GitRoots/ManagementModal";
import { ADD_GIT_ROOT } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
import type { IFormValues } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/types";
import {
  getAddGitRootCredentialsVariables,
  getAreAllMutationValid,
  handleAddedError,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationWeakestView/utils";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default

export const PlusModal: React.FC<IPlusModalProps> = ({
  organizationId,
  changeGroupPermissions,
  changeOrganizationPermissions,
  groupNames,
  isOpen,
  onClose,
  refetchRepositories,
  repositories,
  setSelectedRepositories,
  setSelectedRow,
}: IPlusModalProps): JSX.Element => {
  const { t } = useTranslation();

  const branches = useMemo((): string[] => {
    return repositories.map(
      (repository: IIntegrationRepositoriesAttr): string => {
        const [branch] = repository.defaultBranch.split("/").slice(-1);

        return branch;
      }
    );
  }, [repositories]);
  const groupCtxt: IGroupContext = useContext(groupContext);

  const [isManagingRoot, setIsManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);
  const [groupName, setGroupName] = useState<string>("");
  const [rootModalMessages, setRootModalMessages] = useState({
    message: "",
    type: "success",
  });

  const closeModal: () => void = useCallback((): void => {
    setSelectedRow(undefined);
    setIsManagingRoot(false);
    setGroupName("");
    changeOrganizationPermissions();
    setRootModalMessages({ message: "", type: "success" });
  }, [changeOrganizationPermissions, setRootModalMessages, setSelectedRow]);

  const [addGitRoot] = useMutation<IAddGitRootMutation>(ADD_GIT_ROOT);

  const handleGitSubmit = useCallback(
    async ({
      branch,
      credentials,
      environment,
      gitignore,
      includesHealthCheck,
      nickname,
      useVpn,
    }: IFormValues): Promise<void> => {
      mixpanel.track("AddGitRoot");
      try {
        const chunkSize = 1;
        const repositoriesChunks = _.chunk(repositories, chunkSize);
        const addedChuncks = repositoriesChunks.map(
          (chunck): (() => Promise<AddGitRootResult[]>) =>
            async (): Promise<AddGitRootResult[]> => {
              const added = chunck.map(
                async (repository): Promise<AddGitRootResult> =>
                  addGitRoot({
                    variables: {
                      branch: branch.trim(),
                      credentials:
                        getAddGitRootCredentialsVariables(credentials),
                      environment,
                      gitignore,
                      groupName,
                      includesHealthCheck: includesHealthCheck ?? false,
                      nickname,
                      url: repository.url.trim(),
                      useVpn,
                    },
                  })
              );

              return Promise.all(added);
            }
        );

        const results = await addedChuncks.reduce(
          async (previousValue, currentValue): Promise<AddGitRootResult[]> => [
            ...(await previousValue),
            ...(await currentValue()),
          ],
          Promise.resolve<AddGitRootResult[]>([])
        );
        const areAllMutationValid = getAreAllMutationValid(results);
        if (areAllMutationValid.every(Boolean)) {
          await refetchRepositories();
          setSelectedRepositories([]);
          closeModal();
        }
      } catch (addError: unknown) {
        handleAddedError(addError, setRootModalMessages);
      }
    },
    [
      addGitRoot,
      closeModal,
      groupName,
      refetchRepositories,
      repositories,
      setSelectedRepositories,
    ]
  );

  const onConfirmPlus = useCallback(
    (values: { groupName: string }): void => {
      changeGroupPermissions(values.groupName);
      setGroupName(values.groupName);
      // eslint-disable-next-line fp/no-mutation
      groupCtxt.organizationId = organizationId;
      setIsManagingRoot({ mode: "ADD" });
      onClose();
    },
    [changeGroupPermissions, groupCtxt, organizationId, onClose]
  );

  const validations = object().shape({
    groupName: string().required(t("validations.required")),
  });

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={t("organization.tabs.weakest.modal.title")}
      >
        <Formik
          initialValues={{ groupName: "" }}
          name={"groupToAddRoot"}
          onSubmit={onConfirmPlus}
          validationSchema={validations}
        >
          <Form>
            <Select
              label={t("organization.tabs.weakest.modal.select", {
                count: repositories.length,
              })}
              name={"groupName"}
            >
              <option value={""}>{""}</option>
              {groupNames.map(
                (name): JSX.Element => (
                  <option key={`${name}.id`} value={name}>
                    {name}
                  </option>
                )
              )}
            </Select>
            <ModalConfirm onCancel={onClose} onConfirm={"submit"} />
          </Form>
        </Formik>
      </Modal>
      {isManagingRoot === false ? undefined : (
        <ManagementModal
          finishTour={onClose}
          groupName={groupName}
          initialValues={{
            branch: branches[0],
            cloningStatus: {
              message: "",
              status: "UNKNOWN",
            },
            credentials: {
              auth: "",
              azureOrganization: "",
              id: "",
              isPat: false,
              key: "",
              name: "",
              password: "",
              token: "",
              type: "",
              typeCredential: "",
              user: "",
            },
            environment: "",
            environmentUrls: [],
            gitEnvironmentUrls: [],
            gitignore: [],
            healthCheckConfirm: [],
            id: "",
            includesHealthCheck: null,
            nickname: "",
            secrets: [],
            state: "ACTIVE",
            url: repositories[0].url,
            useVpn: false,
          }}
          isEditing={isManagingRoot.mode === "EDIT"}
          manyRows={repositories.length > 1}
          modalMessages={rootModalMessages}
          nicknames={[]}
          onClose={closeModal}
          onSubmitRepo={handleGitSubmit}
          onUpdate={refetchRepositories}
          runTour={false}
        />
      )}
    </React.StrictMode>
  );
};
