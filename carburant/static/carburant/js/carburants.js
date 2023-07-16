$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-carburant .modal-content").html("");
        //$("#modal-carburant").modal("show");
      },
      success: function (data) {
        $("#modal-carburant .modal-content").html(data.html_form);
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
          $("#carburant-table tbody").html(data.html_carburant_list);
          $("#modal-carburant").modal("hide");
        }
        else {
          $("#modal-carburant .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create carburant
  $(".js-create-carburant").on('click', loadForm);
  $("#modal-carburant").on("submit", ".js-carburant-create-form", saveForm);

  // Update carburant
  $("#carburant-table").on("click", ".js-update-carburant", loadForm);
  $("#modal-carburant").on("submit", ".js-carburant-update-form", saveForm);

  // Delete carburant
  $("#carburant-table").on("click", ".js-delete-carburant", loadForm);
  $("#modal-carburant").on("submit", ".js-carburant-delete-form", saveForm);
});

