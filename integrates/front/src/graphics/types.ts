export interface IGraphicProps {
  bsHeight: number;
  documentName: string;
  documentType: string;
  entity: string;
  footer?: JSX.Element | string;
  generatorName: string;
  generatorType: string;
  reportMode: boolean;
  subject: string;
  title: string;
}
