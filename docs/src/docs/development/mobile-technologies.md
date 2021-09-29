---
id: mobile-technologies
title: Mobile Technologies
sidebar_label: Mobile Technologies
slug: /development/mobile-technologies
---

## Technology stack

- *TypeScript:*
    a typed superset of JavaScript
    that compiles to plain JavaScript.

    To learn more,
    visit the TypeScript documentation page at
    https://www.typescriptlang.org/docs/handbook/basic-types.html.

- *React Native:*
    A framework for building
    native apps with React.

    We also use React
    for Integrates web front-end.
    There are some differences
    between ReactJS and React Native,
    but the key ones are:

    - There are no HTML Elements,
        only React Components,
        although there is View,
        which is the closest you can get
        to a normal HTML
    - Since RN doesn't have a DOM concept
        and doesn't produce HTML,
        there is no CSS either.
        Though,
        there is an equivalent known as
        https://facebook.github.io/react-native/docs/stylesheet.html[StyleSheet]
    - Most ReactJS libraries
        are compatible with React Native,
        actually,
        we can share code between front/ and mobile/
        as long as it doesn't call
        web-specific JS features
        such as `document` or `window`

        To learn more,
        visit the RN documentation page at
        http://facebook.github.io/react-native/.

- **Expo:**
    A set of tools,
    libraries, and services
    that allows us to
    build react-native apps faster
    in a less bare-metal way.

    > Expo is kind of like Rails
    > for React Native.
    > Lots of things are set up for you,
    > so it's quicker to get started
    > and on the right path.
    > With Expo,
    > you don't need Xcode
    > or Android Studio.
    > You just write JavaScript

    Thanks to Expo
    we can make use of several development goodies,
    such as the development server,
    that allows us to run the app
    by scanning a QR code
    and enables live-reloading,
    so it's a matter of editing
    and saving the source file
    to almost instantly see the changes
    reflected in the app.

    Keep in mind
    that our dependencies will fetch react-native
    from Expo's forked repo,
    and that's because RN is at a fast-changing rate,
    so this is in favor
    of a more stable development experience.
    Expo releases SDKs periodically,
    introducing new features,
    bug fixes,
    and the latest additions
    to React and React Native.

    To learn more,
    visit the Expo documentation page at
    https://docs.expo.io/introduction/faq/.

- **Apollo Client:**
    A comprehensive state management library
    for JavaScript that enables you
    to manage both local and remote data
    with GraphQL

    To learn more,
    visit the documentation page at
    https://www.apollographql.com/docs/react/.

- **Jest:**
    A JavaScript testing framework
    worked on full-time
    by Facebook's JavaScript Foundation team.

    To learn more,
    visit the Jest documentation page at
    https://jestjs.io/docs/en/getting-started.

## Development workflow

1. Start the backend server

    > **NOTE:**
    > Due to security policies in android and iOS,
    > mobile apps won't trust self-signed HTTPS certs.
    > To workaround that limitation
    > you must run the backend as HTTP
    > using the following command

    ```bash
    m  . /integrates/back dev-mobile
    ```

1. Start the app bundler

    ```bash
    ./m integrates.mobile
    ```

    Then,
    scan the generated QR code
    with the Expo client App:
    https://play.google.com/store/apps/details?id=host.exp.exponent

    > **IMPORTANT:**
    > Make sure your PC and Smartphone
    > are in the same network
    > so they can reach each other

    > **NOTE:**
    > Due to Apple limitations imposed on Expo,
    > iOS users won't see an option
    > to scan QR in the client.
    > Use the camera app instead

    > **NOTE:**
    > Default permissions changed in iOS 14.
    > If you are developing on apple devices,
    > make sure to allow network access
    > for the Expo client
    > ![Expo Network Access](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211886/docs/development/mobile-technologies/expo_network_access_f4k0se.webp)

1. Lint your code

    ```bash
    ./m integrates.mobile.lint
    ```

1. Test your code

    ```bash
    ./m integrates.mobile.test
    ```

1. Review the changes
    in the 'ephemeral' environment

    After the pipeline passes,
    you can try out your changes,
    scanning the QR code
    in the following URL:
    https://expo.io/@developmentatfluid/asm?release-channel=branch_name
