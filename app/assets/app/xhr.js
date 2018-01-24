'use strict'
/* Angular JQuery Sync */
ajaxConfig();
var $xhr = new (class xhr {
    request($method, $q, $url, $data, text){
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
                       Rollbar.error(text);
                       $.gritter.add({ title: 'Oops!', text: text ,
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
    get($q, $url, $data, text = {}){ return this.request("get", $q, $url, $data, text) };
    post($q, $url, $data, text = {}){ return this.request("post", $q, $url, $data, text) };
});
//Overriding ajax
$("#full_loader").hide();
$( document ).ajaxStart(function() { $("#full_loader").show(); });
$( document ).ajaxStop(function() { $("#full_loader").hide(); });
$( document ).ajaxError(function() { $("#full_loader").hide(); });
