$(function() {

  var loadForm = function(){
    var btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function(){
                      $("#modal-login").modal("show");
                    },
        success: function(data){

                    $("#modal-login .modal-content").html(data.html_form)
                  },
    });
  };

  var logout = function(){
    var btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        success: function(data){
                  console.log("logout Success");
                  window.location.replace(btn.attr("redirect-url"));
                  },
    });
  };

  var submitForm = function() {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function(data){
        if (data.form_is_valid) {
            $("#modal-login").modal("hide");
            location.reload(); //refresh current page
        }
        else{
          $("#modal-login .modal-content").html(data.html_form);
        }
      }
    });
  return false;
  };


  $('.js-login').click(loadForm);
  $('.js-logout').click(logout);
  $("#modal-login").on("submit", ".js-login-form", submitForm);
});
