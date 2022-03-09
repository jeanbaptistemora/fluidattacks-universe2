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

import { AddPaymentModal } from "./AddPaymentMethodModal";
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
import { Col100, Row } from "styles/styledComponents";
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
    const data: IPaymentMethodAttr[] = paymentMethods.map(
      (paymentMethodData: IPaymentMethodAttr): IPaymentMethodAttr => {
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
      }
    );

    // Search bar
    const [searchTextFilter, setSearchTextFilter] = useState("");
    function onSearchTextChange(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
      setSearchTextFilter(event.target.value);
    }
    const filterSearchtextResult: IPaymentMethodAttr[] = filterSearchText(
      data,
      searchTextFilter
    );

    // Add payment method
    const [isAddingPaymentMethod, setAddingPaymentMethod] = useState<
      false | { mode: "ADD" }
    >(false);
    const openAddModal = useCallback((): void => {
      setAddingPaymentMethod({ mode: "ADD" });
    }, []);
    const closeAddModal = useCallback((): void => {
      setAddingPaymentMethod(false);
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
    const handleAddPaymentMethodSubmit = useCallback(
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
        await addPaymentMethod({
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
    const [isUpdatingPaymentMethod, setUpdatingPaymentMethod] = useState<
      false | { mode: "UPDATE" }
    >(false);
    const openUpdateModal = useCallback((): void => {
      setUpdatingPaymentMethod({ mode: "UPDATE" });
    }, []);
    const closeUpdateModal = useCallback((): void => {
      setUpdatingPaymentMethod(false);
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

    const tableHeaders: IHeaderConfig[] = [
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

    return (
      <Container>
        <Row>
          <Col100>
            <Row>
              <h2>{t("organization.tabs.billing.paymentMethods.title")}</h2>
              <Table
                columnToggle={false}
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                  position: "right",
                }}
                dataset={filterSearchtextResult}
                defaultSorted={{ dataField: "brand", order: "asc" }}
                exportCsv={false}
                extraButtons={
                  <Row>
                    <Can do={"api_mutations_add_payment_method_mutate"}>
                      <Button
                        id={"addPaymentMethod"}
                        onClick={openAddModal}
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
                        id={"updatePaymentMethod"}
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
                        id={"removePaymentMethod"}
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
                headers={tableHeaders}
                id={"tblPaymentMethods"}
                pageSize={10}
                search={false}
                selectionMode={{
                  clickToSelect: canRemove || canUpdate,
                  hideSelectColumn: !canRemove && !canUpdate,
                  mode: "radio",
                  onSelect: setCurrentRow,
                }}
                striped={true}
              />
            </Row>
          </Col100>
        </Row>
        {isAddingPaymentMethod === false ? undefined : (
          <AddPaymentModal
            onClose={closeAddModal}
            onSubmit={handleAddPaymentMethodSubmit}
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
