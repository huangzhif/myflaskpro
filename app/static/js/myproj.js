function run_waitMe(el, num, effect){
		text = 'Please wait...';
		fontSize = '';
		switch (num) {
			case 1:
			maxSize = '';
			textPos = 'vertical';
			break;
			case 2:
			text = '';
			maxSize = 30;
			textPos = 'vertical';
			break;
			case 3:
			maxSize = 30;
			textPos = 'horizontal';
			fontSize = '18px';
			break;
		}
		el.waitMe({
			effect: effect,
			text: text,
			bg: 'rgba(255,255,255,0.7)',
			color: '#000',
			maxSize: maxSize,
			waitTime: -1,
			source: 'img.svg',
			textPos: textPos,
			fontSize: fontSize,
			onClose: function(el) {}
		});
	}


function selectGame(type) {
	$("#id_channel").html("");
	$("#id_zone").html("");
	$("#id_zone").selectpicker("refresh");
	$("#id_version").html("");
	$("#publishlog").val("");

	var gameid=$("#id_game").val();
	if (gameid==""){
		return false;
	}

	$.getJSON("/game/get_gameinfo/?type=" + type + "&gameid=" + gameid,function (data) {
		var channelstring = "<option value=''></option>";
		var versionstring = "<option value=''></option>";

		$.each(data["channels_list"],function (i,item) {
			channelstring += "<option value=\"" + item[0] + "\">" + item[1] + "</option>";
		});

		$.each(data["zips_ver"],function (i,item) {
			versionstring += "<option value=\"" + item + "\">" + item + "</option>";
		});

		$("#id_channel").html(channelstring);
		$("#id_channel").selectpicker("refresh");

		if (type != "updatedb"){
			$("#id_version").html(versionstring);
			$("#id_version").selectpicker("refresh");

			$("#id_doc").show();
			var html = converter.makeHtml(data["pridoc"]);
			document.getElementById("id_doc").innerHTML = html;
		}
	})
}


function selectChannel() {
        $("#id_zone").html("");
        $("#id_zone").selectpicker("refresh");
        var gameid= $("#id_game").val();
        var channelid = $("#id_channel").val();

        if (channelid == ""){
            return false;
        }

        $.getJSON("/game/get_zoneinfo/?gameid=" + gameid + "&channelid=" + channelid,function (data) {
            var zonestring;

            $.each(data["zones_list"],function (i,item) {
                zonestring += "<option value=\"" + item[0] + "\">" + item[1] + "</option>";
            });

            $("#id_zone").html(zonestring);
            $("#id_zone").selectpicker("refresh");
        })
    }