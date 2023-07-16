$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-reparation .modal-content").html("");
        //$("#modal-reparation").modal("show");
      },
      success: function (data) {
        $("#modal-reparation .modal-content").html(data.html_form);
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
          $("#reparation-table tbody").html(data.html_reparation_list);
          $("#modal-reparation").modal("hide");
        }
        else {
          $("#modal-reparation .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create reparation
  $(".js-create-reparation").on('click', loadForm);
  $("#modal-reparation").on("submit", ".js-reparation-create-form", saveForm);

  // Update reparation
  $("#reparation-table").on("click", ".js-update-reparation", loadForm);
  $("#modal-reparation").on("submit", ".js-reparation-update-form", saveForm);

  // Delete reparation
  $("#reparation-table").on("click", ".js-delete-reparation", loadForm);
  $("#modal-reparation").on("submit", ".js-reparation-delete-form", saveForm);
});

