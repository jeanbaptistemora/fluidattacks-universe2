# shellcheck shell=bash

function main {
  export EXPO_ANDROID_KEYSTORE_PASSWORD
  export EXPO_ANDROID_KEY_PASSWORD
  export JAVA_HOME=__envJava__
  export JAVA_OPTS="
    -Xmx6G
    -XX:+HeapDumpOnOutOfMemoryError
    -XX:+UnlockExperimentalVMOptions
    -XX:+UseCGroupMemoryLimitForHeap
    -XX:+UseG1GC
  "
  export TURTLE_ANDROID_DEPENDENCIES_DIR="${HOME}/.turtle/androidDependencies"
  export TURTLE_WORKING_DIR_PATH="${HOME}/.turtle/workingdir"
  export GRADLE_OPTS="
    -Dorg.gradle.configureondemand=true
    -Dorg.gradle.daemon=false
    -Dorg.gradle.jvmargs=\"${JAVA_OPTS}\"
    -Dorg.gradle.parallel=true
    -Dorg.gradle.project.android.aapt2FromMavenOverride=${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk/build-tools/30.0.3/aapt2
  "
  export GRADLE_DAEMON_DISABLED="1"
  local secrets=(
    EXPO_PASS
    EXPO_USER
    GOOGLE_SERVICES_APP
  )
  local linked_deps=(
    "react-native-ssl-pinning@1.5.4"
  )
  local shell_app_path="${TURTLE_WORKING_DIR_PATH}/android/sdk41/"

  if has_any_file_changed \
    'integrates/mobile/app.json' \
    'integrates/mobile/assets/icon.png' \
    'integrates/mobile/assets/splash.png'; then
    echo '[INFO] Logging in to AWS...' \
      && aws_login_prod integrates \
      && sops_export_vars __envSecretsProd__ "${secrets[@]}" \
      && pushd integrates/mobile \
      && echo '[INFO] Copying dependencies...' \
      && copy __envSetupIntegratesMobileDevRuntime__ node_modules \
      && echo "${GOOGLE_SERVICES_APP}" > google-services.json \
      && EXPO_ANDROID_KEYSTORE_PASSWORD=${EXPO_PASS} \
      && EXPO_ANDROID_KEY_PASSWORD=${EXPO_PASS} \
      && echo "[INFO] Using NodeJS $(node -v)" \
      && echo "[INFO] Using Java $(java -version 2>&1)" \
      && npx --no-install expo login \
        --username "${EXPO_USER}" \
        --password "${EXPO_PASS}" \
        --non-interactive \
      && aws s3 cp \
        --recursive \
        "s3://fluidintegrates.build/mobile/certs" \
        ./certs \
      && echo '[INFO] Patching Android SDK...' \
      && mkdir -p "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk" \
      && cp -r --no-preserve=mode,ownership \
        __envAndroidSdk__/libexec/android-sdk/* \
        "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk" \
      && touch "${TURTLE_ANDROID_DEPENDENCIES_DIR}/sdk/.ready" \
      && echo '[INFO] Downloading shell app...' \
      && npx --no-install turtle setup:android \
        --sdk-version 41.0.0 \
      && echo '[INFO] Linking native deps...' \
      && cp ./shell/react-native.config.js "${shell_app_path}" \
      && pushd "${shell_app_path}" \
      && npm install --save-exact \
        yarn@1.22.10 \
        @react-native-community/cli@5.0.1 \
        "${linked_deps[@]}" \
      && npm install \
      && for dep in "${linked_deps[@]}"; do
        npx react-native link "${dep}" \
          || return 1
      done \
      && popd \
      && echo '[INFO] Building Android app...' \
      && npx --no-install turtle build:android \
        --username "${EXPO_USER}" \
        --password "${EXPO_PASS}" \
        --keystore-alias fluidintegrates-keystore \
        --keystore-path ./certs/keystore-dev.jks \
        --output output/asm.aab \
        --release-channel "${CI_COMMIT_REF_NAME}" \
        --type app-bundle \
      && rm -rf .expo certs google-services.json node_modules \
      && popd \
      || return 1
  else
    echo '[INFO] No relevant files were modified, skipping build' \
      && return 0
  fi
}

main "${@}"
