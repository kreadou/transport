$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-vehicule .modal-content").html("");
        //$("#modal-vehicule").modal("show");
      },
      success: function (data) {
        $("#modal-vehicule .modal-content").html(data.html_form);
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
          $("#vehicule-table tbody").html(data.html_vehicule_list);
          $("#modal-vehicule").modal("hide");
        }
        else {
          $("#modal-vehicule .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create vehicule
  $(".js-create-vehicule").on('click', loadForm);
  $("#modal-vehicule").on("submit", ".js-vehicule-create-form", saveForm);

  // Update vehicule
  $("#vehicule-table").on("click", ".js-update-vehicule", loadForm);
  $("#modal-vehicule").on("submit", ".js-vehicule-update-form", saveForm);

  // Delete vehicule
  $("#vehicule-table").on("click", ".js-delete-vehicule", loadForm);
  $("#modal-vehicule").on("submit", ".js-vehicule-delete-form", saveForm);
});

