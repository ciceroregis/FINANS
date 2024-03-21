$(document).ready(function () {
    var $cpf = $("#CPF");
    $cpf.mask('000.000.000-00', { reverse: true });

    var $phone_number = $("#phone_number");
    $phone_number.mask('(00)0000-00000', { reverse: false });

    var $landline = $("#landline");
    $landline.mask('(00)0000-0000', { reverse: false });

    var $birth_date = $("#birth_date");
    $birth_date.mask('00/00/0000', { reverse: false });

  // var $zip_code = $("#CEP");
  // $zip_code.mask('99.999-999', { reverse: true });
});
