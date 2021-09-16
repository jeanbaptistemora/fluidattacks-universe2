---
id: front-technologies
title: Front Technologies
sidebar_label: Front Technologies
slug: /development/front-technologies
---

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

    > **_NOTE:_**
    > Google Chrome might cause trouble
    > because of invalid https certificates in localhost.
    > If the bundle fails to load,
    > you can go to
    > chrome://flags/#allow-insecure-localhost
    > and enable that flag

1. Lint your code

    ```bash
    ./make integrates.front.lint
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
    ./make integrates.front.test
    ```
