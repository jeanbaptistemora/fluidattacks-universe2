/* tslint:disable-next-line:no-any
 *   Using any here because the dataset may be anything that the generator needs.
 *   However, at the moment of declaration of the generator the data argument
 *   is a specific type, so it fits into the context.
 */
export type DataType = any;
export type NodeType = HTMLDivElement;
export type GeneratorType = (data: DataType, width: number, height: number) => NodeType;

export interface IGraphicProps {
  bsClass?: string;
  data: DataType;
  footer?: JSX.Element | string;
  generator: GeneratorType;
  title?: JSX.Element | string;
}
