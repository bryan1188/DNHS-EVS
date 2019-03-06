

$(function () {
    //https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html
    var loadForm = function(){
      var btn = $(this);
      $.ajax({
          // url:  '{% url "registration:create_user_ajax" %}',
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function(){
                        $("#modal-user").modal("show");
                      },
          success: function(data){
                      $("#modal-user .modal-content").html(data.html_form)
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
              $("#modal-user").modal("hide");
              $('#user_list').DataTable().ajax.reload();
          }
          else{
            $("#modal-user .modal-content").html(data.html_form);
          }
        }
      });
    return false;
    };

    /* Binding */

    //create User
    $('.js-create-user').click(loadForm);
    $("#modal-user").on("submit", ".js-user-create-form", saveForm);

    //Update User
    $('#user_list').on("click",".js-update-user",loadForm);
    $('#modal-user').on("submit",".js-user-update-form", saveForm);
});
