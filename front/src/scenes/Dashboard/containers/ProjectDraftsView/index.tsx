/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatDrafts, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { GET_DRAFTS } from "./queries";
import { IProjectDraftsAttr, IProjectDraftsBaseProps } from "./types";

const tableHeaders: IHeader[] = [
  { align: "center", dataField: "reportDate", header: "Date", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "type", header: "Type", isDate: false, isStatus: false, width: "8%" },
  { align: "center", dataField: "title", header: "Title", isDate: false, isStatus: false, wrapped: true, width: "18%" },
  {
    align: "center", dataField: "description", header: "Description", isDate: false, isStatus: false, width: "30%",
    wrapped: true,
  },
  { align: "center", dataField: "severityScore", header: "Severity", isDate: false, isStatus: false, width: "8%" },
  {
    align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", isDate: false, isStatus: false,
    width: "6%",
  },
  { align: "center", dataField: "isExploitable", header: "Exploitable", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "isReleased", header: "Released", isDate: false, isStatus: false, width: "10%" },
];

const projectDraftsView: React.FC<IProjectDraftsBaseProps> = (props: IProjectDraftsBaseProps): JSX.Element => {
  const { projectName } = props.match.params;

  const goToFinding: ((rowInfo: { id: string }) => void) = (rowInfo: { id: string }): void => {
    mixpanel.track(
      "ReadDraft",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    location.hash = `#!/project/${projectName}/drafts/${rowInfo.id}/description`;
  };

  const handleQryResult: ((qrResult: IProjectDraftsAttr) => void) = (qrResult: IProjectDraftsAttr): void => {
    mixpanel.track(
      "ProjectDrafts",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    hidePreloader();
  };

  return (
    <Query query={GET_DRAFTS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({loading, error, data}: QueryResult<IProjectDraftsAttr>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting project drafts", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {

            return (
              <React.StrictMode>
                <p>{translate.t("project.findings.help_label")}</p>
                <DataTable
                  dataset={formatDrafts(data.project.drafts)}
                  enableRowSelection={false}
                  exportCsv={true}
                  headers={tableHeaders}
                  id="tblDrafts"
                  onClickRow={goToFinding}
                  pageSize={15}
                  search={true}
                  selectionMode="none"
                />
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

export { projectDraftsView as ProjectDraftsView };
