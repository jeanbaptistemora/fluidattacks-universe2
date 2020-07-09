export declare type EntityType = "group" | "organization" | "tag";

export interface IChartsGenericViewProps {
  entity: EntityType;
  reportMode: boolean;
  subject: string;
}
