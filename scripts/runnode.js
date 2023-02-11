const ytdl = require("ytdl-core");
const fs = require("fs");
const { exit } = require("process");

// find how to insert link to download
// or LINKS to download
const args = process.argv;
// download all the songs using ytdl
function download_audio(parse, download_path) {
    var split = parse.split("|");
    var title = split[0];
    var link = split[1];
    // console.log(parse.split('|'));
    var path = download_path + "/" + title + ".mp3";
    console.log("Downloading", title, "to", path);

    // why no download?
    const stream = ytdl(link, {
        filter: "audioonly",
        quality: "highestaudio",
    });
    stream.pipe(fs.createWriteStream(path));
    stream.on('progress', (chunkLength, downloaded, total) => {
        const percent = downloaded / total;
        console.log(`Downloaded ${(percent * 100).toFixed(2)}%`);
        await (new Promise((resolve) => { setTimeout(() => {}, 100); }));
    });

    stream.on('finish', () => {
        console.log('Download completed.');
    });
}

var song_name;
for (var i = 1; i < args.length; i++) {
    song_name = args[i];
    download_audio(song_name, "assets");
}

// exit();