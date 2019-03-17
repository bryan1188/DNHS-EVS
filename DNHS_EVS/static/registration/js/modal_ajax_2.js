
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

    var toggleObject = function(){
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          success: function(data){
                      $('#user_list').DataTable().ajax.reload();
                      $('#position_list').DataTable().ajax.reload();
                      $('#election_list').DataTable().ajax.reload();
                      $('#party_list').DataTable().ajax.reload();
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
              $('#position_list').DataTable().ajax.reload();
              $('#party_list').DataTable().ajax.reload();
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

    //create Position
    $('.js-create-position').click(loadForm);
    $("#modal-section").on("submit", ".js-position-create-form", saveForm);

    //create Party
    $('.js-create-party').click(loadForm);
    $("#modal-section").on("submit", ".js-party-create-form", saveForm);

    //create Candidate
    $('.js-create-candidate').click(loadForm);
    $("#modal-section").on("submit", ".js-candidate-create-form", saveForm);

    //Update User
    $('#user_list').on("click",".js-update-user",loadForm);
    $('#modal-section').on("submit",".js-user-update-form", saveForm);

    //Update Election
    $('#election_list').on("click",".js-update-election",loadForm);
    $('#modal-section').on("submit",".js-election-update-form", saveForm);

    //Update Position
    $('#position_list').on("click",".js-update-position",loadForm);
    $('#modal-section').on("submit",".js-position-update-form", saveForm);

    //Update Party
    $('#party_list').on("click",".js-update-party",loadForm);
    $('#modal-section').on("submit",".js-party-update-form", saveForm);

    //reset password
    $('#user_list').on("click",".js-reset-password-user",loadForm);
    $('#modal-section').on("submit",".js-user-reset-password-form", saveForm);

    //toggle User
    $('#user_list').on("click",".js-toggle-user",toggleObject);

    //toggle Position
    $('#position_list').on("click",".js-toggle-position",toggleObject);

    //toggle Election
    $('#election_list').on("click",".js-toggle-election",toggleObject);

    //toggle Party
    $('#party_list').on("click",".js-toggle-party",toggleObject);

    //show more details of position
    $('#position_list').on("click",".js-show-more-details-position",loadForm);

    //show more details of election
    $('#election_list').on("click",".js-show-more-details-election",loadForm);

    //show more details of election
    $('#party_list').on("click",".js-show-more-details-party",loadForm);

    //tooltip
    $('[data-toggle="tooltip"]').tooltip();
    $('#position_lis').tooltip({selector: '[data-toggle="tooltip"]'});
});
