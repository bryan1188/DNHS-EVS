$(function () {

    $(".js-create-user").click(function () {
        $.ajax({
            // url:  '{% url "registration:create_user_ajax" %}',
            url: '/registration/ajax/user/create/',
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                          $("#modal-user").modal("show");
                          },
            success: function(data){
                        $("#modal-user .modal-content").html(data.html_form)
                      },
        });
    });
});

$("#modal-user").on("submit", ".js-user-create-form", function () {
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
  });
