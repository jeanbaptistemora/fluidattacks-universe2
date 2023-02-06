interface IGroupAttr {
  name: string;
}

interface IOrganizationComplianceStandardsProps {
  organizationId: string;
}

interface IUnfulfilledRequirementAttr {
  id: string;
  title: string;
}

interface IUnfulfilledStandardAttr {
  standardId: string;
  title: string;
  unfulfilledRequirements: IUnfulfilledRequirementAttr[];
}

export type {
  IGroupAttr,
  IOrganizationComplianceStandardsProps,
  IUnfulfilledStandardAttr,
  IUnfulfilledRequirementAttr,
};
