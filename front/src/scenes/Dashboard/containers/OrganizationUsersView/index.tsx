import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import translate from "../../../../utils/translations/translate";

const organizationUsers: React.FC = (): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // State management

  // GraphQL Operations

  // Auxiliary operations

  // Render Elements
  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" />
    </React.StrictMode>
    );
};

export { organizationUsers as OrganizationUsers };
