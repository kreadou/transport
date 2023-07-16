$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-commande .modal-content").html("");
        //$("#modal-commande").modal("show");
      },
      success: function (data) {
        $("#modal-commande .modal-content").html(data.html_form);
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
          $("#commande-table tbody").html(data.html_commande_list);
          $("#modal-commande").modal("hide");
        }
        else {
          $("#modal-commande .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create commande
  $(".js-create-commande").on('click', loadForm);
  $("#modal-commande").on("submit", ".js-commande-create-form", saveForm);

  // Update commande
  $("#commande-table").on("click", ".js-update-commande", loadForm);
  $("#modal-commande").on("submit", ".js-commande-update-form", saveForm);

  // Delete commande
  $("#commande-table").on("click", ".js-delete-commande", loadForm);
  $("#modal-commande").on("submit", ".js-commande-delete-form", saveForm);
});

