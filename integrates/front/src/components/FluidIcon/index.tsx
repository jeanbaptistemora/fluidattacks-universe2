import React from "react";
import { ReactSVG } from "react-svg";

import style from "components/FluidIcon/index.css";
import authorsIcon from "resources/authors.svg";
import avabilityHighIcon from "resources/availability_high.svg";
import avabilityLowIcon from "resources/availability_low.svg";
import avabilityNoneIcon from "resources/availability_none.svg";
import calendarIcon from "resources/calendar.svg";
import caretDownIcon from "resources/caret_down.svg";
import caretRightIcon from "resources/caret_right.svg";
import complexityHighIcon from "resources/complexity_high.svg";
import complexityLowIcon from "resources/complexity_low.svg";
import confidentialityHighIcon from "resources/confidentiality_high.svg";
import confidentialityLowIcon from "resources/confidentiality_low.svg";
import confidentialityNoneIcon from "resources/confidentiality_none.svg";
import defaultIcon from "resources/default_finding_state.svg";
import deleteIcon from "resources/delete.svg";
import editIcon from "resources/edit.svg";
import exportIcon from "resources/export.svg";
import failIcon from "resources/fail.svg";
import findingsIcon from "resources/findings.svg";
import fixedVulnerabilitiesIcon from "resources/fixed_vulnerabilities.svg";
import graphIcon from "resources/graph.svg";
import importIcon from "resources/import.svg";
import integrityHighIcon from "resources/integrity_high.svg";
import integrityLowIcon from "resources/integrity_low.svg";
import integrityNoneIcon from "resources/integrity_none.svg";
import loadingIcon from "resources/loading.svg";
import okIcon from "resources/ok.svg";
import openVulnerabilitiesIcon from "resources/open_vulnerabilities.svg";
import privilegesHighIcon from "resources/privileges_high.svg";
import privilegesLowIcon from "resources/privileges_low.svg";
import privilegesNoneIcon from "resources/privileges_none.svg";
import scopeChangedIcon from "resources/scope_changed.svg";
import scopeUnchangedIcon from "resources/scope_unchanged.svg";
import searchIcon from "resources/search.svg";
import terminalIcon from "resources/terminal.svg";
import totalIcon from "resources/total.svg";
import totalVulnerabilitiesIcon from "resources/total_vulnerabilities.svg";
import userIcon from "resources/user.svg";
import userNoneIcon from "resources/user_none.svg";
import userRequiredIcon from "resources/user_required.svg";
import vectorAdjacentIcon from "resources/vector_adjacent.svg";
import vectorLocalIcon from "resources/vector_local.svg";
import vectorNetworkIcon from "resources/vector_network.svg";
import vectorPhysicalIcon from "resources/vector_physical.svg";
import verifiedIcon from "resources/verified.svg";
import vulnerabilitiesIcon from "resources/vulnerabilities.svg";

const icons = {
  authors: authorsIcon,
  availabilityHigh: avabilityHighIcon,
  availabilityLow: avabilityLowIcon,
  availabilityNone: avabilityNoneIcon,
  calendar: calendarIcon,
  caretDown: caretDownIcon,
  caretRight: caretRightIcon,
  circle: defaultIcon,
  complexityHigh: complexityHighIcon,
  complexityLow: complexityLowIcon,
  confidentialityHigh: confidentialityHighIcon,
  confidentialityLow: confidentialityLowIcon,
  confidentialityNone: confidentialityNoneIcon,
  delete: deleteIcon,
  edit: editIcon,
  export: exportIcon,
  fail: failIcon,
  findings: findingsIcon,
  fixedVulnerabilities: fixedVulnerabilitiesIcon,
  graph: graphIcon,
  import: importIcon,
  integrityHigh: integrityHighIcon,
  integrityLow: integrityLowIcon,
  integrityNone: integrityNoneIcon,
  loading: loadingIcon,
  ok: okIcon,
  openVulnerabilities: openVulnerabilitiesIcon,
  privilegesHigh: privilegesHighIcon,
  privilegesLow: privilegesLowIcon,
  privilegesNone: privilegesNoneIcon,
  scopeChanged: scopeChangedIcon,
  scopeUnchanged: scopeUnchangedIcon,
  search: searchIcon,
  terminal: terminalIcon,
  total: totalIcon,
  totalVulnerabilities: totalVulnerabilitiesIcon,
  user: userIcon,
  userNone: userNoneIcon,
  userRequired: userRequiredIcon,
  vectorAdjacent: vectorAdjacentIcon,
  vectorLocal: vectorLocalIcon,
  vectorNetwork: vectorNetworkIcon,
  vectorPhysical: vectorPhysicalIcon,
  verified: verifiedIcon,
  vulnerabilities: vulnerabilitiesIcon,
};

export interface IFluidIconProps {
  height?: string;
  icon: keyof typeof icons;
  width?: string;
}

export const FluidIcon: React.FC<IFluidIconProps> = (
  props: Readonly<IFluidIconProps>
): JSX.Element => {
  const { icon, height = "16px", width = "16px" } = props;

  /*
   * The ReactSVG beforeInjection prop works by mutating the SVGElement pass as
   * an argument, please refer to https://www.npmjs.com/package/react-svg#api.
   */
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  function setStyles(svg: SVGElement): void {
    svg.setAttribute("heigth", height);
    svg.setAttribute("width", width);
  }

  return (
    <div className={style.container}>
      <ReactSVG beforeInjection={setStyles} src={icons[icon]} />
    </div>
  );
};
