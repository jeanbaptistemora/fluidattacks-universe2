/**
 * @file mixPanelDashboard.js
 * @author engineering@fluid.la
 */
/*
 * Object to control mixpanel calls
 */
mixPanelDashboard = {}; 
/*
 * MixPanel localhost Fixer
 */
mixPanelDashboard.isProduction = function(){
    return location.toString().indexOf("localhost:8000") == -1;
};

mixPanelDashboard.trackSearchFinding = function(project){
    //if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "SearchFinding", {
            "Email": userEmail,
            "Project": project
        }
    );
};

mixPanelDashboard.trackReadFinding = function(id){
    //if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "ReadFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};

mixPanelDashboard.trackUpdateFinding = function(id){
    //if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "UpdateFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};

mixPanelDashboard.trackDeleteFinding = function(id){
    //if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "DeleteFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};