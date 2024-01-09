const signUpbtn = document.getElementById("signUpBtn");
const signInbtn = document.getElementById("signInBtn");
const registerBtn = document.getElementById("registerBtn");
const signInForm = document.getElementById("signInForm");
const signUpForm = document.getElementById("signUpForm");

function switchSignInUp(signin, signup) {
  signin.style.display = "none";
  signup.style.display = "block";
}

$("#registerBtn").click(function () {
  switchSignInUp(signInForm, signUpForm);
});

$("#signUpBtn").click(function () {
  console.log($("#signUpId").val());
  register();
});

function register() {
  $.ajax({
    type: "POST",
    url: "api/register",
    data: {
      id_give: $("#signUpId").val(), // id
      pw_give: $("#signUpPw").val(), // pw
      name_give: $("#signUpName").val(), // name
      email_give: $("#signUpMail").val(), // email
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("회원가입이 완료되었습니다.");
      } else {
        alert("회원가입에 실패하였습니다");
      }
    },
  });
}

function login() {
  $ajax({
    type: "POST",
    url: "/api/login",
    data: { id_give: $("#userID").val(), pw_give: $("userPassword").val() },
    success: function (response) {
      if (response["result"] == "success") {
        $.cookie("mytoken", response["token"]);

        alert("로그인 완료!");
      } else {
        alert(response["msg"]);
      }
    },
  });
}
