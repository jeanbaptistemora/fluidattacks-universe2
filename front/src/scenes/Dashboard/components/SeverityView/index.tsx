export interface ISeverityViewProps {
  criticity: number;
  cssv2base: number;
  dataset: {
    accessComplexity: string;
    accessVector: string;
    authentication: string;
    availabilityImpact: string;
    confidenceLevel: string;
    confidentialityImpact: string;
    exploitability: string;
    integrityImpact: string;
    resolutionLevel: string;
  };
  isEditing: boolean;
  onUpdate(values: ISeverityViewProps["dataset"]): void;
}
