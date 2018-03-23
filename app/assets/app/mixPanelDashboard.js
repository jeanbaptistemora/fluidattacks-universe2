/*globals mixPanelDashboard:true, location, mixpanel, $ */
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
var result = false;
var none_int = -1;
mixPanelDashboard.isProduction = function () {
    result = false;
    try {
        result = location.toString().indexOf("localhost:8000") !== none_int;
        return result;
    } catch (e) {
        result = false;
        return result;
    }
};

mixPanelDashboard.trackSearch = function (trackName, userEmail, project) {
    if (mixPanelDashboard.isProduction()) { return false; }
    mixpanel.track(
        trackName,
        {
            "Email": userEmail,
            "Project": project
        }
    );
};

mixPanelDashboard.trackReadEventuality = function (userName, userEmail, Organization, project, id) {
    if (mixPanelDashboard.isProduction()) { return false; }
    mixpanel.track(
        "ReadEventuality",
        {
            "Name": userName,
            "Email": userEmail,
            "Organization": Organization,
            "Project": project,
            "EventID": id
        }
    );
};

mixPanelDashboard.trackReports = function (trackName, userName, userEmail, Organization, project) {
    if (mixPanelDashboard.isProduction()) { return false; }
    mixpanel.track(
        trackName,
        {
            "Name": userName,
            "Email": userEmail,
            "Organization": Organization,
            "Project": project
        }
    );
};

mixPanelDashboard.trackFinding = function (trackName, userEmail, id) {
    if (mixPanelDashboard.isProduction()) { return false; }
    mixpanel.track(
        trackName,
        {
            "Email": userEmail,
            "FindingID": id
        }
    );
};

mixPanelDashboard.trackFindingDetailed = function (trackName, userName, userEmail, Organization, project, id) {
    if (mixPanelDashboard.isProduction()) { return false; }
    mixpanel.track(
        trackName,
        {
            "Name": userName,
            "Email": userEmail,
            "Organization": Organization,
            "Project": project,
            "FindingID": id
        }
    );
};
