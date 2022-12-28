import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef, Row } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Table as Tablez } from "components/Table";
import { Tooltip } from "components/Tooltip";
import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";
import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";
import {
  ADD_FILES_TO_DB_MUTATION,
  DOWNLOAD_FILE_MUTATION,
  GET_FILES,
  REMOVE_FILE_MUTATION,
  SIGN_POST_URL_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import type {
  IGetFilesQuery,
  IGroupFileAttr,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/types";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

interface IFilesProps {
  groupName: string;
}

const Files: React.FC<IFilesProps> = ({
  groupName,
}: IFilesProps): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(false);
  }, []);

  const [isOptionsModalOpen, setIsOptionsModalOpen] = useState(false);
  const closeOptionsModal: () => void = useCallback((): void => {
    setIsOptionsModalOpen(false);
  }, []);

  const [currentRow, setCurrentRow] = useState<Record<string, string>>({});

  function handleRowClickz(
    rowInfo: Row<IFile>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setCurrentRow(rowInfo.original as unknown as Record<string, string>);
      setIsOptionsModalOpen(true);
      event.preventDefault();
    };
  }

  const [isButtonEnabled, setIsButtonEnabled] = useState(false);
  const disableButton: () => void = useCallback((): void => {
    setIsButtonEnabled(true);
  }, []);

  const enableButton: () => void = useCallback((): void => {
    setIsButtonEnabled(false);
  }, []);

  // GraphQL operations
  const { data, refetch } = useQuery<IGetFilesQuery>(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group files", error);
      });
    },
    variables: { groupName },
  });

  const [downloadFile] = useMutation(DOWNLOAD_FILE_MUTATION, {
    onCompleted: (downloadData: { downloadFile: { url: string } }): void => {
      openUrl(downloadData.downloadFile.url);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred downloading group files", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  const [removeFile] = useMutation(REMOVE_FILE_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("RemoveGroupFiles");
      msgSuccess(
        t("searchFindings.tabResources.successRemove"),
        t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing group files", error);
      });
    },
  });
  const handleRemoveFile: () => Promise<void> =
    useCallback(async (): Promise<void> => {
      closeOptionsModal();
      mixpanel.track("RemoveFile");
      await removeFile({
        variables: {
          filesData: JSON.stringify({ fileName: currentRow.fileName }),
          groupName,
        },
      });
    }, [closeOptionsModal, currentRow.fileName, groupName, removeFile]);

  const [uploadFile] = useMutation(SIGN_POST_URL_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message === "Exception - Invalid characters in filename") {
          msgError(t("searchFindings.tabResources.invalidChars"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred uploading group files", error);
        }
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  const [addFilesToDb] = useMutation(ADD_FILES_TO_DB_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("AddGroupFiles");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred adding files to the db", error);
      });
    },
    variables: {
      filesData: JSON.stringify(currentRow.fileName),
      groupName,
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  interface IFile {
    description: string;
    fileName: string;
    uploadDate: string;
  }

  interface IAddFiles {
    signPostUrl: {
      url: {
        url: string;
        fields: {
          algorithm: string;
          credential: string;
          date: string;
          key: string;
          policy: string;
          securitytoken: string;
          signature: string;
        };
      };
    };
  }

  interface IAddFilesToDbResults {
    addFilesToDb: {
      success: boolean;
    };
  }

  const resourcesFiles: IGroupFileAttr[] = _.isNull(data.resources.files)
    ? []
    : data.resources.files;
  const filesDataset: IFile[] = resourcesFiles as IFile[];

  const handleUpload: (values: {
    description: string;
    file: FileList;
  }) => void = async (values: {
    description: string;
    file: FileList;
  }): Promise<void> => {
    const repeatedFiles: IFile[] = filesDataset.filter(
      (file: IFile): boolean => file.fileName === values.file[0].name
    );

    if (repeatedFiles.length > 0) {
      msgError(t("searchFindings.tabResources.repeatedItem"));
    } else {
      disableButton();
      const results = await uploadFile({
        variables: {
          filesData: JSON.stringify([
            {
              description: values.description,
              fileName: values.file[0].name,
            },
          ]),
          groupName,
        },
      });

      const { signPostUrl }: IAddFiles = results.data;
      const { url } = signPostUrl;
      const {
        algorithm,
        credential,
        date,
        key,
        policy,
        securitytoken,
        signature,
      } = url.fields;

      const formData = new FormData();
      formData.append("acl", "private");
      formData.append("key", key);
      formData.append("X-Amz-Algorithm", algorithm);
      formData.append("X-Amz-Credential", credential);
      formData.append("X-Amz-Date", date);
      formData.append("policy", policy);
      formData.append("X-Amz-Signature", signature);
      formData.append("X-Amz-Security-Token", securitytoken);
      formData.append("file", values.file[0], values.file[0].name);

      const response = await fetch(url.url, {
        body: formData,
        method: "POST",
      });

      if (response.ok) {
        const resultData = await addFilesToDb({
          onCompleted: (): void => {
            const { addFilesToDb: mutationResults }: IAddFilesToDbResults =
              resultData.data;

            const { success } = mutationResults;
            if (success) {
              msgSuccess(
                t("searchFindings.tabResources.success"),
                t("searchFindings.tabUsers.titleSuccess")
              );
            } else {
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred adding group files to the db",
                response.json
              );
              enableButton();
            }
          },
          variables: {
            filesData: JSON.stringify([
              {
                description: values.description,
                fileName: values.file[0].name,
              },
            ]),
            groupName,
          },
        });
      } else {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred uploading group files",
          response.json
        );
        enableButton();
      }
      enableButton();
      closeAddModal();
    }
  };

  const tableHeadersz: ColumnDef<IFile>[] = [
    {
      accessorKey: "fileName",
      header: t("searchFindings.filesTable.file"),
    },
    {
      accessorKey: "description",
      header: t("searchFindings.filesTable.description"),
    },
    {
      accessorKey: "uploadDate",
      header: t("searchFindings.filesTable.uploadDate"),
    },
  ];

  return (
    <React.StrictMode>
      <div className={"flex flex-wrap nt1"}>
        <Tablez
          columns={tableHeadersz}
          data={filesDataset}
          extraButtons={
            <Can do={"api_mutations_add_files_mutate"}>
              <Tooltip
                id={"searchFindings.tabResources.files.btnTooltip.id"}
                place={"top"}
                tip={t("searchFindings.tabResources.files.btnTooltip")}
              >
                <Button
                  id={"file-add"}
                  onClick={openAddModal}
                  variant={"primary"}
                >
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;{t("searchFindings.tabResources.addRepository")}
                </Button>
              </Tooltip>
            </Can>
          }
          id={"tblFiles"}
          onRowClick={handleRowClickz}
        />
      </div>
      <label>
        <b>{t("searchFindings.tabResources.totalFiles")}</b>
        {filesDataset.length}
      </label>
      <AddFilesModal
        isOpen={isAddModalOpen}
        isUploading={isButtonEnabled}
        onClose={closeAddModal}
        onSubmit={handleUpload} // eslint-disable-line react/jsx-no-bind -- Unexpected behaviour with no-bind
      />
      <Can do={"api_mutations_remove_files_mutate"} passThrough={true}>
        {(canRemove: boolean): JSX.Element => (
          <FileOptionsModal
            canRemove={canRemove}
            fileName={currentRow.fileName}
            isOpen={isOptionsModalOpen}
            onClose={closeOptionsModal}
            onDelete={handleRemoveFile}
            onDownload={downloadFile}
          />
        )}
      </Can>
    </React.StrictMode>
  );
};

export type { IFilesProps };
export { Files };
