import { gql } from "@apollo/client";

const GET_USER_WELCOME = gql`
  query GetUserWelcome {
    me {
      organizations {
        name
      }
      userEmail
    }
  }
`;

const ADD_ORGANIZATION = gql`
  mutation AddOrganization($name: String!) {
    addOrganization(name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

const AUTOENROLL_DEMO = gql`
  mutation AutoenrollDemo {
    autoenrollDemo {
      success
    }
  }
`;

const ADD_GROUP_MUTATION = gql`
  mutation AddGroupMutation(
    $description: String!
    $groupName: String!
    $hasMachine: Boolean!
    $hasSquad: Boolean!
    $language: Language!
    $organizationName: String!
    $service: ServiceType!
    $subscription: SubscriptionType!
  ) {
    addGroup(
      description: $description
      groupName: $groupName
      hasMachine: $hasMachine
      hasSquad: $hasSquad
      language: $language
      organizationName: $organizationName
      service: $service
      subscription: $subscription
    ) {
      success
    }
  }
`;

export {
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  AUTOENROLL_DEMO,
  GET_USER_WELCOME,
};
