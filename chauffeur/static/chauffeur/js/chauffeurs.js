$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-chauffeur .modal-content").html("");
        //$("#modal-chauffeur").modal("show");
      },
      success: function (data) {
        $("#modal-chauffeur .modal-content").html(data.html_form);
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
          $("#chauffeur-table tbody").html(data.html_chauffeur_list);
          $("#modal-chauffeur").modal("hide");
        }
        else {
          $("#modal-chauffeur .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create chauffeur
  $(".js-create-chauffeur").on('click', loadForm);
  $("#modal-chauffeur").on("submit", ".js-chauffeur-create-form", saveForm);

  // Update chauffeur
  $("#chauffeur-table").on("click", ".js-update-chauffeur", loadForm);
  $("#modal-chauffeur").on("submit", ".js-chauffeur-update-form", saveForm);

  // Delete chauffeur
  $("#chauffeur-table").on("click", ".js-delete-chauffeur", loadForm);
  $("#modal-chauffeur").on("submit", ".js-chauffeur-delete-form", saveForm);
});

