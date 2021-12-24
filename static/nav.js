function setCookie(name,val,days) {
    const d = new Date();
    d.setTime(d.getTime() + (days*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = name + "=" + val + ";" + expires + ";path=/";
}
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}
function checkUsername() {
    let username= getCookie("Username")
    var forms = document.getElementsByClassName("userform")
    var text = document.getElementsByClassName("signedin")
    if (username!=""){
        for (const x of forms) {
            x.innerHTML = ""
        }
        text[1].innerHTML = getCookie("Username")
        text[0].innerHTML = "Log out"
    } else {
        forms[0].innerHTML = "Register"
        forms[1].innerHTML = "Login"
        for (const x of text) {
          x.innerHTML = ""
        }
    }
}
checkUsername()