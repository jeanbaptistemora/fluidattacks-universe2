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

mixPanelDashboard.trackPageView = function(trackName, pageName, pageUrl){
    if(mixPanelDashboard.isProduction()) return false;
    mixpanel.track(
        trackName, {
            "Page": pageName,
            "URL": pageUrl
        }
    );
};
