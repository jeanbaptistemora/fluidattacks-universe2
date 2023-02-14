---
id: frontend
title: Frontend
sidebar_label: Frontend
slug: /development/products/integrates/frontend
---

## Overview

Integrates' frontend is a client-side rendered web application
built with [React][react] and [TypeScript][ts].

## Browser support

Supported browsers are listed
in the [requirements](/machine/web/arm#requirements) section.

Thanks to [TypeScript][ts],
we can use newer ECMAScript language features,
as it takes care of downleveling as needed when transpiling,
but as for runtime features,
it is important to ensure compatibility.

Helpful resources:

- https://caniuse.com/
- https://kangax.github.io/compat-table/es6/

## Principles

- _Functional_:
  The view should be a function of state and props.
  The codebase only uses functional components,
  avoids direct mutations and favors a declarative style.
- _The state should not exist_:
  Keep the state to a minimum.
- _There's a component for that_:
  If there isn't, feel free to create it.
- _No need to reinvent the wheel_:
  Sometimes, third-party packages have already figured it out.

## Getting started

To view the changes reflected as you edit the code, you can run:

```bash
  m . /integrates/front
```

## Linting

The front uses [ESLint][eslint]
and [Prettier][prettier]
to enforce compliance with a defined coding style.

To view and auto-fix linting issues, you can run:

```bash
  m . /integrates/front/lint
```

## Testing

The front uses [Jest][jest] as a test runner and
the utilities provided by [React Testing Library][rtl]
to test the UI behavior from a user perspective.

To execute the test cases on your computer, you can run:

```bash
  m . /integrates/front/test
```

## Core

### State Management

:::note
State management is a constantly evolving topic in react applications.
:::

- Transferred state:
  This makes up the majority of the frontend state.
  Data loaded from the backend is managed by the [Apollo Client][apollo].
- Forms: Their ephemeral state is managed by [Formik][formik].
- Local state:
  [useState][usestate] and [Context][context] where needed.

### API Client

The front uses the [Apollo Client][apollo] to interact with the backend.

You can use the `useQuery` hook to load data
and the `useMutation` hook to trigger create, update or delete operations.

Refer to Apollo's documentation for more details.

### Forms

The front uses [Formik][formik] to power its forms, fields and validations.

You can use the `<Formik>` component,
with inputs from `src/components/Input` to compose forms,
and [Yup][yup] to declare a validation schema to be checked on submit.

Refer to Formik and Yup's documentation for more details.

### Tables

The front uses [TanStack Table][table] to power its data tables,
fitting them with features such as
sorting, pagination, column toggling, row expansion, exports and more.

You can use the `<Table>` component,
from `src/components/Table` to build a table from a dataset and columns.

Refer to TanStack Table's documentation for more details.

### Authorization

:::note
Authorization is enforced by the backend (authz/model.py),
this is just a utility to prevent the user
from running into 'access denied' messages.
:::

Integrates uses [Attribute-based access control][abac]
to manage its authorization model,
and the front uses some utilities from [CASL][casl] to implement it.

You can do [conditional rendering][conditional]
based on what the user is allowed to access:

```tsx
import { Can } from "utils/authz/Can";

const DemoComponent = () => {
  return (
    <div>
      <Can I={"do_some_action"}>
        <p>{"Welcome"}</p>
      </Can>
      <Can I={"do_some_action"} not={true}>
        <p>{"Get outta here"}</p>
      </Can>
    </div>
  );
};
```

You can also use it outside JSX

```tsx
import { useAbility } from "@casl/react";
import { authzPermissionsContext } from "utils/authz/config";

const DemoComponent = () => {
  const permissions = useAbility(authzPermissionsContext);

  function handleClick() {
    if (permissions.can("do_some_action")) {
      alert("Welcome");
    } else {
      alert("Get outta here");
    }
  }

  return <button onClick={handleClick}>{"Click me"}</button>;
};
```

### Feature preview

In a constantly evolving product,
it may be useful to conduct [A/B testing][ab].

This strategy allows trying new ideas with a small subset of the users,
analyzing reception, iterating and improving before releasing them to everyone.

You can do [conditional rendering][conditional] based on user preference:

```tsx
import { featurePreviewContext } from "utils/featurePreview";

const DemoComponent = () => {
  const { featurePreview } = useContext(featurePreviewContext);

  if (featurePreview) {
    return <h1>{"Shiny new view"}</h1>;
  }

  return <h2>{"Current default view"}</h2>;
};
```

### Routing

The front uses [React Router][router] to declare routes and
manage navigation between them.

You can use the `<Route>` and `<Switch>` components to declare routes,
the `useParams` hook to get the URL parameters,
the `<Link>` component for declarative navigation,
and the `useHistory` hook for imperative navigation.

Refer to React Router's documentation for more details.

### Styling

The front uses [styled-components][styled] and
[Tachyons][tachyons] to create and compose UI styles.

You can declare styled components with the `styled` tag,
reference tachyons classes,
and also add custom CSS as needed.

Refer to styled-components and Tachyons' documentation for more details.

### Internationalization

The front uses [i18next][i18n] to manage translations.

While we currently support only English,
more languages may be added later on,
making it a good idea to avoid hardcoding texts
and having them instead as translations.

You can declare texts in the respective file for the language,
at `src/utils/translations`,
and then, use the `useTranslation` hook to access them in the component.

Refer to i18next's documentation for more details.

### Dependencies

The front uses [npm][npm] as its package manager.

When adding or updating dependencies,
keep [this requirement](/criteria/requirements/302) in mind.
Always make sure to pin the dependency to an exact version,
as semantic versioning is often unreliable and may cause regressions
due to unexpected incompatibilities.

Refer to https://github.com/fluidattacks/makes#makenodejslock
if you need to generate a lock file
without having Node.js installed on your computer.

### Logging

`console.log` usage is not allowed
per https://eslint.org/docs/latest/rules/no-console,
though it can still be used locally for debugging.

You can use `src/utils/logger.ts`,
which sends errors and warnings to Bugsnag,
the bug-tracking platform we currently use.

To access Bugsnag, sign in to your Okta account.
If you can't find the app,
feel free to request access via help@fluidattacks.com

## Design

Visual consistency is key to providing users with a good experience.
This motivation led to the creation of the components library,
a collection of UI components that can be easily used by developers
and continuously refined by designers.

You can access it on:

- Production:
  https://integrates.front.production.fluidattacks.com/trunk/storybook/index.html
- Developer branch:
  `integrates.front.development.fluidattacks.com/branch-name/storybook/index.html`
- Locally:
  `localhost:6006`, after running `m . /integrates/front storybook`

Most of these components are implementations of the design guidelines
defined by the Customer Experience team at Fluid Attacks.

## Tooling

Helpful tools that enhance development experience when working on the front:

- https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
- https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en
- https://chrome.google.com/webstore/detail/apollo-client-devtools/jdkknkkbebbapilgoeccciglkfbmbnfm
- https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
- https://marketplace.visualstudio.com/items?itemName=firsttris.vscode-jest-runner
- https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode
- https://semver.npmjs.com/

## Troubleshooting

Helpful tips and tricks that have proven to be useful
when diagnosing issues on the front:

- How do I do [X]?:
  Refer to the documentation of the core packages mentioned above.
  If that doesn't solve it,
  feel free to reach out for help on the development channel
  or chat with a domain expert.
- Why is [X] not working?:
  Look for error traces on the browser console
  or use breakpoints to inspect the code
  and variable values as it runs
  https://developer.chrome.com/docs/devtools/javascript/breakpoints/.
- Is the backend returning an error?:
  Use the network tab to view more details about the request
  and its response https://developer.chrome.com/docs/devtools/network/.
- Can't find an element on a test?:
  Try increasing the [print limit][rtl-debug]
  to view more details and suggestions
  or try a snippet on https://testing-playground.com/.

## Frontend Testing

Frontend tests are classified into the following levels:

- **Unit tests:**
  From the test,
  start to create a function.

- **End-to-end tests:**
  These tests verify that the flows a user
  follows work as expected,
  for example:
  loading a web page,
  logging in,
  verifying email notifications,
  and online payments,
  validating that these flows are done and that they work correctly.

[react]: https://reactjs.org/
[ts]: https://www.typescriptlang.org/
[eslint]: https://eslint.org/
[prettier]: https://prettier.io/
[jest]: https://jestjs.io/
[rtl]: https://testing-library.com/docs/react-testing-library/intro/
[apollo]: https://www.apollographql.com/docs/react/
[formik]: https://formik.org/
[yup]: https://github.com/jquense/yup#readme
[table]: https://tanstack.com/table/v8/docs/guide/introduction
[usestate]: https://reactjs.org/docs/hooks-state.html
[context]: https://reactjs.org/docs/context.html
[abac]: https://en.wikipedia.org/wiki/Attribute-based_access_control
[casl]: https://casl.js.org/v6/en/package/casl-react
[conditional]: https://reactjs.org/docs/conditional-rendering.html
[ab]: https://en.wikipedia.org/wiki/A/B_testing
[router]: https://v5.reactrouter.com/
[styled]: https://styled-components.com/
[tachyons]: https://tachyons.io/
[i18n]: https://react.i18next.com/
[npm]: https://www.npmjs.com/
[rtl-debug]: https://testing-library.com/docs/dom-testing-library/api-debugging/
