// Toggle Function
//로그인<->회원가입 전환 토글
$(".toggle").click(function () {
  // Switches the Icon
  $(this).children("i").toggleClass("fa-pencil");
  if ($(this).text() == "회원가입") $(this).text("로그인");
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

let idlap = 0
let nicklap = 0

//회원가입 버튼 클릭
function join() {
  let id = $('#userid').val()
  let pw = $('#pw').val()
  let pw_check = $('#pw_check').val()
  let nick = $('#nickname').val()

  $.ajax({
    type: "POST",
    url: "/api/join",
    data: { id_give: id, pw_give: pw, pwc_give: pw_check, nick_give: nick },
    success: function (response) {
      alert(response['msg'])

      if (response['state'] == 1) window.location.reload()
    }
  });
}

//아이디 중복체크
function checkID() {
  let id = $('#userid').val()

  $.ajax({
    type: "POST",
    url: "/api/idcheck",
    data: { id_give: id },
    success: function (response) {
      alert(response['msg'])
    }
  });
}

//닉네임 중복체크
function checkNick() {
  let nick = $('#nickname').val()

  $.ajax({
    type: "POST",
    url: "/api/nickcheck",
    data: { nick_give: nick },
    success: function (response) {
      alert(response['msg'])
    }
  });
}

function login() {
  let id = $('#idInput').val()
  let pw = $('#pwInput').val()

  $.ajax({
    type: "POST",
    url: "/api/login",
    data: { id_give: id, pw_give: pw },
    success: function (response) {
      if (response['state'] == 0) {
        alert(response['msg'])
        window.location.reload()
      }
      else {
        $.cookie('mytoken', response['token'])
        location.href = '/'
      }
    }
  });
}