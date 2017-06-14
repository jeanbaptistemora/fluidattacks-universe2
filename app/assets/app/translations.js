/**
 * @file translations.js
 * @author engineering@fluid.la
 */
 /**
 * Establece la configuracion de las rutas para integrates
 * @config {AngularJS} 
 * @param {Object} $stateProvider
 * @param {Object} $urlRouterProvider
 * @return {undefined}
 */
integrates.config(['$translateProvider', function($translateProvider) {
    var translations = {
		'left_menu': {
			'first': 'Search Findings',
			'second': 'Search eventualities'
		},
		'breadcumbs': {
			'findings': {
				'page': 'Findings',
				'function': 'Findings by project'
			},
			'eventualities':{
				'page': 'Eventualities',
				'function': 'Eventualities by project'
			}
		},
		'search_findings': {
			'filter_menu':{
				'filter_select':{
					'any': 'All',
					'analysis': 'Analysis',
					'application': 'Application',
					'binary': 'Binary',
					'code': 'Code',
					'infrastructure': 'Infrastructure'
				},
				'search':{
					'placeholder': 'Fluid project name'
				}
			},
			'filter_labels':{
				'findings': 'Findings',
				'cardinalities': 'Cardinalities'
			},
			'filter_buttons':{
				'advance': 'Advance',
				'documentation': 'Documentation'
			},	
			'table':{
				'headings':{
					'action': 'Action',
					'type': 'Type',
					'finding': 'Finding',
					'vulnerability': 'Vulnerability',
					'criticity': 'Criticity',
					'cardinality': 'Cardinality'
				}
			}
		}
    };
    var traducciones = {
		'left_menu': {
			'first': 'Buscar Hallazgos',
			'second': 'Buscar Eventualidades'
		},
		'breadcumbs': {
			'findings': {
				'page': 'Hallazgos',
				'function': 'Hallazgos por proyecto'
			},
			'eventualities':{
				'page': 'Eventualidades',
				'function': 'Eventualidades por proyecto'
			}
		},
		'search_findings': {
			'filter_menu':{
				'filter_select':{
					'any': 'Todos',
					'analysis': 'Análisis',
					'application': 'Aplicacion',
					'binary': 'Binario',
					'code': 'Código',
					'infrastructure': 'Infrastructura'
				},
				'search':{
					'placeholder': 'Nombre del proyecto en Fluid'
				}
			},
			'filter_labels':{
				'findings': 'Hallazgos',
				'cardinalities': 'Cardinalidades'
			},
			'filter_buttons':{
				'advance': 'Avance',
				'documentation': 'Documentacion'
			},	
			'table':{
				'headings':{
					'action': 'Acción',
					'type': 'Tipo prueba',
					'finding': 'Hallazgo',
					'vulnerability': 'Vulnerabilidad',
					'criticity': 'Criticidad',
					'cardinality': 'Cardinalidad'
				}
			}
		}
    };
    if(localStorage['lang'] === undefined){
		localStorage['lang'] = 'es';
	}
	$translateProvider
		.translations('en', translations)
		.translations('es', traducciones)
		.preferredLanguage(localStorage['lang']);

}]);
