function sentenceCase (str) { //convert string to Title. Upper case first letter of the word
    if ((str===null) || (str===''))
         return false;
    else
     str = str.toString();

   return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

$(function (){ //link my table,uploaded_students, to datable.js

  //add function to Load button. This will populate the First Name and Last Name
  $('.table tbody').on('click','.my-btn',function(){
    var currow = $(this).closest('tr');
    $('#id_first_name').val(sentenceCase(currow.find('td:eq(1)').text()));
    $('#id_last_name').val(sentenceCase(currow.find('td:eq(2)').text()));
    $('input[name="student_lrn"]').val(currow.find('td:eq(0)').text().trim());
  });
});

$(function () { // script to switch the two checkboxed if the other is checked
    var fade_time = 500;

    $('#id_for_student_0').change(function() {
        if(this.checked) {
          $('#id_for_student_1').prop("checked", false);
          // $('#uploaded_students_wrapper').show();
          $('#uploaded_students_wrapper').fadeIn(fade_time);
          $(':button').prop('disabled', false);
        }
        else if($('#id_for_student_1').prop("checked") == false){
            // $('#uploaded_students_wrapper').hide();
            $('#uploaded_students_wrapper').fadeOut(fade_time);
            $(':button').prop('disabled', true);
        }

  });

  $('#id_for_student_1').change(function() {
      if(this.checked) {
        $('#id_for_student_0').prop("checked", false);
        // $('#uploaded_students_wrapper').show();
        $('#uploaded_students_wrapper').fadeIn(fade_time);
         $(':button').prop('disabled', false);
      }
      else if($('#id_for_student_0').prop("checked") == false){
          // $('#uploaded_students_wrapper').hide();
          $('#uploaded_students_wrapper').fadeOut(fade_time);
          $(':button').prop('disabled', true);
      }
    });
}
);
