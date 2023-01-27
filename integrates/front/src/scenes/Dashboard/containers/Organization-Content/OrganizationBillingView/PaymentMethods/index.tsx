import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faDownload,
  faPlus,
  faTrashAlt,
  faUserEdit,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddCreditCardModal } from "./AddCreditCardModal";
import { AddOtherMethodModal } from "./AddOtherMethodModal";
import { UpdateCreditCardModal } from "./UpdateCreditCardModal";
import { UpdateOtherMethodModal } from "./UpdateOtherMethodModal";

import {
  ADD_CREDIT_CARD_PAYMENT_METHOD,
  ADD_OTHER_PAYMENT_METHOD,
  DOWNLOAD_FILE_MUTATION,
  REMOVE_PAYMENT_METHOD,
  UPDATE_CREDIT_CARD_PAYMENT_METHOD,
  UPDATE_OTHER_PAYMENT_METHOD,
} from "../queries";
import type { IPaymentMethodAttr } from "../types";
import { Button } from "components/Button";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Text } from "components/Text";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

interface IOrganizationPaymentMethodsProps {
  organizationId: string;
  paymentMethods: IPaymentMethodAttr[];
  onUpdate: () => void;
}

export const OrganizationPaymentMethods: React.FC<IOrganizationPaymentMethodsProps> =
  ({
    organizationId,
    paymentMethods,
    onUpdate,
  }: IOrganizationPaymentMethodsProps): JSX.Element => {
    const { t } = useTranslation();
    const permissions: PureAbility<string> = useAbility(
      authzPermissionsContext
    );
    const [currentCreditCardRow, setCurrentCreditCardRow] = useState<
      IPaymentMethodAttr[]
    >([]);
    const [currentOtherMethodRow, setCurrentOtherMethodRow] = useState<
      IPaymentMethodAttr[]
    >([]);

    // Data
    const creditCardData: IPaymentMethodAttr[] = paymentMethods
      .map((paymentMethodData: IPaymentMethodAttr): IPaymentMethodAttr => {
        const isDefault: boolean = paymentMethodData.default;
        const capitalized: string = _.capitalize(paymentMethodData.brand);
        const brand: string = isDefault
          ? `${t(
              "organization.tabs.billing.paymentMethods.defaultPaymentMethod"
            )} ${capitalized}`
          : capitalized;

        return {
          ...paymentMethodData,
          brand,
        };
      })
      .filter((paymentMethod: IPaymentMethodAttr): boolean => {
        return paymentMethod.lastFourDigits !== "";
      });

    const otherMethodData: IPaymentMethodAttr[] = paymentMethods.filter(
      (paymentMethod: IPaymentMethodAttr): boolean => {
        return paymentMethod.lastFourDigits === "";
      }
    );

    const otherMetodData = otherMethodData.map((method): IPaymentMethodAttr => {
      return {
        ...method,
        download: method.id,
      };
    });

    // Add payment method
    const [isAddingPaymentMethod, setIsAddingPaymentMethod] = useState<
      "CREDIT_CARD" | "OTHER_METHOD" | false
    >(false);
    const openAddCreditCardModal = useCallback((): void => {
      setIsAddingPaymentMethod("CREDIT_CARD");
    }, []);
    const openAddOtherMethodModal = useCallback((): void => {
      setIsAddingPaymentMethod("OTHER_METHOD");
    }, []);
    const closeAddModal = useCallback((): void => {
      setIsAddingPaymentMethod(false);
    }, []);
    const [addCreditCardPaymentMethod] = useMutation(
      ADD_CREDIT_CARD_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          closeAddModal();
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.add.success.body"),
            t("organization.tabs.billing.paymentMethods.add.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            if (
              error.message ===
              "Exception - Provided payment method could not be created"
            ) {
              msgError(
                t(
                  "organization.tabs.billing.paymentMethods.add.errors.couldNotBeCreated"
                )
              );
            } else {
              msgError(t("groupAlerts.errorTextsad"));
              Logger.error("Couldn't create payment method", error);
            }
          });
        },
      }
    );
    const [addOtherPaymentMethod] = useMutation(ADD_OTHER_PAYMENT_METHOD, {
      onCompleted: (): void => {
        onUpdate();
        closeAddModal();
        msgSuccess(
          t("organization.tabs.billing.paymentMethods.add.success.body"),
          t("organization.tabs.billing.paymentMethods.add.success.title")
        );
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't create payment method", error);
        });
      },
    });
    const handleAddCreditCardMethodSubmit = useCallback(
      async ({
        cardCvc,
        cardExpirationMonth,
        cardExpirationYear,
        cardNumber,
        makeDefault,
      }: {
        cardCvc: string;
        cardExpirationMonth: string;
        cardExpirationYear: string;
        cardNumber: string;
        makeDefault: boolean;
      }): Promise<void> => {
        mixpanel.track("AddPaymentMethod", { method: "TC" });
        await addCreditCardPaymentMethod({
          variables: {
            cardCvc,
            cardExpirationMonth,
            cardExpirationYear,
            cardNumber,
            makeDefault,
            organizationId,
          },
        });
      },
      [addCreditCardPaymentMethod, organizationId]
    );

    const handleFileListUpload = (
      file: FileList | undefined
    ): File | undefined => {
      return _.isEmpty(file) ? undefined : (file as FileList)[0];
    };

    const handleAddOtherMethodSubmit = useCallback(
      async ({
        businessName,
        city,
        country,
        email,
        rutList,
        state,
        taxIdList,
      }: {
        businessName: string;
        city: string;
        country: string;
        email: string;
        rutList: FileList | undefined;
        state: string;
        taxIdList: FileList | undefined;
      }): Promise<void> => {
        const rut = handleFileListUpload(rutList);
        const taxId = handleFileListUpload(taxIdList);
        mixpanel.track("AddPaymentMethod", { method: "Wired" });
        await addOtherPaymentMethod({
          variables: {
            businessName,
            city,
            country,
            email,
            organizationId,
            rut,
            state,
            taxId,
          },
        });
      },
      [addOtherPaymentMethod, organizationId]
    );

    // Remove payment method
    const canRemove: boolean = permissions.can(
      "api_mutations_remove_payment_method_mutate"
    );
    const [removePaymentMethod, { loading: removing }] = useMutation(
      REMOVE_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          setCurrentCreditCardRow([]);
          setCurrentOtherMethodRow([]);
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.remove.success.body"),
            t("organization.tabs.billing.paymentMethods.remove.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            switch (error.message) {
              case "Exception - Cannot perform action. Please add a valid payment method first":
              case "Exception - Invalid payment method. Provided payment method does not exist for this organization":
                msgError(
                  t(
                    "organization.tabs.billing.paymentMethods.remove.errors.noPaymentMethod"
                  )
                );
                break;
              case "Exception - Cannot perform action. The organization has active or trialing subscriptions":
                msgError(
                  t(
                    "organization.tabs.billing.paymentMethods.remove.errors.activeSubscriptions"
                  )
                );
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.error("Couldn't remove payment method", error);
            }
          });
        },
      }
    );
    const handleRemoveCreditCardPaymentMethod: () => void =
      useCallback((): void => {
        void removePaymentMethod({
          variables: {
            organizationId,
            paymentMethodId: currentCreditCardRow[0]?.id,
          },
        });
      }, [organizationId, currentCreditCardRow, removePaymentMethod]);

    const handleRemoveOtherPaymentMethod: () => void = useCallback((): void => {
      void removePaymentMethod({
        variables: {
          organizationId,
          paymentMethodId: currentOtherMethodRow[0]?.id,
        },
      });
    }, [organizationId, currentOtherMethodRow, removePaymentMethod]);

    // Update payment method
    const canUpdateCreditCard: boolean = permissions.can(
      "api_mutations_update_credit_card_payment_method_mutate"
    );
    const canUpdateOther: boolean = permissions.can(
      "api_mutations_update_other_payment_method_mutate"
    );
    const [isUpdatingCreditCard, setIsUpdatingCreditCard] = useState<
      false | { mode: "UPDATE" }
    >(false);
    const openUpdateCreditCardModal = useCallback((): void => {
      setIsUpdatingCreditCard({ mode: "UPDATE" });
    }, []);
    const closeUpdateCreditCardModal = useCallback((): void => {
      setIsUpdatingCreditCard(false);
    }, []);
    const [isUpdatingOhterMethod, setIsUpdatingOhterMethod] = useState<
      false | { mode: "UPDATE" }
    >(false);
    const openUpdateOhterMethodModal = useCallback((): void => {
      setIsUpdatingOhterMethod({ mode: "UPDATE" });
    }, []);
    const closeUpdateOhterMethodModal = useCallback((): void => {
      setIsUpdatingOhterMethod(false);
    }, []);
    const [updateCreditCardPaymentMethod, { loading: updatingCreditCard }] =
      useMutation(UPDATE_CREDIT_CARD_PAYMENT_METHOD, {
        onCompleted: (): void => {
          onUpdate();
          closeUpdateCreditCardModal();
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.update.success.body"),
            t("organization.tabs.billing.paymentMethods.update.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            switch (error.message) {
              case "Exception - Cannot perform action. Please add a valid payment method first":
              case "Exception - Invalid payment method. Provided payment method does not exist for this organization":
                msgError(
                  t(
                    "organization.tabs.billing.paymentMethods.update.errors.noPaymentMethod"
                  )
                );
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.error("Couldn't update payment method", error);
            }
          });
        },
      });
    const [updateOtherPaymentMethod, { loading: updatingOther }] = useMutation(
      UPDATE_OTHER_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          closeUpdateOhterMethodModal();
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.update.success.body"),
            t("organization.tabs.billing.paymentMethods.update.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            if (
              error.message ===
              "Exception - Invalid payment method. Provided payment method does not exist for this organization"
            ) {
              msgError(
                t(
                  "organization.tabs.billing.paymentMethods.update.errors.noPaymentMethod"
                )
              );
            } else {
              msgError(t("groupAlerts.errorTextsad"));
              Logger.error("Couldn't update payment method", error);
            }
          });
        },
      }
    );
    const handleUpdateCreditCardPaymentMethodSubmit = useCallback(
      async ({
        cardExpirationMonth,
        cardExpirationYear,
        makeDefault,
      }: {
        cardExpirationMonth: number | undefined;
        cardExpirationYear: number | undefined;
        makeDefault: boolean;
      }): Promise<void> => {
        await updateCreditCardPaymentMethod({
          variables: {
            cardExpirationMonth,
            cardExpirationYear,
            makeDefault,
            organizationId,
            paymentMethodId: currentCreditCardRow[0]?.id,
          },
        });
      },
      [updateCreditCardPaymentMethod, organizationId, currentCreditCardRow]
    );

    const handleUpdateOtherPaymentMethodSubmit = useCallback(
      async ({
        businessName,
        city,
        country,
        email,
        rutList,
        state,
        taxIdList,
      }: {
        businessName: string;
        city: string;
        country: string;
        email: string;
        rutList: FileList | undefined;
        state: string;
        taxIdList: FileList | undefined;
      }): Promise<void> => {
        const rut = handleFileListUpload(rutList);
        const taxId = handleFileListUpload(taxIdList);
        await updateOtherPaymentMethod({
          variables: {
            businessName,
            city,
            country,
            email,
            organizationId,
            paymentMethodId: currentOtherMethodRow[0]?.id,
            rut,
            state,
            taxId,
          },
        });
      },
      [updateOtherPaymentMethod, organizationId, currentOtherMethodRow]
    );

    // Download legal document file
    const [downloadFile] = useMutation(DOWNLOAD_FILE_MUTATION, {
      onCompleted: (downloadData: {
        downloadBillingFile: { url: string };
      }): void => {
        openUrl(downloadData.downloadBillingFile.url);
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred downloading billing file", error);
        });
      },
    });

    const handleDownload = useCallback(
      async (paymentMethodId: string): Promise<void> => {
        const [paymentMethod] = paymentMethods.filter((method): boolean => {
          return method.id === paymentMethodId;
        });
        if (paymentMethod.rut) {
          const { fileName } = paymentMethod.rut;
          await downloadFile({
            variables: { fileName, organizationId, paymentMethodId },
          });
        } else if (paymentMethod.taxId) {
          const { fileName } = paymentMethod.taxId;
          await downloadFile({
            variables: { fileName, organizationId, paymentMethodId },
          });
        } else {
          msgError("Not Found a downloadable file");
        }
      },
      [downloadFile, organizationId, paymentMethods]
    );

    const creditCardTableHeadersz: ColumnDef<IPaymentMethodAttr>[] = [
      {
        accessorKey: "brand",
        header: "Brand",
      },
      {
        accessorKey: "lastFourDigits",
        header: "Last four digits",
      },
      {
        accessorKey: "expirationMonth",
        header: "Expiration Month",
      },
      {
        accessorKey: "expirationYear",
        header: "Expiration Year",
      },
    ];

    const handleDownloadClick = useCallback(
      (value: string): VoidFunction => {
        return (): void => {
          void handleDownload(value);
        };
      },
      [handleDownload]
    );

    const downloadFormatter = (value: string): JSX.Element => {
      return (
        <Button onClick={handleDownloadClick(value)} variant={"secondary"}>
          <FontAwesomeIcon icon={faDownload} />
        </Button>
      );
    };

    const otherMethodsTableHeaders: ColumnDef<IPaymentMethodAttr>[] = [
      {
        accessorKey: "businessName",
        header: "Business Name",
      },
      {
        accessorKey: "email",
        header: "e-factura email",
      },
      {
        accessorKey: "country",
        header: "Country",
      },
      {
        accessorKey: "download",
        cell: (cell: ICellHelper<IPaymentMethodAttr>): JSX.Element =>
          downloadFormatter(cell.getValue()),
        header: "Document",
      },
    ];

    return (
      <div>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("organization.tabs.billing.paymentMethods.title")}
        </Text>
        <Text fw={7} mb={2} mt={3} size={"medium"}>
          {t("organization.tabs.billing.paymentMethods.add.creditCard.label")}
        </Text>
        <Table
          columns={creditCardTableHeadersz}
          data={creditCardData}
          extraButtons={
            <Fragment>
              <Can do={"api_mutations_add_credit_card_payment_method_mutate"}>
                <Button
                  id={"addCreditCard"}
                  onClick={openAddCreditCardModal}
                  variant={"primary"}
                >
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.add.button")}
                </Button>
              </Can>
              <Can
                do={"api_mutations_update_credit_card_payment_method_mutate"}
              >
                <Button
                  disabled={
                    _.isEmpty(currentCreditCardRow) ||
                    removing ||
                    updatingCreditCard
                  }
                  id={"updateCreditCard"}
                  onClick={openUpdateCreditCardModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faUserEdit} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.update.button")}
                </Button>
              </Can>
              <Can do={"api_mutations_remove_payment_method_mutate"}>
                <Button
                  disabled={
                    _.isEmpty(currentCreditCardRow) ||
                    removing ||
                    updatingCreditCard
                  }
                  id={"removeCreditCard"}
                  onClick={handleRemoveCreditCardPaymentMethod}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.remove.button")}
                </Button>
              </Can>
            </Fragment>
          }
          id={"tblCreditCard"}
          rowSelectionSetter={
            canRemove || canUpdateCreditCard
              ? setCurrentCreditCardRow
              : undefined
          }
          rowSelectionState={currentCreditCardRow}
          selectionMode={"radio"}
        />
        <Text fw={7} mb={2} mt={3} size={"medium"}>
          {t("organization.tabs.billing.paymentMethods.add.otherMethods.label")}
        </Text>
        <Table
          columns={otherMethodsTableHeaders}
          data={otherMetodData}
          extraButtons={
            <Fragment>
              <Can do={"api_mutations_add_other_payment_method_mutate"}>
                <Button
                  id={"addOtherMethod"}
                  onClick={openAddOtherMethodModal}
                  variant={"primary"}
                >
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.add.button")}
                </Button>
              </Can>
              <Can do={"api_mutations_update_other_payment_method_mutate"}>
                <Button
                  disabled={
                    _.isEmpty(currentOtherMethodRow) ||
                    removing ||
                    updatingOther
                  }
                  id={"updateOtherMethod"}
                  onClick={openUpdateOhterMethodModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faUserEdit} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.update.button")}
                </Button>
              </Can>
              <Can do={"api_mutations_remove_payment_method_mutate"}>
                <Button
                  disabled={
                    _.isEmpty(currentOtherMethodRow) ||
                    removing ||
                    updatingOther
                  }
                  id={"removeOtherMethod"}
                  onClick={handleRemoveOtherPaymentMethod}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.remove.button")}
                </Button>
              </Can>
            </Fragment>
          }
          id={"tblOtherMethods"}
          rowSelectionSetter={
            canRemove || canUpdateOther ? setCurrentOtherMethodRow : undefined
          }
          rowSelectionState={currentOtherMethodRow}
          selectionMode={"radio"}
        />
        {isAddingPaymentMethod === "CREDIT_CARD" && (
          <AddCreditCardModal
            onChangeMethod={setIsAddingPaymentMethod}
            onClose={closeAddModal}
            onSubmit={handleAddCreditCardMethodSubmit}
          />
        )}
        {isAddingPaymentMethod === "OTHER_METHOD" && (
          <AddOtherMethodModal
            onChangeMethod={setIsAddingPaymentMethod}
            onClose={closeAddModal}
            onSubmit={handleAddOtherMethodSubmit}
          />
        )}
        {isUpdatingCreditCard === false ? undefined : (
          <UpdateCreditCardModal
            onClose={closeUpdateCreditCardModal}
            onSubmit={handleUpdateCreditCardPaymentMethodSubmit}
          />
        )}
        {isUpdatingOhterMethod === false ? undefined : (
          <UpdateOtherMethodModal
            initialValues={{
              businessName: currentOtherMethodRow[0].businessName,
              city: currentOtherMethodRow[0].city,
              country: currentOtherMethodRow[0].country,
              email: currentOtherMethodRow[0].email,
              rutList: undefined,
              state: currentOtherMethodRow[0].state,
              taxIdList: undefined,
            }}
            onClose={closeUpdateOhterMethodModal}
            onSubmit={handleUpdateOtherPaymentMethodSubmit}
          />
        )}
      </div>
    );
  };
