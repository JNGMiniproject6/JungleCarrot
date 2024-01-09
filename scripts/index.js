const signUpbtn = document.getElementById("signUpBtn");
const signInbtn = document.getElementById("signInBtn");
const signInForm = document.getElementById("signInForm");
const signUpForm = document.getElementById("signUpForm");

function switchSignInUp(signin, signup) {
  signin.style.display = "none";
  signup.style.display = "block";
}

signUpbtn.addEventListener("click", () => {
  switchSignInUp(signInForm, signUpForm);
});
