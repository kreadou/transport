$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-client .modal-content").html("");
        //$("#modal-client").modal("show");
      },
      success: function (data) {
        $("#modal-client .modal-content").html(data.html_form);
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
          $("#client-table tbody").html(data.html_client_list);
          $("#modal-client").modal("hide");
        }
        else {
          $("#modal-client .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  /* Binding */
  // Create client
  $(".js-create-client").on('click', loadForm);
  $("#modal-client").on("submit", ".js-client-create-form", saveForm);

  // Update client
  $("#client-table").on("click", ".js-update-client", loadForm);
  $("#modal-client").on("submit", ".js-client-update-form", saveForm);

  // Delete client
  $("#client-table").on("click", ".js-delete-client", loadForm);
  $("#modal-client").on("submit", ".js-client-delete-form", saveForm);
});

