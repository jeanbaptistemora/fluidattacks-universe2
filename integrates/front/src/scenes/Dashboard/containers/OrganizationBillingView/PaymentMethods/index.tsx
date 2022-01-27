import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";

import { AddPaymentModal } from "./AddPaymentMethodModal";
import { Container } from "./styles";

import {
  ADD_BILLING_PAYMENT_METHOD,
  REMOVE_BILLING_PAYMENT_METHOD,
} from "../queries";
import type { IPaymentMethodAttr } from "../types";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext/index";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IOrganizationBillingPaymentMethodsProps {
  organizationId: string;
  paymentMethods: IPaymentMethodAttr[];
  onUpdate: () => void;
}

export const OrganizationBillingPaymentMethods: React.FC<IOrganizationBillingPaymentMethodsProps> =
  ({
    organizationId,
    paymentMethods,
    onUpdate,
  }: IOrganizationBillingPaymentMethodsProps): JSX.Element => {
    // Data
    const data: IPaymentMethodAttr[] = paymentMethods.map(
      (paymentMethodData: IPaymentMethodAttr): IPaymentMethodAttr => {
        const isDefault: boolean = paymentMethodData.default;
        const capitalized: string = _.capitalize(paymentMethodData.brand);
        const brand: string = isDefault
          ? `${capitalized} ${translate.t(
              "organization.tabs.billing.paymentMethods.defaultPaymentMethod"
            )}`
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
    const closeModal = useCallback((): void => {
      setAddingPaymentMethod(false);
    }, []);
    const [addPaymentMethod] = useMutation(ADD_BILLING_PAYMENT_METHOD, {
      onCompleted: (): void => {
        onUpdate();
        closeModal();
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't add payment method", error);
        });
      },
    });
    const handlePaymentMethodSubmit = useCallback(
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
    const permissions: PureAbility<string> = useAbility(
      authzPermissionsContext
    );
    const canDelete: boolean = permissions.can(
      "api_mutations_remove_billing_payment_method_mutate"
    );
    const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
    const [removePaymentMethod, { loading: removing }] = useMutation(
      REMOVE_BILLING_PAYMENT_METHOD,
      {
        onCompleted: (): void => {
          onUpdate();
          setCurrentRow({});
          msgSuccess(
            translate.t(
              "organization.tabs.billing.paymentMethods.remove.success.body"
            ),
            translate.t(
              "organization.tabs.billing.paymentMethods.remove.success.title"
            )
          );
        },
        onError: ({ graphQLErrors }): void => {
          graphQLErrors.forEach((error): void => {
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't add payment method", error);
          });
        },
      }
    );
    const handleRemoveStakeholder: () => void = useCallback((): void => {
      void removePaymentMethod({
        variables: {
          organizationId,
          paymentMethodId: currentRow.id,
        },
      });
    }, [organizationId, currentRow.id, removePaymentMethod]);

    const tableHeaders: IHeaderConfig[] = [
      {
        align: "center",
        dataField: "brand",
        header: "Brand",
      },
      {
        align: "center",
        dataField: "lastFourDigits",
        header: "Last four digits",
      },
      {
        align: "center",
        dataField: "expirationMonth",
        header: "Expiration Month",
      },
      {
        align: "center",
        dataField: "expirationYear",
        header: "Expiration Year",
      },
    ];

    return (
      <Container>
        <Row>
          <Col100>
            <Row>
              <h2>
                {translate.t("organization.tabs.billing.paymentMethods.title")}
              </h2>
              <DataTableNext
                bordered={true}
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
                    <Can do={"api_mutations_add_billing_payment_method_mutate"}>
                      <Button onClick={openAddModal}>
                        <FontAwesomeIcon icon={faPlus} />
                        &nbsp;
                        {translate.t(
                          "organization.tabs.billing.paymentMethods.add"
                        )}
                      </Button>
                    </Can>
                    <Can
                      do={"api_mutations_remove_billing_payment_method_mutate"}
                    >
                      <Button
                        disabled={_.isEmpty(currentRow) || removing}
                        id={"removeUser"}
                        onClick={handleRemoveStakeholder}
                      >
                        <FontAwesomeIcon icon={faTrashAlt} />
                        &nbsp;
                        {translate.t(
                          "organization.tabs.billing.paymentMethods.remove.button"
                        )}
                      </Button>
                    </Can>
                  </Row>
                }
                headers={tableHeaders}
                id={"tblBillingPaymentMethods"}
                pageSize={10}
                search={false}
                selectionMode={{
                  clickToSelect: canDelete,
                  hideSelectColumn: !canDelete,
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
            onClose={closeModal}
            onSubmit={handlePaymentMethodSubmit}
          />
        )}
      </Container>
    );
  };
