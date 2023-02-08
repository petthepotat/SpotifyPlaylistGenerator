const ytdl = require("ytdl-core");
const fs = require("fs");

// find how to insert link to download
// or LINKS to download
const url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";

ytdl(url)
  .pipe(fs.createWriteStream("song.mp3"))
  .on("finish", () => {
    console.log("Finished downloading.");
  });

