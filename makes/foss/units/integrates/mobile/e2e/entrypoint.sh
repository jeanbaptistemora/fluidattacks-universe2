# shellcheck shell=bash

function main {
  export ANDROID_SDK_ROOT='__argAndroidSdk__/libexec/android-sdk'
  export CI_COMMIT_REF_NAME
  export JAVA_HOME='__argJava__'
  local host='127.0.0.1'
  local port='5037'

  pushd integrates/mobile/e2e \
    && echo '[INFO] Making sure ports are free...' \
    && makes-kill-port "${port}" 4723 \
    && curl -sSo expoClient.apk '__argApkUrl__' \
    && echo '[INFO] Copying dependencies...' \
    && copy __argIntegratesMobileE2eNpm__ node_modules \
    && echo '[INFO] Looking for available android devices...' \
    && echo '[INFO] Make sure to enable USB debugging and set' \
      'your mobile device to file transfer mode' \
    && "${ANDROID_SDK_ROOT}/platform-tools/adb" wait-for-device \
    && { npx --no-install appium --default-capabilities capabilities/android.json & } \
    && makes-wait 10 "${host}:${port}" \
    && pytest ./ \
      --exitfirst \
      --verbose \
    && makes-kill-port "${port}" 4723 \
    && rm -rf node_modules \
    && popd \
    || return 1
}

main "${@}"
