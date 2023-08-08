const form1 = document.getElementById('form1');
const ytInput = document.getElementById('id_url');

form1.addEventListener('submit', (e) => {
    e.preventDefault();

    const ytId = getYoutubeId(ytInput.value);

    let player;

    function loadVideo(videoId, startSeconds = 0) {
        player = new YT.Player('player', {
            videoId: videoId,

            playerVars: {
                'autoplay': 1,
                'controls': 1,
                'start': startSeconds
            },
            events: {
                'onReady': onPlayerReady
            }
        });
    }

    function onPlayerReady(event) {
        // Event.target refers to the player object
        const player = event.target;

        // Add an event listener to each timestamp link
        const links = document.querySelectorAll('#timestamps a');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();

                // Get the timestamp from the link
                const time = link.getAttribute('date-time');

                // Seek to the timestamp in the player
                player.seekTo(time, true);
            });
        });
    }

})


