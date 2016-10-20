var BASE = { production: "/integrates/",
             development: "/" };
BASE.url = BASE.development;

var integrates = angular.module("FluidIntegrates", ['ui.router','ui.bootstrap']); 

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