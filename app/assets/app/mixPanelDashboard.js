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
    result = false;
    try{
        result = location.toString().indexOf("localhost:8000") != -1;
    }catch(e){
        result = false;
    }finally{
        return result;
    }
};

mixPanelDashboard.trackSearchFinding = function(userEmail, project){
    if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "SearchFinding", {
            "Email": userEmail,
            "Project": project
        }
    );
};

mixPanelDashboard.trackReadFinding = function(userEmail, id){
    if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "ReadFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};

mixPanelDashboard.trackUpdateFinding = function(userEmail, id){
    if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "UpdateFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};

mixPanelDashboard.trackDeleteFinding = function(userEmail, id){
    if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        "DeleteFinding", {
            "Email": userEmail,
            "FindingID": id
        }
    );
};