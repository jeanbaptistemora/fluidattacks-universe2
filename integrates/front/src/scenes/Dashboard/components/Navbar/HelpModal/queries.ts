import { gql } from "@apollo/client";

const GET_GROUP_SERVICES = gql`
  query GetGroupServices($groupName: String!) {
    group(groupName: $groupName) {
      name
      serviceAttributes
    }
  }
`;

export { GET_GROUP_SERVICES };
