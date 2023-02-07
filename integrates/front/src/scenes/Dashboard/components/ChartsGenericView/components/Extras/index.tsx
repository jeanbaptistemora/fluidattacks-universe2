import { useLazyQuery, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faDownload, faFileCsv } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Gap } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import {
  GET_VULNERABILITIES_URL,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/components/ChartsGenericView/queries";
import type {
  EntityType,
  IChartsGenericViewProps,
  ISubscriptionsToEntityReport,
} from "scenes/Dashboard/components/ChartsGenericView/types";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import type { IVerifyFn } from "scenes/Dashboard/components/VerifyDialog/types";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

const ChartsGenericViewExtras: React.FC<IChartsGenericViewProps> = ({
  entity,
  subject,
}: IChartsGenericViewProps): JSX.Element => {
  const { t } = useTranslation();
  const entityName: EntityType = entity;
  const downloadPngUrl: URL = new URL(
    "/graphics-report",
    window.location.origin
  );
  downloadPngUrl.searchParams.set("entity", entity);
  downloadPngUrl.searchParams.set(entityName, subject);

  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const { data: dataSubscriptions } = useQuery<ISubscriptionsToEntityReport>(
    SUBSCRIPTIONS_TO_ENTITY_REPORT,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading subscriptions info", error);
        });
      },
    }
  );

  const [getUrl] = useLazyQuery(GET_VULNERABILITIES_URL, {
    onCompleted: (result: {
      organization: { vulnerabilitiesUrl: string };
    }): void => {
      setIsVerifyDialogOpen(false);
      openUrl(result.organization.vulnerabilitiesUrl);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Stakeholder could not be verified":
            msgError(t("group.findings.report.alerts.nonVerifiedStakeholder"));
            break;
          case "Exception - The verification code is invalid":
            msgError(t("group.findings.report.alerts.invalidVerificationCode"));
            break;
          case "Exception - Document not found":
            msgError(t("analytics.sections.extras.vulnerabilitiesUrl.error"));
            break;
          case "Exception - The verification code is required":
            msgError(t("profile.mobileModal.alerts.requiredVerificationCode"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error(
              "An error occurred getting vulnerabilities url for organization",
              error.message
            );
        }
      });
    },
  });

  const getVulnerabilitiesUrl = useCallback(
    (verificationCode: string): void => {
      getUrl({
        variables: {
          identifier: subject,
          verificationCode,
        },
      });
    },
    [getUrl, subject]
  );

  const onRequestReport = useCallback(
    (setVerifyCallbacks: IVerifyFn): (() => void) =>
      (): void => {
        setVerifyCallbacks(
          (verificationCode: string): void => {
            getVulnerabilitiesUrl(verificationCode);
          },
          (): void => {
            setIsVerifyDialogOpen(false);
          }
        );
        setIsVerifyDialogOpen(true);
      },
    [getVulnerabilitiesUrl]
  );

  if (_.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Gap>
        <ExternalLink
          download={`charts-${entity}-${subject}.png`}
          href={downloadPngUrl.toString()}
        >
          <Button variant={"primary"}>
            <FontAwesomeIcon icon={faDownload} />
            &nbsp;
            {t("analytics.sections.extras.download")}
          </Button>
        </ExternalLink>
        {entity === "organization" ? (
          <Can do={"api_resolvers_organization_vulnerabilities_url_resolve"}>
            <VerifyDialog isOpen={isVerifyDialogOpen}>
              {(setVerifyCallbacks): JSX.Element => {
                return (
                  <Tooltip
                    disp={"inline-block"}
                    id={"analytics.sections.extras.vulnerabilitiesUrl.id"}
                    place={"right"}
                    tip={t(
                      "analytics.sections.extras.vulnerabilitiesUrl.tooltip"
                    )}
                  >
                    <Button
                      onClick={onRequestReport(setVerifyCallbacks)}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faFileCsv} />
                      &nbsp;
                      {t("analytics.sections.extras.vulnerabilitiesUrl.text")}
                    </Button>
                  </Tooltip>
                );
              }}
            </VerifyDialog>
          </Can>
        ) : undefined}
      </Gap>
    </React.StrictMode>
  );
};

export { ChartsGenericViewExtras };
