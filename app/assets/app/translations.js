/**
 * @file translations.js
 * @author engineering@fluid.la
 */
 /**
 * Establece la configuracion de las traducciones de integrates
 * @config {AngularJS}
 * @param {Object} $translateProvider
 * @return {undefined}
 */
integrates.config(['$translateProvider', function($translateProvider) {
    $translateProvider.useSanitizeValueStrategy('sanitize');
    var translations = {
        'logout': {
            'message': 'Are you sure?',
            'title': 'Close Session',
            'ok': 'Logout',
            'cancel': 'Cancel'
        },
        'left_menu': {
            'first': 'Findings',
            'second': 'Events'
        },
        'breadcumbs': {
            'findings': {
                'page': 'Findings',
                'function': 'Findings by project'
            },
            'eventualities':{
                'page': 'Events',
                'function': 'Events by project'
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
                    'placeholder': 'FLUID project name'
                }
            },
            'filter_labels':{
                'findings': 'Findings',
                'cardinalities': 'Vulnerabilities',
                'criticity': 'Total Criticity Found',
                'closure': 'Vulnerabilities remediated'
            },
            'filter_buttons':{
                'advance': 'Progress',
                'documentation': 'Documentation'
            },
            'table':{
                'headings':{
                    'action': 'Action',
                    'age': 'Age',
                    'timestamp': 'Date',
                    'type': 'Type',
                    'finding': 'Title',
                    'vulnerability': 'Description',
                    'criticity': 'Severity',
                    'cardinality': '# Vuln.',
                    'state': 'Status',
                    'exploit': 'Exploit'
                }
            },
            'descriptions':{
              'description1': '',
              'description2': 'Click',
              'description3': 'to see more details'
            },
            'eventualities':{
              'description': 'Click to see more details'
            },
            'project_buttons':{
              'back': 'Go Back',
              'delete': 'Delete'
            },
            'project_labels':{
              'type': 'Type',
              'criticity': 'Criticity',
              'vulnerabilities': 'Vulnerabilities',
              'status': 'Status',
              'report': 'Report Date',
              'project': 'FLUID\'s Project',
              'client': 'Customer\'s Project'
            },
            'tab_description':{
              'description_name': 'Description',
              'type': 'Finding Type',
              'detailed': 'Detailed',
              'general': 'General',
              'title': 'Title',
              'stage': 'Scenario',
              'category': 'Category',
              'risk': 'Risk Value',
              'probability': 'Probability',
              'severity': 'Severity',
              'description': 'Description',
              'requirements': 'Requirements',
              'where': 'Where',
              'vectors': 'Attack Vectors',
              'threat': 'Threat',
              'recommendation': 'Recommendation',
              'system': 'Committed Systems',
              'records': 'Compromised Records',
              'totalrecords': 'Total Compromised Records',
              'weakness': 'Weakness',
              'editable': 'Edit',
              'update': 'Update'
            },
            'tab_cssv2':{
              'description_name': 'Severity',
              'vector': 'Access Vector',
              'confidenciality': 'Confidentiality Impact',
              'integrity': 'Integrity Impact',
              'availability': 'Availability Impact',
              'authentication': 'Authentication',
              'exploitability': 'Exploitability',
              'confidence': 'Confidence Level',
              'resolution':'Resolution Level',
              'complexity': 'Access Complexity',
              'editable': 'Edit',
              'update':'Update'
            },
            'tab_tracking':{
              'open': 'Open Vulnerabilities',
              'close': 'Closed Vulnerabilities',
              'finding': 'Reported Finding',
              'cicle': 'Closing cycle'
            },
            'tab_evidence':{
              'evidence_name':'Evidence',
              'editable': 'Edit',
              'detail': 'Detail',
              'update':'Update'
            },
            'pop_table':{
               'type': 'Type',
               'date': 'Date',
               'status': 'Status',
               'details':'Description'
            },
            'event_table':{
               'id': 'ID',
               'date': 'Date',
               'type': 'Type',
               'status': 'Status'
             },
             'page_head':{
               'breadcrumb':{
                'project': 'Project'
             }
           }
        },
        'main_content':{
          'projects':{
            'title': 'My Projects',
            'description1': 'You can check the details of a project ',
            'description2': 'clicking',
            'description3': ' on it'
          },
          'eventualities':{
                'title': 'My Events',
                'description_1': 'You can check the details of an event ',
                'description_2': 'clicking',
                'description_3': 'on it'
              }
        },
        'grapExploit':{
          'title': 'Exploitability',
          'exploit_label': 'Exploitable',
          'nonexploit_label': 'Not Exploitable'
        },
        'grapType':{
          'title': 'Finding Type',
          'seg_label': 'Vulnerability',
          'hig_label': 'Hygiene'
        },
        'grapStatus':{
          'title': 'Findings by Status',
          'open_label': 'Open',
          'partial_label': 'Partial',
          'close_label': 'Closed'
        },
        'tab_container':{
          'findings': 'Findings',
          'eventualities': 'Events'
        },
        'event_by_name':{
          'page_head':{
            'search': 'Search',
            'vuln_by_proj': 'Events by project ',
            'search': 'Search',
          },
          'main_content':{
            'id': 'ID',
            'name': 'Name',
            'placeholder':'Name or ID project'
          },
          'modal_avance':{
            'title': 'Events Resume'
          },
          'modal_ver':{
            'type': 'Type',
            'analyst': 'Analyst',
            'f_proj': 'FLUID\'s Project',
            'c_proj': 'Customer\'s Project',
            'client': 'Client',
            'detail': 'Description',
            'date': 'Date',
            'affec': 'Affection',
            'ok': 'OK'
         },
          'modal_edit':{
            'type': 'Type',
            'analyst': 'Analyst',
            'f_proj': 'FLUID\'s Project',
            'c_proj': 'Customer\'s Project',
            'client': 'Client',
            'detail': 'Description',
            'date': 'Date',
            'affec': 'Affection',
            'close': 'Close',
            'refresh': 'Update'
         },
         'row':{
           'muted': 'Please wait, loading...',
           'event': 'EVENTS',
           'affect': 'TOTAL AFFECTATION'
         },
         'table':{
           'date': 'Date',
           'type': 'Type',
           'affect':'Affectation',
           'status':'Status'
         }
       }
    };
    var traducciones = {
        'logout': {
            'message': 'Esta seguro de que desea salir?',
            'title':'Cerrar Sesion',
            'ok': 'Salir',
            'cancel': 'Cancelar'
        },
        'left_menu': {
            'first': 'Hallazgos',
            'second': 'Eventualidades'
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
                    'analysis': 'Analisis',
                    'application': 'Aplicacion',
                    'binary': 'Binario',
                    'code': 'Codigo',
                    'infrastructure': 'Infraestructura'
                },
                'search':{
                    'placeholder': 'Nombre del proyecto en Fluid'
                }
            },
            'filter_labels':{
                'findings': 'Hallazgos',
                'cardinalities': 'Vulnerabilidades',
                'criticity': 'Criticidad Total Encontrada',
                'closure': 'Vulnerabilidades remediadas'
            },
            'filter_buttons':{
                'advance': 'Avance',
                'documentation': 'Documentacion'
            },
            'table':{
                'headings':{
                    'age': 'Edad',
                    'action': 'Accion',
                    'timestamp': 'Fecha',
                    'type': 'Tipo',
                    'finding': 'Titulo',
                    'vulnerability': 'Descripcion',
                    'criticity': 'Severidad',
                    'cardinality': '# Vuln.',
                    'state': 'Estado',
                    'exploit': 'Explotable'
                }
            },
            'descriptions':{
              'description1': 'Haz',
              'description2': 'click',
              'description3': 'para ver mas detalles del hallazgo'
            },
            'eventualities':{
              'description': 'Haz click para ver el detalle'
            },
            'project_buttons':{
              'back': 'Volver',
              'delete': 'Eliminar'
            },
            'project_labels':{
              'type': 'Tipo',
              'criticity': 'Criticidad',
              'vulnerabilities': 'Vulnerabilidades',
              'status': 'Estado',
              'report': 'Fecha Reporte',
              'project': 'Proyecto Fluid',
              'client': 'Proyecto Cliente'
            },
            'tab_description':{
              'description_name': 'Descripcion',
              'type': 'Tipo Hallazgo',
              'detailed': 'Detallado',
              'general': 'General',
              'title': 'Titulo',
              'stage': 'Escenario',
              'category': 'Categoria',
              'risk': 'Valor Riesgo',
              'probability': 'Probabilidad',
              'severity': 'Severidad',
              'description': 'Descripcion',
              'requirements': 'Requisitos',
              'where': 'Donde',
              'vectors': 'Vectores de ataque',
              'threat': 'Amenaza',
              'recommendation': 'Recomendacion',
              'system': 'Sistemas Comprometidos',
              'records': 'Registros Comprometidos',
              'totalrecords': 'Total Registros Comprometidos',
              'weakness': 'Debilidad',
              'editable': 'Hacer Editable',
              'update': 'Actualizar'
            },
            'tab_cssv2':{
              'description_name': 'Severidad',
              'vector': 'Vector de Acceso',
              'confidenciality': 'Impacto Confidencialidad',
              'integrity': 'Impacto Integridad',
              'availability': 'Impacto Disponibilidad',
              'authentication': 'Autenticacion',
              'exploitability': 'Explotabilidad',
              'confidence': 'Nivel Confianza',
              'resolution':'Nivel Resolucion',
              'complexity': 'Complejidad Acceso',
              'editable': 'Hacer Editable',
              'update':'Actualizar'
            },
            'tab_tracking':{
              'open': 'Vulnerabilidades Abiertas',
              'close': 'Vulnerabilidades Cerradas',
              'finding': 'Hallazgo reportado',
              'cicle': 'Ciclo de cierre'
            },
            'tab_evidence':{
              'evidence_name':'Evidencia',
              'editable': 'Hacer Editable',
              'detail': 'Detalle',
              'update':'Actualizar'
            },
            'pop_table':{
               'type': 'Tipo',
               'date': 'Fecha',
               'status': 'Estado',
               'details':'Descripcion'
             },
             'event_table':{
               'id': 'ID',
               'date': 'Fecha',
               'type': 'Tipo',
               'status': 'Estado'
             },
             'page_head':{
               'breadcrumb':{
                'project': 'Proyecto'
             }
           }
        },
        'main_content':{
          'projects':{
            'title': 'Mis Proyectos',
            'description1': 'Para ver el detalle del proyecto debes hacer ',
            'description2': 'click',
            'description3': ' sobre el proyecto'
          },
          'eventualities':{
                 'title': 'Mis Eventualidades',
                 'description_1': 'Para ver el detalle de la eventualidad debes hacer',
                 'description_2': 'click',
                 'description_3': 'sobre la eventualidad'
           }
        },
        'grapExploit':{
          'title': 'Distribucion por Explotabilidad',
          'exploit_label': 'Explotable',
          'nonexploit_label': 'No Explotable'
        },
        'grapType':{
          'title': 'Distribucion por Tipo Hallazgo',
          'seg_label': 'Vulnerabilidad',
          'hig_label': 'Higiene'
        },
        'grapStatus':{
          'title': 'Hallazgos por Estado',
          'open_label': 'Abiertos',
          'partial_label': 'Parciales',
          'close_label': 'Cerrados'
        },
        'tab_container':{
          'findings': 'Hallazgos',
          'eventualities': 'Eventualidades'
        },
        'event_by_name':{
          'page_head':{
            'search': 'Busqueda',
            'vuln_by_proj': 'Eventualidades por proyecto'
          },
          'main_content':{
            'id': 'ID',
            'name': 'Nombre',
            'placeholder':'Nombre o ID de proyecto'
          },
          'modal_avance':{
            'title': 'Resumen eventualidades'
          },
          'modal_ver':{
            'type': 'Tipo',
            'analyst': 'Analista',
            'f_proj': 'Proyecto Fluid',
            'c_proj': 'Proyecto Cliente',
            'client': 'Cliente',
            'detail': 'Detalle',
            'date': 'Fecha',
            'affec': 'Afectacion',
            'ok': 'OK'
         },
          'modal_edit':{
            'type': 'Tipo',
            'analyst': 'Analista',
            'f_proj': 'Proyecto Fluid',
            'c_proj': 'Proyecto Cliente',
            'client': 'Cliente',
            'detail': 'Detalle',
            'date': 'Fecha',
            'affec': 'Afectacion',
            'close': 'Cerrar',
            'refresh': 'Actualizar'
         },
         'row':{
           'muted': 'Un momento por favor, cargando...',
           'event': 'EVENTUALIDADES',
           'affect': 'AFECTACION TOTAL'
         },
         'table':{
           'date': 'Fecha',
           'type': 'Tipo',
           'affect':'Afectacion',
           'status':'Estado'
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
