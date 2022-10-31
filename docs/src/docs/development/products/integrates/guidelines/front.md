---
id: front
title: Front
sidebar_label: Front
slug: /development/integrates/guidelines/front
---

## Overview

Integrates' frontend is a web application
built with [React][react] and [TypeScript][ts].

## Browser support

Supported browsers are listed in [requirements](/machine/web/arm#requirements).

Thanks to [TypeScript][ts],
we can use newer ECMAScript language features,
as it already takes care of that when traspiling,
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
  Keep state to a minimum.
- _There's a component for that_:
  If there isn't, feel free to create it.
- _No need to reinvent the wheel_:
  Sometimes, third party packages have already figured it out.

## Getting started

To view the changes reflected as you edit the code, you can run:

```bash
  m . /integrates/front
```

## Linting

The frontend uses [ESLint][eslint]
and [Prettier][prettier]
to enforce compliance with a defined coding style.

To view and auto-fix linting issues, you can run:

```bash
  m . /integrates/front/lint
```

## Testing

The frontend uses [Jest][jest] as a test runner and
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

- Transfered state:
  This makes up the majority of the frontend state.
  Data loaded from the backend is managed by the [Apollo Client][apollo].
- Forms: Their ephemeral state is managed by [Formik][formik].
- Local state:
  [useState][usestate] and [Context][context] where needed.

### API Client

The frontend uses the [Apollo Client][apollo] to interact with the backend.

You can use the `useQuery` hook to load data
and the `useMutation` hook to trigger create, update or delete operations.

Refer to Apollo's documentation for more details.

### Forms

The frontend uses [Formik][formik] to power its forms, fields and validations.

Refer to Formik's documentation for more details.

### Routing

The frontend uses [React Router][router] to declare routes and
manage navigation between them.

You can use the `<Route>` and `<Switch>` components to declare routes,
the `useParams` hook to get the URL parameters,
the `<Link>` component for declarative navigation,
and the `useHistory` hook for imperative navigation.

Refer to React Router's documentation for more details.

### Styling

The frontend uses [styled-components][styled] and
[Tachyons][tachyons] to create and compose UI styles.

You can declare styled components with the `styled` tag,
reference tachyons classes,
and also add custom css as needed.

Refer to styled-components's documentation for more details.

### Internationalization

The frontend uses [i18next][i18n] to manage translations.

While we currently support only English,
more languages may be added later on,
making it a good idea to avoid hardcoding texts,
having them instead as translations.

You can declare your texts in the respective file for the language,
and use the `useTranslation` hook to access them in the component.

Refer to i18next's documentation for more details.

### Dependencies

The frontend uses [npm][npm] as its package manager.

When adding or updating dependencies,
keep [this requirement](/criteria/requirements/302) in mind.
Always make sure to pin the dependency to an exact version,
as semantic versioning is often unreliable and may cause regressions
due to unexpected incompatibilities.

Refer to https://github.com/fluidattacks/makes#makenodejslock
if you need to generate a lock file
without having Node.js installed on your computer.

### Logging

`console.log` is not allowed per https://eslint.org/docs/latest/rules/no-console

You can use `src/utils/logger.ts`,
which sends errors and warnings to Bugsnag,
the bug tracking platform we currently use.

To access Bugsnag, sign in to your Okta account.
If you can't find the app,
feel free to request access via help@fluidattacks.com

## Design

Visual consistency and clarity are key to provide users with a good experience.
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

Helpful tools that enhance development experience when working on the frontend:

- https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en
- https://chrome.google.com/webstore/detail/apollo-client-devtools/jdkknkkbebbapilgoeccciglkfbmbnfm
- https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
- https://marketplace.visualstudio.com/items?itemName=firsttris.vscode-jest-runner
- https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode
- https://semver.npmjs.com/

## Troubleshooting

Helpful tips and tricks that have proven to be useful
to diagnose issues when working on the frontend:

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

[react]: https://reactjs.org/
[ts]: https://www.typescriptlang.org/
[eslint]: https://eslint.org/
[prettier]: https://prettier.io/
[jest]: https://jestjs.io/
[rtl]: https://testing-library.com/docs/react-testing-library/intro/
[apollo]: https://www.apollographql.com/docs/react/
[formik]: https://formik.org/
[usestate]: https://reactjs.org/docs/hooks-state.html
[context]: https://reactjs.org/docs/context.html
[router]: https://v5.reactrouter.com/
[styled]: https://styled-components.com/
[tachyons]: https://tachyons.io/
[i18n]: https://react.i18next.com/
[npm]: https://www.npmjs.com/
[rtl-debug]: https://testing-library.com/docs/dom-testing-library/api-debugging/
