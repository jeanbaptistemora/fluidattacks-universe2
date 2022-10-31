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

To view and auto-fix linting issues you can run:

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

## Technology stack

- **TypeScript:**
  A typed superset of JavaScript
  that compiles to plain JavaScript.

  To learn more,
  visit the TypeScript documentation page at
  https://www.typescriptlang.org/docs/handbook/basic-types.html

- **ReactJS:**
  A JavaScript library
  for building user interfaces.

  To learn more,
  visit the documentation page at
  https://reactjs.org/.

- **Apollo GraphQL Client:**
  A complete state management library
  for JavaScript apps

  To learn more,
  visit the documentation page at
  https://www.apollographql.com/docs/react/.

- **Webpack:**
  A static module bundler
  for modern JavaScript applications

  To learn more,
  visit the documentation page at
  https://webpack.js.org/concepts/.

- **Jest:**
  A JavaScript testing framework
  worked on full-time
  by Facebook's JavaScript Foundation team.

  To learn more,
  visit the documentation page at
  https://jestjs.io/docs/en/getting-started.

## Development workflow

1. Start the development server

   ```bash
   m . /integrates/front
   ```

   The changes will be reflected
   as you edit and save the code.
   If it can't be instantly applied,
   the server will perform a full reload
   on the page you are working.

   You can read more
   about this functionality here:
   https://webpack.js.org/concepts/hot-module-replacement/

1. Lint your code

   ```bash
   m . /integrates/front/lint
   ```

   You have the option
   to lint in real time (with ESLint)
   and fix on save,
   by following the next steps:

   - Download the
     [VScode eslint extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
   - Go to settings.json in vscode
     and add these rules:

     ```json
     {
       // This tells the extension to lookup for node_modules in the front directory.
       "eslint.workingDirectories": ["front"],
       // This allows you to autofix linting errors on save.
       "editor.codeActionsOnSave": {
         "source.fixAll": true
       }
     }
     ```

1. Test your code

   ```bash
   m . /integrates/front/test
   ```

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
