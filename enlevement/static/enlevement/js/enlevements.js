$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-enlevement .modal-content").html("");
        //$("#modal-enlevement").modal("show");
      },
      success: function (data) {
        $("#modal-enlevement .modal-content").html(data.html_form);
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
          $("#enlevement-table tbody").html(data.html_enlevement_list);
          $("#modal-enlevement").modal("hide");
        }
        else {
          $("#modal-enlevement .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create enlevement
  $(".js-create-enlevement").on('click', loadForm);
  $("#modal-enlevement").on("submit", ".js-enlevement-create-form", saveForm);

  // Update enlevement
  $("#enlevement-table").on("click", ".js-update-enlevement", loadForm);
  $("#modal-enlevement").on("submit", ".js-enlevement-update-form", saveForm);

  // Delete enlevement
  $("#enlevement-table").on("click", ".js-delete-enlevement", loadForm);
  $("#modal-enlevement").on("submit", ".js-enlevement-delete-form", saveForm);
});

