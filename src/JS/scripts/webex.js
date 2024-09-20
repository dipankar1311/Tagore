function listMeetingTranscripts() {
    doGet("https://webexapis.com/v1/meetingTranscripts", function (result) {
        $.each(result["items"], function (idx, value) {
            $("#idx-list-transcripts").append(`<li>
                <a class="dropdown-item" href="#" data-meeting-id="${value.meetingId}" data-vtt="${value.vttDownloadLink}">
                    ${value.meetingTopic} ${moment(value.startTime).format("MMM Do YYYY h:mm:ss A")}
                </a>
            </li>`);
        });
    });
}

function onlyNumbers(str) {
    return /^[0-9]+$/.test(str);
}

function getMeetingTranscript(vttLink) {
    doGet(vttLink, function (result) {
        html = "";
        txt = "";

        result = result.replace(/(?:\r\n|\r|\n)/g, '<br>');
        $.each(result.split("<br>"), function (idx, line) {
            if (line && line.length > 0 && line != "WEBVTT" && !line.includes("-->") && !onlyNumbers(line)) {
                html += line + "<br>";
                txt += line + "\n";
            }
        });
        html += "<br><br><br>";

        $("#idx-meeting-transcript").html(html);

        // Download to file
        downloadHeader = "data:text/plain;charset=utf-8,";
        $("#idx-meeting-transcript-file").attr("href", downloadHeader + txt);

        $("#idx-meeting-transcript-file")[0].click();
        $("#btn-opt-transcript").parent().show();
        $("#idx-list-transcripts").parent().hide();
        $("#idx-ocr-input").show();
    });
}

async function getMeetingTranscriptOpt(link) {
    console.log("HELLO");
    var outputLength = 0;
    var locked = false;
    var loop = true;
	$("#idx-meeting-transcript-file-meta")[0].click();
    while (loop && outputLength < 1) {
        console.log("HELLO");
        await new Promise(r => setTimeout(r, 2000));

        console.log("CHECKING...");
        if (!locked) {
            locked = true;
            console.log("Requested latest file");
            doGet("http://" + window.location.host + "/resources/updatedtranscript/optimized_transcript.txt", function(result) {
                outputLength = result.length;
                console.log(`outputLength: ${outputLength}`);
                locked = false;
            }, function(err) {
            	locked = false;
            });
        }

        if (outputLength > 1) {
            loop = false;
            console.log("OUTPUT READY");
            // Give it a second to load any new data
            await new Promise(r => setTimeout(r, 1000));

            doGet("http://" + window.location.host + "/resources/updatedtranscript/optimized_transcript.txt", function(result) {
                console.log(result);
                html = "";

                result = result.replace(/(?:\r\n|\r|\n)/g, '<br>');
                $.each(result.split("<br>"), function (idx, line) {
                    if (line && line.length > 0) {
                        html += line + "<br>";
                    }
                });
                html += "<br><br><br>";

                $("#idx-meeting-transcript-opt").html(html);
                $("#btn-opt-transcript").parent().hide();

                $("#idx-ocr-output").show();
            });
        }
    }
} 

function getMeetingRecording(meetingId) {
    recodringListUrl = `https://webexapis.com/v1/recordings?meetingId=${meetingId}`;
    doGet(recodringListUrl, function(result) {
        recordingId = result.items[0].id;

        recordingDetailsUrl = `https://webexapis.com/v1/recordings/${recordingId}`;
        doGet(recordingDetailsUrl, function(result) {
            console.log(result.temporaryDirectDownloadLinks.audioDownloadLink);
            window.open(result.temporaryDirectDownloadLinks.audioDownloadLink, "_blank");
        });
    });
}

$(document).ready(async function () {
    listMeetingTranscripts();

    $(document).on("click", "#btn-get-transcript", function () {
        $("#idx-meeting-transcript").html("Loading...");
        ip = $("#ip-transcript").val();
        getMeetingTranscript(`https://webexapis.com/v1/meetingTranscripts/${ip}/download?format=vtt`);
    });

    $(document).on("click", "#idx-list-transcripts a.dropdown-item", function () {
        getMeetingTranscript($(this).attr("data-vtt").trim());

        $("#btn-opt-transcript").attr("data-link", $(this).attr("data-vtt").trim());
        $("#btn-opt-transcript").attr("data-meeting-id", $(this).attr("data-meeting-id").trim());
    });

    $(document).on("click", "#btn-opt-transcript", function () {
        getMeetingTranscriptOpt($(this).attr("data-link").trim());
        getMeetingRecording($(this).attr("data-meeting-id"));
    });

    $(document).on("click", "#idx-ocr-input", function () {
        $("#idx-ocr-input-modal").modal("show");
    });
    $(document).on("click", "#idx-ocr-output", function () {
        $("#idx-ocr-output-modal").modal("show");
		$("#idx-ocr-output-modal iframe")[0].src = $("#idx-ocr-output-modal iframe")[0].src; 
    }); 
});
