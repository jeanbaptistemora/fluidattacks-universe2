/* eslint-disable no-underscore-dangle */
import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { GET_SUBSCRIPTIONS } from "scenes/Dashboard/containers/NotificationsView/queries";
import type {
  ISubscriptionName,
  ISubscriptionNameDataSet,
  ISubscriptionsNames,
} from "scenes/Dashboard/containers/NotificationsView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const NotificationsView: React.FC = (): JSX.Element => {
  const [fieldValue] = useState();

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: translate.t("searchFindings.notificationTable.notification"),
      width: "99%",
    },
    {
      dataField: "subscribeEmail",
      header: translate.t("searchFindings.notificationTable.email"),
      width: "1%",
    },
  ];

  const { data: dataEnum } = useQuery<ISubscriptionsNames>(GET_SUBSCRIPTIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("configuration.errorText"));
        Logger.warning(
          "An error occurred loading the subscriptions info",
          error
        );
      });
    },
  });

  const subscriptions: ISubscriptionName[] =
    _.isUndefined(dataEnum) || _.isEmpty(dataEnum)
      ? []
      : dataEnum.__type.enumValues.map(
          (name: ISubscriptionName): ISubscriptionNameDataSet => {
            return {
              ...name,
              subscribeEmail: (
                <Col100>
                  <input checked={fieldValue} type={"checkbox"} />
                </Col100>
              ),
            };
          }
        );

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <DataTableNext
              bordered={true}
              dataset={subscriptions}
              exportCsv={false}
              headers={tableHeaders}
              id={"tblNotifications"}
              pageSize={10}
              search={false}
            />
          </Col100>
        </Row>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button disabled={false} id={"config-confirm"} type={"submit"}>
                {translate.t("configuration.confirm")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { NotificationsView };
