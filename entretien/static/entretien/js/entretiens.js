$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-entretien .modal-content").html("");
        //$("#modal-entretien").modal("show");
      },
      success: function (data) {
        $("#modal-entretien .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#entretien-table tbody").html(data.html_entretien_list);
          $("#modal-entretien").modal("hide");
        }
        else {
          $("#modal-entretien .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create entretien
  $(".js-create-entretien").on('click', loadForm);
  $("#modal-entretien").on("submit", ".js-entretien-create-form", saveForm);

  // Update entretien
  $("#entretien-table").on("click", ".js-update-entretien", loadForm);
  $("#modal-entretien").on("submit", ".js-entretien-update-form", saveForm);

  // Delete entretien
  $("#entretien-table").on("click", ".js-delete-entretien", loadForm);
  $("#modal-entretien").on("submit", ".js-entretien-delete-form", saveForm);
});

