box = $("#m_box")[0] // box button to be clicked on
$("#dialog").dialog({autoOpen: false});
function addCoin() {
	console.log("clicked");
        fetch("/addcoin/" + getCookie("Username"));
        box.remove();
	$("#dialog").dialog('open');
}
box.addEventListener("click", addCoin);
