$(document).ready( function () {
  var form = $('#id_school_year').closest("form");

  var table = $('#uploaded_students').DataTable( {
    "processing": true,
    "ajax": {
        "processing": true,
        "url": "{% url 'registration:populate_table_uploaded_students_2_ajax' %}",
        "data": function( d ) {
                d.school_year = $('#id_school_year').val();
                d.grade_level = $('#id_grade_level').val();
                d.section = $('#id_section').val();
              },
        "dataSrc": ""
    },
    'columns': [
      {"data": "fields.lrn"},
      {"data": "fields.last_name"},
      {"data": "fields.first_name"},
      {"data": "fields.middle_name"},
      {"data": "fields.sex"},
      {"data": "fields.birth_date"},
      {"data": "fields.age"},
      {"data": "fields.father_name"},
      {"data": "fields.mother_name"},
    ]
  });
} );

$(document).ready( function () {
  var form = $('#id_school_year').closest("form");

  var table = $('#uploaded_students').DataTable( {
    "processing": true,
    "ajax": {
        "processing": true,
        "serverSide": true,
        "url": "{% url 'registration:populate_table_uploaded_students_data-table-view_ajax' %}",
        "data": function( d ) {
                d.school_year = $('#id_school_year').val();
                d.grade_level = $('#id_grade_level').val();
                d.section = $('#id_section').val();
              },
        "dataSrc": "",
        'columns': [
          {"data": "fields.lrn"},
          {"data": "fields.last_name"},
          {"data": "fields.first_name"},
          {"data": "fields.middle_name"},
          {"data": "fields.sex"},
          {"data": "fields.birth_date"},
          {"data": "fields.age"},
          {"data": "fields.father_name"},
          {"data": "fields.mother_name"},
        ]
    }
  });
} );


function clear_section(){
  $('#id_section')
    .find('option')
    .remove()
    .end()
    .append('<option value="">---------</option>')
}

function clear_grade_level(){
    $('#id_grade_level')
      .find('option')
      .remove()
      .end()
      .append('<option value="">---------</option>')
  }


$('#id_school_year').change( function(){
  var form = $(this).closest("form");
  clear_grade_level();
  clear_section();
  $.ajax({  //populate other drop down
    url: '{% url "registration:get_filter_options_for_level_ajax" %}',
    data: form.serialize(),
    success: function(data){
      $('#id_grade_level').html(data);
    }
    });

    $('#uploaded_students').DataTable().ajax.reload();
  });

$('#id_grade_level').change( function(){
  var form = $(this).closest("form");
  $.ajax({  //populate other drop down
    url: '{% url "registration:get_filter_options_for_section_ajax" %}',
    data: form.serialize(),
    success: function(data){
      $('#id_section').html(data);
    }
    });

  clear_section();
  $('#uploaded_students').DataTable().ajax.reload();
});

$('#id_section').change( function(){
  $('#uploaded_students').DataTable().ajax.reload();
});
