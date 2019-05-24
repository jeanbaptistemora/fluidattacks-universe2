// Patch graphql-tag typings since they make use of 'any'
import "graphql-tag";
import { DocumentNode } from "graphql";

declare module "graphql-tag" {
  export default function gql(literals: TemplateStringsArray): DocumentNode;
}
