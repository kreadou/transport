$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-devis .modal-content").html("");
        //$("#modal-devis").modal("show");
      },
      success: function (data) {
        $("#modal-devis .modal-content").html(data.html_form);
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
          $("#devis-table tbody").html(data.html_devis_list);
          $("#modal-devis").modal("hide");
        }
        else {
          $("#modal-devis .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create devis
  $(".js-create-devis").on('click', loadForm);
  $("#modal-devis").on("submit", ".js-devis-create-form", saveForm);

  // Update devis
  $("#devis-table").on("click", ".js-update-devis", loadForm);
  $("#modal-devis").on("submit", ".js-devis-update-form", saveForm);

  // Delete devis
  $("#devis-table").on("click", ".js-delete-devis", loadForm);
  $("#modal-devis").on("submit", ".js-devis-delete-form", saveForm);
});

