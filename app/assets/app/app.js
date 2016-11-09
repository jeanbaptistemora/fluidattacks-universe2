/*
 * Configuracion para CSRF
 */ 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/*
 * Inicializacion de aplicacion en angular para Integrates
 */
var BASE = { production: "/integrates/",
             development: "/" };
BASE.url = BASE.development;
//definicion de modulos
var integrates = angular.module("FluidIntegrates", ['ui.router','ui.bootstrap']); 
//definicion de rutas y configuracion
integrates.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('home');
    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: 'assets/views/dashboard.html'
        })
        .state('VulnerabilitiesByName', {
            url: '/VulnerabilitiesByName',
            templateUrl: 'assets/views/search/vulns_by_name.html',
            controller: 'findingController'  
        })
        .state('EventualitiesByName', {
            url: '/EventualitiesByName',
            templateUrl: 'assets/views/search/event_by_name.html',
            controller: 'eventualityController'        
        })
        .state('AnalystForms',{
            url: '/AnaylistForms',
            templateUrl: 'assets/views/forms/analyst.html'
        })
        .state('ProductionForms',{
            url: '/ProductionForms',
            templateUrl: 'assets/views/forms/production.html'
        })
        .state('TalentForms',{
            url: '/TalentForms',
            templateUrl: 'assets/views/forms/talent.html'
        })
        .state('AuxilioForm',{
            url: '/AuxilioForm',
            templateUrl: 'assets/views/forms/auxilio.html'
        })
        
});