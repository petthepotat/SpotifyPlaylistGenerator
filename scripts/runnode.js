const ytdl = require("ytdl-core");
const fs = require("fs");
const { exit } = require("process");


// ----------------------------------------------

let COUNTER = 0;

// find how to insert link to download
// or LINKS to download
const args = process.argv;
// download all the songs using ytdl
async function download_audio(parse, download_path, ID) {
    var split = parse.split("|");
    var title = split[0];
    var link = split[1];

    // generate path
    var path = download_path + "/" + title + ".mp3";
    // create stream object
    const stream = ytdl(link, {
        filter: "audioonly",
        quality: "highestaudio",
    });

    // download
    console.log(`START|${title}`);
    stream.pipe(fs.createWriteStream(path));

    // output progress to console
    stream.on('progress', (chunkLength, downloaded, total) => {
        const percent = downloaded / total;
        console.log(`UPDATE|${title}|${(percent * 100).toFixed(2)}%`);
        // new Promise((resolve) => { setTimeout(() => {}, 100); });
    });
    stream.on('finish', () => {
        console.log(`FINISHED|${title}`);
    });
}

var path = args[1];
var song_name;
for (var i = 2; i < args.length; i++) {
    song_name = args[i];
    download_audio(song_name, path, COUNTER++);
}

// exit();