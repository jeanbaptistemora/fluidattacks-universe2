/* globals mixPanelDashboard:true, location, mixpanel, $ */
/**
 * @file mixPanelDashboard.js
 * @author engineering@fluidattacks.com
 */
/*
 * Object to control mixpanel calls
 */
const mixPanelDashboard = {};

/*
 * MixPanel localhost Fixer
 */
let result = false;
const noneInt = -1;
mixPanelDashboard.isProduction = function isProduction () {
  result = false;
  try {
    result = location.toString().indexOf("localhost:8000") !== noneInt;
    return result;
  }
  catch (err) {
    result = false;
    return result;
  }
};

mixPanelDashboard.trackSearch = function trackSearch (trackName, userEmail, project) {
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

mixPanelDashboard.trackReadEventuality = function trackReadEventuality (userName, userEmail, Organization, project, id) {
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

mixPanelDashboard.trackReports = function trackReports (trackName, userName, userEmail, Organization, project) {
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

mixPanelDashboard.trackFinding = function trackFinding (trackName, userEmail, id) {
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

mixPanelDashboard.trackFindingDetailed = function trackFindingDetailed (trackName, userName, userEmail, Organization, project, id) {
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
