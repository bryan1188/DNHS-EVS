$(function() {

    var variable_container = $('#variable_container');

    $(window).on('load',function(){
      // show modal to authenticate
        $.ajax({
            url: variable_container.attr("data-url-authenticate_voter_ajax"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                          $("#modal-section").modal("show");
                        },
            success: function(data){
                        $("#modal-section .modal-content").html(data.html_form);
                      },
        });
    });

    function show_confirmation(voter_id){
      $.ajax({
        url: "/election/ajax/voter/confirmation/" + voter_id,
        type: 'get',
        dataType: 'json',
        beforeSend: function(){
                      $("#modal-vote-confirmation").modal("show");
                    },
        success: function(data){
           $("#modal-vote-confirmation .modal-content").html(data.html_form);
           // alert("test");
        }
      });

    }

    $(function () {
      var authenticateVoter = function(){
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function(data){
            if (data.form_is_valid){
              // convert data.voter string to javascript json format
              var voter = jQuery.parseJSON(data.voter)[0];
              $("#modal-section").modal("hide");

              //show confirmation page
              show_confirmation(voter.pk);
            }
            else {
              $("#modal-section .modal-content").html(data.html_form);
            }
          }
        });

        //return false to not display the json data value.
        //data should be processed accordingly through ajax's call 'success'
        return false;
      };

      var userConfirmed = function(){
        var form = $(this);

        $.ajax({
          url: form.attr("action"),
          type: form.attr("method"),
          dataType: 'json',
          beforeSend: function(){
                        $("#modal-vote-confirmation").modal("hide");
                        $("#modal-show-ballot").modal("show");
                      },
          success: function(data){
             $("#modal-show-ballot .modal-content").html(data.html_form);
             // alert("test");
          }
        });

        //return false to not display the json data value.
        //data should be processed accordingly through ajax's call 'success'
        return false;
      }

      //bind
      $("#modal-section").on("submit", ".js-authenticate-voter-form", authenticateVoter);

      $('#modal-vote-confirmation').on('click','.js-not-me', function(){
          //refresh current page to show again modal-section
          //so voter will enter again the token
          location.reload();
      });

      $('#modal-vote-confirmation').on("click",".js-this-is-me", userConfirmed);

    });

});
