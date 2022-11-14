// Toggle Function
$(".toggle").click(function () {
  // Switches the Icon
  $(this).children("i").toggleClass("fa-pencil");
  if($(this).text() == "회원가입") $(this).text("로그인");
  else $(this).text("회원가입");

  // Switches the forms
  $(".form").animate(
    {
      height: "toggle",
      "padding-top": "toggle",
      "padding-bottom": "toggle",
      opacity: "toggle"
    },
    "slow"
  );
});