box = $("#m_box")[0] // box button to be clicked on
$("#dialog").dialog({autoOpen: false});
function addCoin() {
	console.log("clicked");
        fetch("/addcoin/" + getCookie("Username"));
	$("#m_box").effect('shake',{},2000);
	$("#m_box").hide('explode',{},1000);
        box.remove();
	$("#dialog").dialog('open');
}
box.addEventListener("click", addCoin);
