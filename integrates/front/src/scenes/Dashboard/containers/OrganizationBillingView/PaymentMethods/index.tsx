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
import _ from "lodash";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddCreditCardModal } from "./AddCreditCardModal";
import { AddOtherMethodModal } from "./AddOtherMethodModal";
import { Container } from "./styles";
import { UpdateCreditCardModal } from "./UpdateCreditCardModal";
import { UpdateOtherMethodModal } from "./UpdateOtherMethodModal";

import {
  ADD_PAYMENT_METHOD,
  DOWNLOAD_FILE_MUTATION,
  REMOVE_PAYMENT_METHOD,
  UPDATE_PAYMENT_METHOD,
} from "../queries";
import type { IPaymentMethodAttr } from "../types";
import { Button } from "components/Button";
import { Table } from "components/Table/index";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { Text } from "components/Text";
import { GraphicButton } from "styles/styledComponents";
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
      Record<string, string>
    >({});
    const [currentOtherMethodRow, setCurrentOtherMethodRow] = useState<
      Record<string, string>
    >({});

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

    // Search credit card bar
    const [searchFilterCreditCard, setSearchFilterCreditCard] = useState("");
    function onSearchCreditCardChange(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
      setSearchFilterCreditCard(event.target.value);
    }
    const filterSearchTextCreditCard: IPaymentMethodAttr[] = filterSearchText(
      creditCardData,
      searchFilterCreditCard
    );

    // Search other method bar
    const [searchFilterOtherMethod, setSearchFilterOtherMethod] = useState("");
    function onSearchOtherMethodChange(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
      setSearchFilterOtherMethod(event.target.value);
    }
    const filterSearchTextOtherMethod: IPaymentMethodAttr[] = filterSearchText(
      otherMethodData,
      searchFilterOtherMethod
    );

    const otherMetodData = filterSearchTextOtherMethod.map(
      (method): IPaymentMethodAttr => {
        return {
          ...method,
          download: method.id,
        };
      }
    );

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
    const [addPaymentMethod] = useMutation(ADD_PAYMENT_METHOD, {
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
          switch (error.message) {
            case "Exception - Provided payment method could not be created":
              msgError(
                t(
                  "organization.tabs.billing.paymentMethods.add.errors.couldNotBeCreated"
                )
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.error("Couldn't create payment method", error);
          }
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
        const businessName = "";
        const email = "";
        const country = "";
        const state = "";
        const city = "";
        const rut = undefined;
        const taxId = undefined;
        await addPaymentMethod({
          variables: {
            businessName,
            cardCvc,
            cardExpirationMonth,
            cardExpirationYear,
            cardNumber,
            city,
            country,
            email,
            makeDefault,
            organizationId,
            rut,
            state,
            taxId,
          },
        });
      },
      [addPaymentMethod, organizationId]
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
        const cardCvc = "";
        const cardExpirationMonth = "";
        const cardExpirationYear = "";
        const cardNumber = "";
        const makeDefault = false;
        const rut = handleFileListUpload(rutList);
        const taxId = handleFileListUpload(taxIdList);
        await addPaymentMethod({
          variables: {
            businessName,
            cardCvc,
            cardExpirationMonth,
            cardExpirationYear,
            cardNumber,
            city,
            country,
            email,
            makeDefault,
            organizationId,
            rut,
            state,
            taxId,
          },
        });
      },
      [addPaymentMethod, organizationId]
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
          setCurrentCreditCardRow({});
          setCurrentOtherMethodRow({});
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.remove.success.body"),
            t("organization.tabs.billing.paymentMethods.remove.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            switch (error.message) {
              case "Exception - Cannot perform action. Please add a valid payment method first":
                msgError(
                  t(
                    "organization.tabs.billing.paymentMethods.remove.errors.noPaymentMethod"
                  )
                );
                break;
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
    const handleRemovePaymentMethod: () => void = useCallback((): void => {
      void removePaymentMethod({
        variables: {
          organizationId,
          paymentMethodId: currentCreditCardRow.id
            ? currentCreditCardRow.id
            : currentOtherMethodRow.id,
        },
      });
    }, [
      organizationId,
      currentCreditCardRow,
      currentOtherMethodRow,
      removePaymentMethod,
    ]);

    // Update payment method
    const canUpdate: boolean = permissions.can(
      "api_mutations_update_payment_method_mutate"
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
    const [updatePaymentMethod, { loading: updating }] = useMutation(
      UPDATE_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          closeUpdateCreditCardModal();
          closeUpdateOhterMethodModal();
          msgSuccess(
            t("organization.tabs.billing.paymentMethods.update.success.body"),
            t("organization.tabs.billing.paymentMethods.update.success.title")
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't update payment method", error);
          });
        },
      }
    );
    const handleUpdatePaymentMethodSubmit = useCallback(
      async ({
        cardExpirationMonth,
        cardExpirationYear,
        makeDefault,
        businessName,
        city,
        country,
        email,
        rutList,
        state,
        taxIdList,
      }: {
        cardExpirationMonth: string;
        cardExpirationYear: string;
        makeDefault: boolean;
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
        await updatePaymentMethod({
          variables: {
            businessName,
            cardExpirationMonth,
            cardExpirationYear,
            city,
            country,
            email,
            makeDefault,
            organizationId,
            paymentMethodId: currentCreditCardRow.id
              ? currentCreditCardRow.id
              : currentOtherMethodRow.id,
            rut,
            state,
            taxId,
          },
        });
      },
      [
        updatePaymentMethod,
        organizationId,
        currentCreditCardRow,
        currentOtherMethodRow,
      ]
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

    // Table header
    const creditCardTableHeaders: IHeaderConfig[] = [
      {
        dataField: "brand",
        header: "Brand",
      },
      {
        dataField: "lastFourDigits",
        header: "Last four digits",
      },
      {
        dataField: "expirationMonth",
        header: "Expiration Month",
      },
      {
        dataField: "expirationYear",
        header: "Expiration Year",
      },
    ];

    const downloadFormatter = (
      value: string,
      _row: Readonly<Record<string, string>>,
      _rowIndex: number,
      _key: Readonly<IHeaderConfig>
    ): JSX.Element => {
      async function onClick(): Promise<void> {
        await handleDownload(value);
      }

      return (
        <GraphicButton onClick={onClick}>
          <FontAwesomeIcon icon={faDownload} />
        </GraphicButton>
      );
    };

    const otherMethodsTableHeaders: IHeaderConfig[] = [
      {
        dataField: "businessName",
        header: "Business Name",
      },
      {
        dataField: "email",
        header: "e-factura email",
      },
      {
        dataField: "country",
        header: "Country",
      },
      {
        dataField: "download",
        formatter: downloadFormatter,
        header: "Document",
      },
    ];

    return (
      <Container>
        <Text fw={7} mb={3} mt={4} size={5}>
          {t("organization.tabs.billing.paymentMethods.title")}
        </Text>
        <Text fw={7} mb={2} mt={3} size={4}>
          {t("organization.tabs.billing.paymentMethods.add.creditCard.label")}
        </Text>
        <Table
          columnToggle={false}
          customSearch={{
            customSearchDefault: searchFilterCreditCard,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchCreditCardChange,
            position: "right",
          }}
          dataset={filterSearchTextCreditCard}
          defaultSorted={{ dataField: "brand", order: "asc" }}
          exportCsv={false}
          extraButtons={
            <Fragment>
              <Can do={"api_mutations_add_payment_method_mutate"}>
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
              <Can do={"api_mutations_update_payment_method_mutate"}>
                <Button
                  disabled={
                    _.isEmpty(currentCreditCardRow) || removing || updating
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
                    _.isEmpty(currentCreditCardRow) || removing || updating
                  }
                  id={"removeCreditCard"}
                  onClick={handleRemovePaymentMethod}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.remove.button")}
                </Button>
              </Can>
            </Fragment>
          }
          headers={creditCardTableHeaders}
          id={"tblCreditCard"}
          pageSize={10}
          search={false}
          selectionMode={{
            clickToSelect: canRemove || canUpdate,
            hideSelectColumn: !canRemove && !canUpdate,
            mode: "radio",
            onSelect: setCurrentCreditCardRow,
          }}
        />
        <Text fw={7} mb={2} mt={3} size={4}>
          {t("organization.tabs.billing.paymentMethods.add.otherMethods.label")}
        </Text>
        <Table
          columnToggle={false}
          customSearch={{
            customSearchDefault: searchFilterOtherMethod,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchOtherMethodChange,
            position: "right",
          }}
          dataset={otherMetodData}
          defaultSorted={{ dataField: "businessName", order: "asc" }}
          exportCsv={false}
          extraButtons={
            <Fragment>
              <Can do={"api_mutations_add_payment_method_mutate"}>
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
              <Can do={"api_mutations_update_payment_method_mutate"}>
                <Button
                  disabled={
                    _.isEmpty(currentOtherMethodRow) || removing || updating
                  }
                  id={"updateCreditCard"}
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
                    _.isEmpty(currentOtherMethodRow) || removing || updating
                  }
                  id={"removeOtherMethod"}
                  onClick={handleRemovePaymentMethod}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;
                  {t("organization.tabs.billing.paymentMethods.remove.button")}
                </Button>
              </Can>
            </Fragment>
          }
          headers={otherMethodsTableHeaders}
          id={"tblOtherMethods"}
          pageSize={10}
          search={false}
          selectionMode={{
            clickToSelect: canRemove || canUpdate,
            hideSelectColumn: !canRemove && !canUpdate,
            mode: "radio",
            onSelect: setCurrentOtherMethodRow,
          }}
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
            onSubmit={handleUpdatePaymentMethodSubmit}
          />
        )}
        {isUpdatingOhterMethod === false ? undefined : (
          <UpdateOtherMethodModal
            initialValues={{
              businessName: currentOtherMethodRow.businessName,
              cardExpirationMonth: "",
              cardExpirationYear: "",
              city: currentOtherMethodRow.city,
              country: currentOtherMethodRow.country,
              email: currentOtherMethodRow.email,
              makeDefault: false,
              rutList: undefined,
              state: currentOtherMethodRow.state,
              taxIdList: undefined,
            }}
            onClose={closeUpdateOhterMethodModal}
            onSubmit={handleUpdatePaymentMethodSubmit}
          />
        )}
      </Container>
    );
  };
