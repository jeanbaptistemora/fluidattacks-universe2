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
    $translateProvider.useSanitizeValueStrategy('sanitizeParameters');
    var translations = {
        'logout': {
            'message': 'Are you sure?',
            'title': 'Close Session',
            'ok': 'Logout',
            'cancel': 'Cancel'
        },
        'left_menu': {
            'first': 'Findings',
            'second': 'Events',
            'third': 'Forms'
        },
        'forms': {
            'progress': 'Progress',
            'findings': 'Findings',
            'closure': 'Closure',
            'events': 'Events'
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
                'search':{
                    'placeholder': 'FLUID project name',
                    'button': 'Search',
                }
            },
            'filter_labels':{
                'findings': 'Findings',
                'cardinalities': 'Open Vulnerabilities',
                'criticity': 'Total Severity Found',
                'closure': 'Fixed vulnerabilities'
            },
            'filter_buttons':{
                'advance': 'Progress',
                'documentation': 'Documentation'
            },
            'table':{
                'headings':{
                    'action': 'Action',
                    'age': 'Age (Days)',
                    'timestamp': 'Date',
                    'type': 'Type',
                    'finding': 'Title',
                    'vulnerability': 'Description',
                    'criticity': 'Severity',
                    'cardinality': 'Open Vuln.',
                    'state': 'Status',
                    'exploit': 'Exploitable',
                    'treatment': 'Treatment'
                }
            },
            'descriptions':{
              'description1': '',
              'description2': 'Click',
              'description3': 'on a finding to see more details'
            },
            'eventualities':{
              'description': 'Click on an event to see more details'
            },
            'project_buttons':{
              'back': 'Back',
              'delete': 'Delete'
            },
            'project_labels':{
              'type': 'Type',
              'criticity': 'Severity',
              'vulnerabilities': 'Open Vulnerabilities',
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
              'cardinality': 'Open Vulnerabilities',
              'vectors': 'Attack Vectors',
              'threat': 'Threat',
              'recommendation': 'Recommendation',
              'system': 'Affected Systems',
              'records': 'Compromised Records',
              'totalrecords': 'Total Compromised Records',
              'weakness': 'Weakness',
              'editable': 'Edit',
              'update': 'Update',
              'treatment': 'Treatment',
              'treat_justification': 'Treatment Justification',
              'treat_manager': 'Treatment Manager',
              'edit_treatment': 'Edit',
              'update_treatment': 'Update',
              'update_treatmodal': 'Update Treatment',
              'remediated': 'Remediated',
              'remediated_finding': 'Finding remediated'
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
              'finding': 'Discovery',
              'cicle': 'Closing cycle'
            },
            'tab_evidence':{
              'evidence_name':'Evidence',
              'editable': 'Edit',
              'detail': 'Detail',
              'update':'Update',
              'alert':'In progress...',
              'animation_exploit':'Exploitation animation',
              'evidence_exploit':'Exploitation evidence'
            },
            'tab_comments':{
              'comments_name':'Comments'
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
            'description1': 'You can check the details of a project by ',
            'description2': 'clicking',
            'description3': ' on it',
            'project_title': 'FLUID\'s Project',
            'project_description': 'Description'
          },
          'eventualities':{
                'title': 'My Events',
                'description_1': 'You can check the details of an event by ',
                'description_2': 'clicking',
                'description_3': 'on it',
                'project_title': 'FLUID\'s Project',
                'date': 'Date',
                'type': 'Type',
                'description': 'Description',
                'close': 'CLOSE'
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
        'progress_mod':{
          'title': 'Progress Report',
          'finding': 'Finding'
        },
        'technical_report_mod':{
          'title': 'Technical Reports'
        },
        'executive_report_mod':{
          'title': 'Executive Reports'
        },
        'proj_alerts':{
          'search_title': 'News!',
          'search_cont': 'Searching Project...',
          'attent_title': 'Attention!',
          'attent_cont': 'Empty search',
          'updated_title': 'Correct!',
          'updated_cont': 'Updated ;)',
          'error_textsad': 'There is an error :(',
          'error_text': 'There is an error',
          'event_title': 'Searching',
          'event_wait': 'Wait a moment please...',
          'event_select': 'You must select an event',
          'event_required': 'Name or ID is required',
          'event_internal': 'Internal error, loading...',
          'event_formstack': 'Unable to access Formstack',
          'event_positiveint': 'Affectation must be a positive integer or zero',
          'event_updated': 'Event updated',
          'event_exist':'This proyect has no vulnerabilities or does not exist',
          'no_finding':'We could not find the finding!',
          'error_severity':'Severity must be an integer bewteen 0 and 5',
          'wrong_severity':'You must calculate severity correctly',
          'not_found':'We could not find it!',
          'differ_comment':'You must enter a new treatment justification',
          'empty_comment':'You must enter a treatment justification!',
          'short_comment':'You must enter a justification of at least 50 characters and maximum 80 characters',
          'congratulation':'Congratulations',
          'updated_treat':'Treatment updated',
          'remediated_success':'This finding was marked as remediated. A request to verify the solution was sent'
        },
        'tab_container':{
          'findings': 'Findings',
          'eventualities': 'Events'
        },
        'event_by_name':{
          'page_head':{
            'search': 'Search',
            'vuln_by_proj': 'Events by project ',
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
         },
         'btn_group':{
           'watch': 'WATCH!',
           'edit': 'EDIT!',
           'resume': 'RESUME!'
         }
       },
       'event_formstack':{
         'type':{
           'auth_attack': 'Authorization for special attack',
           'toe_differs': 'ToE differs from what was approved',
           'high_approval': 'High availability approval',
           'incor_supplies': 'Incorrect or missing supplies',
           'explic_suspend': 'Client explicitly suspends project',
           'approv_change': 'Client approves the change of ToE',
           'cancel_proj': 'Client cancels the project/milestone',
           'det_attack': 'Client detects an attack',
           'other': 'other',
           'inacc_ambient': 'Inaccessible ambient',
           'uns_ambient': 'Unstable ambient',
           'unknown':'-'
         },
         'status':{
           'solve': 'Solved',
           'unsolve': 'Unsolved',
           'unknown':'-'
         }
       },
       'finding_formstack':{
         'actor':{
           'any_internet': 'Anyone on Internet',
           'any_costumer': 'Any costumer of the organization',
           'some_costumer': 'Only some costumers of the organization',
           'any_access': 'Anyone with access to the station',
           'any_employee': 'Any employee of the organization',
           'some_employee': 'Only some employees',
           'one_employee': 'Only one employee',
           'default': '-'
         },
         'authentication':{
           'any_authen': '0.704 | None: Authentication is not required',
           'single_authen': '0.560 | Single: Single authentication point',
           'multiple_authen': '0.450 | Multiple: Multiple authentication points',
           'default':'-'
         },
         'category':{
           'update_base': 'Update and configure components security baselines',
           'define_model': 'Define the authorization model considering the principle of minimum privilege',
           'performance': 'Performance',
           'event': 'Event',
           'avoid_technical': 'Avoid exposing the technical information of the application, servers and platforms.',
           'exclude_data': 'Exclude sensitive data from source code and event log',
           'strengt_authen': 'Strengthen controls in authentication and session management',
           'strengt_process': 'Strengthen controls in file processing',
           'strengt_protect': 'Strengthen the protection of stored data related to passwords or cryptographic keys',
           'validate_input': 'Implement controls to validate input data',
           'maintain': 'Maintainability',
           'record_event': 'Record events for traceability and audit',
           'secure_protoc': 'Use secure communication protocols',
           'validate_http': 'Validate the integrity of transactions in HTTP requests',
           'default':'-'
         },
         'complexity':{
           'high_complex': '0.350 | High: Special conditions are required like administrative access',
           'medium_complex': '0.610 | Medium: Some conditions are required like system access',
           'low_complex': '0.710 | Low: No special conditions are required',
           'default':'-'
         },
         'scenario':{
           'anon_inter': 'Anonymous from Internet',
           'anon_intra': 'Anonymous from Intranet',
           'infra_scan': 'Infrastructure scan',
           'unauth_extra': 'Unauthorized Extranet user',
           'auth_inter': 'Authorized Internet user',
           'unauth_inter': 'Unauthorized Internet user',
           'auth_intra': 'Authorized Intranet user',
           'unauth_inter': 'Unauthorized Internet user',
           'default': '-'
         },
         'status':{
           'open': 'Open',
           'close': 'Closed',
           'part_close': 'Partially closed',
           'default': '-'
         },
         'exploitability':{
           'improbable': '0.850 | Improbable: There is no exploit',
           'conceptual': '0.900 | Conceptual: There are laboratory tests',
           'functional': '0.950 | Functional: There is an exploit',
           'high': '1.000 | High: Exploit is not required or it can be automated',
           'default': '-'
         },
         'exploitable':{
           'yes': 'Yes',
           'no': 'No',
           'default': '-'
         },
         'confidenciality':{
           'none': '0 | None: There is no impact',
           'partial': '0.275 | Partial: Access to information but no control over it',
           'complete': '0.660 | Complete: Total control over information related with the target',
           'default': '-'
         },
         'availability':{
           'none': '0 | None: There is no impact',
           'partial': '0.275 | Partial: There is intermittency in the access to the target',
           'complete': '0.660 | Complete: There is a total target fallen',
           'default': '-'
         },
         'integrity':{
           'none': '0 | None: There is no impact',
           'partial': '0.275 | Partial: Posibility of modify some target information',
           'complete': '0.660 | Complete: Posibility of modify all target information',
           'default': '-'
         },
         'confidence':{
           'not_confirm': '0.900 | Not confirmed: There are few sources that recognize vulnerability',
           'not_corrob': '0.950 | Not corroborared: Vulnerability is recognized by unofficial sources',
           'confirmed': '1.000 | Confirmed: The vulnerability is recognized by the manufacturer',
           'default': '-'
         },
         'resolution':{
           'palliative': '0.950 | Palliative: There is a patch that was not published by the manufacturer',
           'official': '0.870 | Official: There is an manufacturer available patch',
           'temporal': '0.900 | Temporal: There are temporary solutions',
           'non_existent': '1.000 | Non-existent: There is no solution',
           'default': '-'
         },
         'probability':{
           'prev_vuln': '100% previously with vulnerability',
           'easy_vuln': '75% Easy to have a vulnerability',
           'possible_vuln': '50% Possible vulnerability',
           'diffic_vuln': '25% Difficult to have a vulnerability',
           'default': '-'
         },
         'finding_type':{
           'hygiene': 'Hygiene',
           'vuln': 'Vulnerability',
           'default': '-'
         },
         'test_method':{
           'analysis': 'Analysis',
           'app': 'App',
           'binary': 'Binary',
           'code': 'Code',
           'infras': 'Infrastructure',
           'default': '-'
         },
         'access_vector':{
           'adjacent': '0.646 | Adjacent network: Exploitable from same network segment',
           'network': '1.000 | Network: Exploitable from Internet',
           'local': '0.395 | Local: Exploitable with local access to the target',
           'default': '-'
         },
         'criticity_header':{
           'high': ' High',
           'moderate': ' Moderate',
           'tolerable': ' Tolerable'
         },
         'treatment_header':{
           'default': '-',
           'asummed': 'Asummed',
           'working': 'Working on it',
           'remediated': 'Remediate'
         },
       },
       'registration':{
         'close_session': 'Close Session',
         'close_modal': 'Are you sure?',
         'yes': 'Yes',
         'no': 'No',
         'hello': 'Hello',
         'no_authorization': 'You do not have authorization for login yet. Please contact FLUID\'s staff to get access.'
       },
       'confirmmodal':{
         'title_cssv2': 'Update CSSv2',
         'title_description': 'Update Description',
         'title_finding': 'Delete Finding',
         'confirm': 'Are you sure?',
         'no': 'No',
         'yes': 'Yes'
       },
       'deletemodal':{
         'justification': 'Justification',
         'change_evidence': 'Change of evidence',
         'finding_changed': 'Finding has changed',
         'not_vulnerability': 'It is not a Vulnerability',
         'duplicated': 'It is duplicated'
       }
    };
    var traducciones = {
        'logout': {
            'message': 'Esta seguro de que desea salir?',
            'title':'Cerrar Sesión',
            'ok': 'Salir',
            'cancel': 'Cancelar'
        },
        'left_menu': {
            'first': 'Hallazgos',
            'second': 'Eventualidades',
            'third': 'Formularios'
        },
        'forms': {
            'progress': 'Avance',
            'findings': 'Hallazgos',
            'closure': 'Cierre',
            'events': 'Eventualidades'
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
                'search':{
                    'placeholder': 'Nombre del proyecto en FLUID',
                    'button': 'Ejecutar esta busqueda',
                }
            },
            'filter_labels':{
                'findings': 'Hallazgos',
                'cardinalities': 'Vulnerabilidades Abiertas',
                'criticity': 'Criticidad Total Encontrada',
                'closure': 'Vulnerabilidades remediadas'
            },
            'filter_buttons':{
                'advance': 'Avance',
                'documentation': 'Documentacion'
            },
            'table':{
                'headings':{
                    'age': 'Edad (Días)',
                    'action': 'Accion',
                    'timestamp': 'Fecha',
                    'type': 'Tipo',
                    'finding': 'Titulo',
                    'vulnerability': 'Descripcion',
                    'criticity': 'Severidad',
                    'cardinality': 'Vuln. Abiertas',
                    'state': 'Estado',
                    'exploit': 'Explotable',
                    'treatment': 'Tratamiento'

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
              'vulnerabilities': 'Vulnerabilidades Abiertas',
              'status': 'Estado',
              'report': 'Fecha Reporte',
              'project': 'Proyecto FLUID',
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
              'cardinality': 'Vulnerabilidades Abiertas',
              'vectors': 'Vectores de ataque',
              'threat': 'Amenaza',
              'recommendation': 'Recomendacion',
              'system': 'Sistemas Comprometidos',
              'records': 'Registros Comprometidos',
              'totalrecords': 'Total Registros Comprometidos',
              'weakness': 'Debilidad',
              'editable': 'Editar',
              'update': 'Actualizar',
              'treatment': 'Tratamiento',
              'treat_justification': 'Justificación del Tratamiento',
              'treat_manager': 'Responsable del Tratamiento',
              'edit_treatment': 'Editar',
              'update_treatment': 'Actualizar',
              'update_treatmodal': 'Actualizar Tratamiento',
              'remediated': 'Remediado',
              'remediated_finding': 'Hallazgo remediado'
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
              'editable': 'Editar',
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
              'editable': 'Editar',
              'detail': 'Detalle',
              'update':'Actualizar',
              'alert':'En desarrollo...',
              'animation_exploit':'Animación de explotación',
              'evidence_exploit':'Evidencia de explotación'
            },
            'tab_comments':{
              'comments_name':'Comentarios'
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
            'description3': ' sobre el proyecto',
            'project_title': 'Proyecto FLUID',
            'project_description': 'Descripción'
          },
          'eventualities':{
                 'title': 'Mis Eventualidades',
                 'description_1': 'Para ver el detalle de la eventualidad debes hacer',
                 'description_2': 'click',
                 'description_3': 'sobre la eventualidad',
                 'project_title': 'Proyecto FLUID',
                 'date': 'Fecha',
                 'type': 'Tipo',
                 'description': 'Detalle',
                 'close': 'CERRAR'
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
        'progress_mod':{
          'title': 'Reporte de Avance',
          'finding': 'Hallazgo'
        },
        'technical_report_mod':{
          'title': 'Informes Técnicos'
        },
        'executive_report_mod':{
          'title': 'Informes Ejecutivos'
        },
        'proj_alerts':{
          'search_title': 'Noticia!',
          'search_cont': 'Buscando Proyecto...',
          'attent_title': 'Cuidado!',
          'attent_cont': 'Busqueda vacia',
          'updated_title': 'Correcto!',
          'updated_cont': 'Actualizado ;)',
          'error_textsad': 'Hay un error :(',
          'error_text': 'Hay un error',
          'event_title': 'Consultando',
          'event_wait': 'Un momento por favor...',
          'event_select': 'Debes seleccionar una eventualidad',
          'event_required': 'El nombre es obligatorio',
          'event_internal': 'Error interno, cargando datos...',
          'event_formstack': 'No se tuvo acceso a Formstack...',
          'event_positiveint': 'La afectación debe ser un número positivo o cero',
          'event_updated': 'Eventualidad actualizada',
          'event_exist':'Este proyecto no tiene eventualidades o no existe',
          'no_finding':'No encontramos el hallazgo!',
          'error_severity':'La severidad debe ser un numero de 0 a 5',
          'wrong_severity':'Debes calcular correctamente la severidad',
          'not_found':'No pudimos encontrarlo!',
          'differ_comment':'Debes ingresar una nueva justificación del tratamiento',
          'empty_comment':'Debes ingresar una justificación del tratamiento!',
          'short_comment':'Debes ingresar una justificación de mínimo 50 caracteres y máximo 80 caracteres',
          'congratulation':'Felicidades',
          'updated_treat':'El tratamiento fue actualizado',
          'remediated_success':'El hallazgo fue marcado como remediado, la solicitud de revisión de la solución fue enviada'
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
            'f_proj': 'Proyecto FLUID',
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
            'f_proj': 'Proyecto FLUID',
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
         },
         'btn_group':{
           'watch': 'VER!',
           'edit': 'EDITAR!',
           'resume': 'RESUMEN!'
         }
       },
       'event_formstack':{
         'type':{
           'auth_attack': 'Autorización para ataque especial',
           'toe_differs': 'Alcance difiere a lo aprobado',
           'high_approval': 'Aprobación de alta disponibilidad',
           'incor_supplies': 'Insumos incorrectos o faltantes',
           'explic_suspend': 'Cliente suspende explicitamente',
           'approv_change': 'Cliente aprueba cambio de alcance',
           'cancel_proj': 'Cliente cancela el proyecto/hito',
           'det_attack': 'Cliente detecta ataque',
           'other': 'Otro',
           'inacc_ambient': 'Ambiente no accesible',
           'uns_ambient': 'Ambiente inestable',
           'unknown':'-'
         },
         'status':{
           'solve': 'Tratada',
           'unsolve': 'Pendiente',
           'unknown':'-'
         }
       },
       'finding_formstack':{
         'actor':{
           'any_internet': 'Cualquier persona en Internet',
           'any_costumer': 'Cualquier cliente de la organización',
           'some_costume': 'Solo algunos clientes de la organización',
           'any_access': 'Cualquier persona con acceso a la estación',
           'any_employee': 'Cualquier empleado de la organización',
           'some_employee': 'Solo algunos empleados',
           'one_employee': 'Solo un empleado',
           'default': '-'
         },
         'authentication':{
           'any_authen': '0.704 | Ninguna: No se requiere autenticación',
           'single_authen': '0.560 | Única: Único punto de autenticación',
           'multiple_authen': '0.450 | Multiple: Multiples puntos de autenticación',
           'default':'-'
         },
         'category':{
           'update_base': 'Actualizar y configurar las líneas base de seguridad de los componentes',
           'define_model': 'Definir el modelo de autorización considerando el principio de mínimo privilegio',
           'performance': 'Desempeño',
           'event': 'Eventualidad',
           'avoid_technical': 'Evitar exponer la información técnica de la aplicación, servidores y plataformas',
           'exclude_data': 'Excluir datos sensibles del código fuente y del registro de eventos',
           'strengt_authen': 'Fortalecer controles en autenticación y manejo de sesión',
           'strengt_process': 'Fortalecer controles en el procesamiento de archivos',
           'strengt_protect': 'Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas',
           'validate_input': 'Implementar controles para validar datos de entrada',
           'maintain': 'Mantenibilidad',
           'record_event': 'Registrar eventos para trazabilidad y auditoría',
           'secure_protoc': 'Utilizar protocolos de comunicación seguros',
           'validate_http': 'Validar la integridad de las transacciones en peticiones HTTP',
           'default':'-'
         },
         'complexity':{
           'high_complex': '0.350 | Alto: Se requieren condiciones especiales como acceso administrativo',
           'medium_complex': '0.610 | Medio: Se requieren algunas condiciones como acceso al sistema',
           'low_complex': '0.710 | Bajo: No se requiere ninguna condición especial',
           'default':'-'
         },
         'scenario':{
           'anon_inter': 'Anónimo desde Internet',
           'anon_intra': 'Anónimo desde Intranet',
           'infra_scan': 'Escaneo de Infraestructura',
           'unauth_extra': 'Extranet usuario no autorizado',
           'auth_inter': 'Internet usuario autorizado',
           'unauth_inter': 'Internet usuario no autorizado',
           'auth_intra': 'Intranet usuario autorizado',
           'unauth_inter': 'Intranet usuario no autorizado',
           'default': '-'
         },
         'status':{
           'open': 'Abierto',
           'close': 'Cerrado',
           'part_close': 'Parcialmente cerrado',
           'default': '-'
         },
         'exploitability':{
           'improbable': '0.850 | Improbable: No existe un exploit',
           'conceptual': '0.900 | Conceptual: Existen pruebas de laboratorio',
           'functional': '0.950 | Funcional: Existe exploit',
           'high': '1.000 | Alta: No se requiere exploit o se puede automatizar',
           'default': '-'
         },
         'exploitable':{
           'yes': 'Si',
           'no': 'No',
           'default': '-'
         },
         'confidenciality':{
           'none': '0 | Ninguno: No se presenta ningún impacto',
           'partial': '0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella',
           'complete': '0.660 | Completo: Se controla toda la información relacionada con el objetivo',
           'default': '-'
         },
         'availability':{
           'none': '0 | Ninguno: No se presenta ningún impacto',
           'partial': '0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo',
           'complete': '0.660 | Completo: Hay una caída total del objetivo',
           'default': '-'
         },
         'integrity':{
           'none': '0 | Ninguno: No se presenta ningún impacto',
           'partial': '0.275 | Parcial: Es posible modificar cierta información del objetivo',
           'complete': '0.660 | Completo: Es posible modificar toda la información del objetivo',
           'default': '-'
         },
         'confidence':{
           'not_confirm': '0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad',
           'not_corrob': '0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales',
           'confirmed': '1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante',
           'default': '-'
         },
         'resolution':{
           'palliative': '0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante',
           'official': '0.870 | Oficial: Existe un parche disponible por el fabricante',
           'temporal': '0.900 | Temporal: Existen soluciones temporales',
           'non_existent': '1.000 | Inexistente: No existe solución',
           'default': '-'
         },
         'probability':{
           'prev_vuln': '100% Vulnerado Anteriormente',
           'easy_vuln': '75% Fácil de vulnerar',
           'possible_vuln': '50% Posible de vulnerar',
           'diffic_vuln': '25% Difícil de vulnerar',
           'default': '-'
         },
         'finding_type':{
           'hygiene': 'Higiene',
           'vuln': 'Vulnerabilidad',
           'default': '-'
         },
         'test_method':{
           'analysis': 'Análisis',
           'app': 'Aplicación',
           'binary': 'Binario',
           'code': 'Código',
           'infras': 'Infraestructura',
           'default': '-'
         },
         'access_vector':{
           'adjacent': '0.646 | Red adyacente: Explotable desde el mismo segmento de red',
           'network': '1.000 | Red: Explotable desde Internet',
           'local': '0.395 | Local: Explotable con acceso local al objetivo',
           'default': '-'
         },
         'criticity_header':{
           'high': ' Alto',
           'moderate': ' Moderado',
           'tolerable': ' Tolerable'
         },
         'treatment_header':{
           'default': '-',
           'asummed': 'Asumido',
           'working': 'Pendiente',
           'remediated': 'Remediar'
         },
       },
       'registration':{
         'close_session': 'Cerrar Sesión',
         'close_modal': 'Esta seguro de que desea salir?',
         'yes': 'Si',
         'no': 'No',
         'hello': 'Hola',
         'no_authorization': 'No tienes autorización aún para ingresar. Comunícate con un representante de FLUID para obtener acceso.'
       },
       'confirmmodal':{
         'title_cssv2': 'Actualizar CSSv2',
         'title_description': 'Actualizar Descripción',
         'title_finding': 'Eliminar Hallazgo',
         'confirm': '¿Realizar esta acción?',
         'no': 'Cancelar',
         'yes': 'Aceptar'
       },
       'deletemodal':{
         'justification': 'Justificación',
         'change_evidence': 'Cambio de Evidencia',
         'finding_changed': 'Por Modificación del Hallazgo',
         'not_vulnerability': 'No es una Vulnerabilidad',
         'duplicated': 'Está Duplicado'
       }
    };
    if(localStorage['lang'] === undefined){
        localStorage['lang'] = 'en';
    }
    $translateProvider
        .translations('en', translations)
        .translations('es', traducciones)
        .preferredLanguage(localStorage['lang']);

}]);
