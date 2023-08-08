let player;

function onPlayerReady(event) {
// const links = document.querySelectorAll("#times a");
// console.log(links)
// links.forEach((link) => {
//     link.addEventListener("click", function (event) {
//         event.preventDefault();
//         const time = parseFloat(link.innerHTML);
//         player.seekTo(time);
//     });
// });

}

function createYouTubePlayer() {
    const val = document.getElementById("id_url").value;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#\&\?]*).*/;
    const match = val.match(regExp);
    const idd = match && match[2];

    function onYouTubeIframeAPIReady(video_ID) {
        player = new YT.Player("player", {
            height: "360",
            width: "640",
            videoId: idd,
            events: {
                "onReady": onPlayerReady
            }
        });
    }

    onYouTubeIframeAPIReady(idd);
}

// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function (event) {
    const getPlayerButton = document.querySelector('input[name="get"]');
    getPlayerButton.addEventListener("click", function (event) {
        event.preventDefault();
        createYouTubePlayer();
    });

});

function seek(t){
    player.seekTo(t);
}