
$(function () {
    //https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html
    var loadForm = function(){
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function(){
                        $("#modal-section").modal("show");
                      },
          success: function(data){
                      $("#modal-section .modal-content").html(data.html_form);
                    },
      });
    };

    var toggleUser = function(){
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          success: function(data){
                      $('#user_list').DataTable().ajax.reload();
                    },
      });
    };

    var saveForm = function() {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function(data){
          if (data.form_is_valid) {
              $("#modal-section").modal("hide");
              $('#election_list').DataTable().ajax.reload();
              $('#user_list').DataTable().ajax.reload();

          }
          else{
            $("#modal-section .modal-content").html(data.html_form);
          }
        }
      });
    return false;
    };

    /* Binding */

    //create User
    $('.js-create-user').click(loadForm);
    $("#modal-section").on("submit", ".js-user-create-form", saveForm);

    //create Election
    $('.js-create-election').click(loadForm);
    $("#modal-section").on("submit", ".js-election-create-form", saveForm);

    //Update User
    $('#user_list').on("click",".js-update-user",loadForm);
    $('#modal-section').on("submit",".js-user-update-form", saveForm);

    //reset password
    $('#user_list').on("click",".js-reset-password-user",loadForm);
    $('#modal-section').on("submit",".js-user-reset-password-form", saveForm);

    //toggle User
    $('#user_list').on("click",".js-toggle-user",toggleUser);
});
