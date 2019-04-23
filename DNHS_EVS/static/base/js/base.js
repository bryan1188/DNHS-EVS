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

  var reviewVoteForm = function(){
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function(){
                        $("#modal-review-vote-auth").modal("show");
                      },
          success: function(data){

                      $("#modal-review-vote-auth .modal-content").html(data.html_form)
                    },
      });
  };

  var reviewVoteFormSubmit = function(){
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function(data){
        if (data.form_is_valid) {
            // $("#modal-review-vote-auth").modal("hide");
            // $("#modal-review-vote").modal("show");
            $("#modal-review-vote-auth .modal-content").html(data.html_form_votes)
        }
        else{
          $("#modal-review-vote-auth .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  $('.js-login').click(loadForm);
  $('.js-logout').click(logout);
  $('.js-review-vote').click(reviewVoteForm);
  $("#modal-login").on("submit", ".js-login-form", submitForm);
  $("#modal-review-vote-auth").on("submit", ".js-review-vote-auth-form", reviewVoteFormSubmit);
});
