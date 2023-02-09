const ytdl = require("ytdl-core");
const fs = require("fs");
const { exit } = require("process");

// find how to insert link to download
// or LINKS to download
const args = process.argv;

console.log(args);

// exit();
const url = "https://www.youtube.com/watch?v=QH2-TGUlwu4"

// download all the songs using ytdl

var song_name;
for (var i = 1, song_name = args[i]; i < args.length; i++){
    console.log(song_name);
}

exit()
ytdl(url)
  .pipe(fs.createWriteStream("song.mp3"))
  .on("finish", () => {
    console.log("Finished downloading.");
  });




