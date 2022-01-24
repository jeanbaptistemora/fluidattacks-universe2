import _ from "lodash";
import React from "react";

import { Container } from "./styles";

import type { IPaymentMethodAttr } from "../types";
import { DataTableNext } from "components/DataTableNext/index";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Col100, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IOrganizationBillingPaymentMethodsProps {
  paymentMethods: IPaymentMethodAttr[];
}

export const OrganizationBillingPaymentMethods: React.FC<IOrganizationBillingPaymentMethodsProps> =
  ({
    paymentMethods,
  }: IOrganizationBillingPaymentMethodsProps): JSX.Element => {
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
                dataset={data}
                defaultSorted={{ dataField: "brand", order: "asc" }}
                exportCsv={false}
                headers={tableHeaders}
                id={"tblBillingPaymentMethods"}
                pageSize={10}
                search={false}
              />
            </Row>
          </Col100>
        </Row>
      </Container>
    );
  };
