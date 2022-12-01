import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IPlusModalProps } from "./types";

import {
  handleCreationError,
  handleUpdateError,
  useGitSubmit,
} from "../GroupScopeView/GitRoots/helpers";
import { ManagementModal } from "../GroupScopeView/GitRoots/ManagementModal";
import { ADD_GIT_ROOT, UPDATE_GIT_ROOT } from "../GroupScopeView/queries";
import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";

export const PlusModal: React.FC<IPlusModalProps> = ({
  organizationId,
  changeGroupPermissions,
  changeOrganizationPermissions,
  groupNames,
  isOpen,
  refetchRepositories,
  repository,
  onClose,
}: IPlusModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [branch] = repository.defaultBranch.split("/").slice(-1);
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
    setIsManagingRoot(false);
    setGroupName("");
    changeOrganizationPermissions();
    setRootModalMessages({ message: "", type: "success" });
  }, [changeOrganizationPermissions, setRootModalMessages]);

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: async (): Promise<void> => {
      await refetchRepositories();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleCreationError(graphQLErrors, setRootModalMessages);
    },
  });

  const [updateGitRoot] = useMutation(UPDATE_GIT_ROOT, {
    onCompleted: async (): Promise<void> => {
      await refetchRepositories();
      setGroupName("");
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, setRootModalMessages, "root");
    },
  });

  const handleGitSubmit = useGitSubmit(
    addGitRoot,
    groupName,
    isManagingRoot,
    setRootModalMessages,
    updateGitRoot
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
              label={t("organization.tabs.weakest.modal.select")}
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
            branch,
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
            url: repository.url,
            useVpn: false,
          }}
          isEditing={isManagingRoot.mode === "EDIT"}
          manyRows={false}
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
