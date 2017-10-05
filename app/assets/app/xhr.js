'use strict'
/* Angular JQuery Sync */
var $xhr = new (class xhr {
    request($method, $q, $url, $data){
        if(!$q) throw "Undefined Promise";
        if(!$url) throw "Undefined URL";
        var deferred = $q.defer();
        try { 
            $.ajax({ 
                url: $url, type: $method, data: $data,
                success: function (response) { deferred.resolve(response); },
                error: function (XMLHttpRequest, textStatus, errorThrown) { 
                   if(XMLHttpRequest.status == 401){
                       location = BASE.url + "index";
                   }else{
                       $.gritter.add({ title: 'Oops!', text: 'Hay un error',
                            class_name: 'color warning', sticky: false,
                       });
                   }
                }
            });
        } catch (e) { 
            deferred.resolve(e);
        }
        return deferred.promise;
    }
    get($q, $url, $data = {}){ return this.request("get", $q, $url, $data) };
    post($q, $url, $data = {}){ return this.request("post", $q, $url, $data) };
});
//Overriding ajax
$("#full_loader").hide();
$( document ).ajaxStart(function() { $("#full_loader").show(); });
$( document ).ajaxStop(function() { $("#full_loader").hide(); });
$( document ).ajaxError(function() { $("#full_loader").hide(); });