// Toggle Function
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

function join() {
  if (document.getElementById('idlap').innerText != 10) {
    alert('아이디 중복체크를 진행해주세요.')
  }
  else if (document.getElementById('nicklap').innerText != 10) {
    alert('닉네임 중복체크를 진행해주세요.')
  }
  else {
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
}

function checkID() {
  let id = $('#userid').val()

  $.ajax({
    type: "POST",
    url: "/api/idcheck",
    data: { id_give: id },
    success: function (response) {
      alert(response['msg'])
      if (response['state'] == 1) {
        $('#idlap').text(10)
      }
    }
  });
}

function checkNick() {
  let nick = $('#nickname').val()

  $.ajax({
    type: "POST",
    url: "/api/nickcheck",
    data: { nick_give: nick },
    success: function (response) {
      alert(response['msg'])
      if (response['state'] == 1) {
        $('#nicklap').text(10)
      }
    }
  });
}

$( document ).ready( function() {
  $( '#userid' ).change( function() {
    if(document.getElementById('idlap').innerText == 10)$('#idlap').text(0)
  } );
  $( '#nickname' ).change( function() {
    if(document.getElementById('nicklap').innerText == 10)$('#nicklap').text(0)
  } );
} );