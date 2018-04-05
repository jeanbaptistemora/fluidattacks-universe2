/* globals mixPanelDashboard:true, location, mixpanel, $ */
/**
 * @file mixPanelDashboard.js
 * @author engineering@fluidattacks.com
 */
/*
 * Object to control mixpanel calls
 */
mixPanelDashboard = {};

/*
 * MixPanel localhost Fixer
 */
let result = false;
const none_int = -1;
mixPanelDashboard.isProduction = function () {
  result = false;
  try {
    result = location.toString().indexOf("localhost:8000") !== none_int;
    return result;
  }
  catch (err) {
    result = false;
    return result;
  }
};

mixPanelDashboard.trackSearch = function (trackName, userEmail, project) {
  if (mixPanelDashboard.isProduction()) {
    return false;
  }
  mixpanel.track(
    trackName,
    {
      "Email": userEmail,
      "Project": project
    }
  );
};

mixPanelDashboard.trackReadEventuality = function (userName, userEmail, Organization, project, id) {
  if (mixPanelDashboard.isProduction()) {
    return false;
  }
  mixpanel.track(
    "ReadEventuality",
    {
      "Email": userEmail,
      "EventID": id,
      "Name": userName,
      Organization,
      "Project": project
    }
  );
};

mixPanelDashboard.trackReports = function (trackName, userName, userEmail, Organization, project) {
  if (mixPanelDashboard.isProduction()) {
    return false;
  }
  mixpanel.track(
    trackName,
    {
      "Email": userEmail,
      "Name": userName,
      Organization,
      "Project": project
    }
  );
};

mixPanelDashboard.trackFinding = function (trackName, userEmail, id) {
  if (mixPanelDashboard.isProduction()) {
    return false;
  }
  mixpanel.track(
    trackName,
    {
      "Email": userEmail,
      "FindingID": id
    }
  );
};

mixPanelDashboard.trackFindingDetailed = function (trackName, userName, userEmail, Organization, project, id) {
  if (mixPanelDashboard.isProduction()) {
    return false;
  }
  mixpanel.track(
    trackName,
    {
      "Email": userEmail,
      "FindingID": id,
      "Name": userName,
      Organization,
      "Project": project
    }
  );
};
