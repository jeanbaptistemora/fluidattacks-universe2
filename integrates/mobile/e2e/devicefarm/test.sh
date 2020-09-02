# shellcheck shell=bash

export APPIUM_VERSION=1.16.0
export CI_COMMIT_REF_NAME="__CI_COMMIT_REF_NAME__"
export PYTHON_VERSION=3

# shellcheck disable=SC1091
    cd "${DEVICEFARM_TEST_PACKAGE_PATH}" \
&&  . bin/activate \
&&  pip install -r requirements.txt \
&&  avm "${APPIUM_VERSION}" \
&&  ln -s \
      /usr/local/avm/versions/$APPIUM_VERSION/node_modules/.bin/appium \
      /usr/local/avm/versions/$APPIUM_VERSION/node_modules/appium/bin/appium.js \
&&  {
      appium \
        --log-timestamp \
        --default-capabilities "{
          \"app\": \"${DEVICEFARM_APP_PATH}\",
          \"chromedriverExecutable\": \"${DEVICEFARM_CHROMEDRIVER_EXECUTABLE}\",
          \"deviceName\": \"${DEVICEFARM_DEVICE_NAME}\",
          \"platformName\": \"${DEVICEFARM_DEVICE_PLATFORM_NAME}\",
          \"platformVersion\": \"${DEVICEFARM_DEVICE_OS_VERSION}\",
          \"udid\": \"${DEVICEFARM_DEVICE_UDID}\"
        }" \
      >> "${DEVICEFARM_LOG_DIR}/appiumlog.txt" 2>&1 \
      &
    } \
&&  start_appium_timeout=0 \
&&  while true;
    do
      if [ $start_appium_timeout -gt 60 ];
      then
        echo "appium server never started in 60 seconds. Exiting";
        exit 1;
      fi;
      if grep -q "Appium REST http interface listener started on 0.0.0.0:4723" < "${DEVICEFARM_LOG_DIR}/appiumlog.txt";
      then
        echo "Appium REST http interface listener started on 0.0.0.0:4723";
        break;
      else
        echo "Waiting for appium server to start. Sleeping for 1 second";
        sleep 1;
        start_appium_timeout=$((start_appium_timeout+1));
      fi;
    done \
&&  pytest tests/ \
      --exitfirst \
      --verbose
