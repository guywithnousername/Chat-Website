function htmlentities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
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
    let username= htmlentities(getCookie("Username"))
    var forms = $(".userform")
    var text = $(".signedin")
    if (username!=""){
        for (const x of forms) {
            x.remove()
        }
        text[1].innerHTML = htmlentities(getCookie("Username"))
        text[0].innerHTML = "Log out"
    } else {
        forms[0].innerHTML = "Register"
        forms[1].innerHTML = "Login"
        for (const x of text) {
          x.remove()
        }
    }
}
checkUsername()
