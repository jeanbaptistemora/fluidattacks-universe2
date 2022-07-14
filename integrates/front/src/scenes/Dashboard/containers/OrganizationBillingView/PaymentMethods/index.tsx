import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faPlus,
  faTrashAlt,
  faUserEdit,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddCreditCardModal } from "./AddCreditCardModal";
import { AddOtherMethodModal } from "./AddOtherMethodModal";
import { Container } from "./styles";
import { UpdatePaymentModal } from "./UpdatePaymentMethodModal";

import {
  ADD_PAYMENT_METHOD,
  REMOVE_PAYMENT_METHOD,
  UPDATE_PAYMENT_METHOD,
} from "../queries";
import type { IPaymentMethodAttr } from "../types";
import { Button } from "components/Button";
import { Table } from "components/Table/index";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

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
    const [currentRow, setCurrentRow] = useState<Record<string, string>>({});

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
            state,
          },
        });
      },
      [addPaymentMethod, organizationId]
    );

    const handleAddOtherMethodSubmit = useCallback(
      async ({
        businessName,
        city,
        country,
        email,
        state,
      }: {
        businessName: string;
        city: string;
        country: string;
        email: string;
        state: string;
      }): Promise<void> => {
        const cardCvc = "";
        const cardExpirationMonth = "";
        const cardExpirationYear = "";
        const cardNumber = "";
        const makeDefault = false;
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
            state,
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
          setCurrentRow({});
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
          paymentMethodId: currentRow.id,
        },
      });
    }, [organizationId, currentRow.id, removePaymentMethod]);

    // Update payment method
    const canUpdate: boolean = permissions.can(
      "api_mutations_update_payment_method_mutate"
    );
    const [isUpdatingPaymentMethod, setIsUpdatingPaymentMethod] = useState<
      false | { mode: "UPDATE" }
    >(false);
    const openUpdateModal = useCallback((): void => {
      setIsUpdatingPaymentMethod({ mode: "UPDATE" });
    }, []);
    const closeUpdateModal = useCallback((): void => {
      setIsUpdatingPaymentMethod(false);
    }, []);
    const [updatePaymentMethod, { loading: updating }] = useMutation(
      UPDATE_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          closeUpdateModal();
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
      }: {
        cardExpirationMonth: string;
        cardExpirationYear: string;
        makeDefault: boolean;
      }): Promise<void> => {
        await updatePaymentMethod({
          variables: {
            cardExpirationMonth,
            cardExpirationYear,
            makeDefault,
            organizationId,
            paymentMethodId: currentRow.id,
          },
        });
      },
      [updatePaymentMethod, organizationId, currentRow.id]
    );

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
    ];

    return (
      <Container>
        <Row>
          <div className={"w-100-ns"}>
            <Row>
              <h2>{t("organization.tabs.billing.paymentMethods.title")}</h2>
            </Row>
            <Row>
              <h3>
                {t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.label"
                )}
              </h3>
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
                  <Row>
                    <Can do={"api_mutations_add_payment_method_mutate"}>
                      <Button
                        id={"addCreditCard"}
                        onClick={openAddCreditCardModal}
                        variant={"primary"}
                      >
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;
                        {t(
                          "organization.tabs.billing.paymentMethods.add.button"
                        )}
                      </Button>
                    </Can>
                    <Can do={"api_mutations_update_payment_method_mutate"}>
                      <Button
                        disabled={_.isEmpty(currentRow) || removing || updating}
                        id={"updateCreditCard"}
                        onClick={openUpdateModal}
                        variant={"secondary"}
                      >
                        <FontAwesomeIcon icon={faUserEdit} />
                        &nbsp;
                        {t(
                          "organization.tabs.billing.paymentMethods.update.button"
                        )}
                      </Button>
                    </Can>
                    <Can do={"api_mutations_remove_payment_method_mutate"}>
                      <Button
                        disabled={_.isEmpty(currentRow) || removing || updating}
                        id={"removeCreditCard"}
                        onClick={handleRemovePaymentMethod}
                        variant={"secondary"}
                      >
                        <FontAwesomeIcon icon={faTrashAlt} />
                        &nbsp;
                        {t(
                          "organization.tabs.billing.paymentMethods.remove.button"
                        )}
                      </Button>
                    </Can>
                  </Row>
                }
                headers={creditCardTableHeaders}
                id={"tblCreditCard"}
                pageSize={10}
                search={false}
                selectionMode={{
                  clickToSelect: canRemove || canUpdate,
                  hideSelectColumn: !canRemove && !canUpdate,
                  mode: "radio",
                  onSelect: setCurrentRow,
                }}
              />
            </Row>
            <Row>
              <h3>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.label"
                )}
              </h3>
              <Table
                columnToggle={false}
                customSearch={{
                  customSearchDefault: searchFilterOtherMethod,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchOtherMethodChange,
                  position: "right",
                }}
                dataset={filterSearchTextOtherMethod}
                defaultSorted={{ dataField: "businessName", order: "asc" }}
                exportCsv={false}
                extraButtons={
                  <Row>
                    <Can do={"api_mutations_add_payment_method_mutate"}>
                      <Button
                        id={"addOtherMethod"}
                        onClick={openAddOtherMethodModal}
                        variant={"primary"}
                      >
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;
                        {t(
                          "organization.tabs.billing.paymentMethods.add.button"
                        )}
                      </Button>
                    </Can>
                  </Row>
                }
                headers={otherMethodsTableHeaders}
                id={"tblOtherMethods"}
                pageSize={10}
                search={false}
                selectionMode={{
                  clickToSelect: canRemove || canUpdate,
                  hideSelectColumn: !canRemove && !canUpdate,
                  mode: "radio",
                  onSelect: setCurrentRow,
                }}
              />
            </Row>
          </div>
        </Row>
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
        {isUpdatingPaymentMethod === false ? undefined : (
          <UpdatePaymentModal
            onClose={closeUpdateModal}
            onSubmit={handleUpdatePaymentMethodSubmit}
          />
        )}
      </Container>
    );
  };
