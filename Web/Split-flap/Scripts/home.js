
$(document).ready(function () {
    function refreshMessages() {
        $.get("Messages/", function (result) {
            var lines = JSON.parse(result);
            var showedText = "";
            for (var i = 0; i < lines.length; i++) {
                var date = lines[i].CreatedOn;
                var day = date.slice(5, 7);
                var month = date.slice(8, 10);
                var hour = date.slice(11, 13);
                var minute = date.slice(14, 16);
                var dateStr = month + "/" + day + " " + hour + ":" + minute;
                showedText += dateStr + " > " + lines[i].Content + "<br />";
            }
            $("#history").html(showedText);
        });
    }

    $("#submitMessage").click(function () {
        $.post("Messages/Create", { Content: $("#message").val() }, function (result) {
            refreshMessages();
        });
    });

    setInterval(refreshMessages, 60 * 1000);
    refreshMessages();
});