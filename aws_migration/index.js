/**
 * This module downloads old assets from S3 temporarily and re-uploads them to the new S3 bucket.
 */
const fs = require("fs");
const https = require("https");
const axios = require("axios");
const csv = require("csvtojson");
const { Parser } = require("json2csv");
const s3 = require("./clients/s3-client-config");
const isValidUrl = require("./helpers/url-validator");

// const OLD_BUCKET_NAME = 'fit4002';
const NEW_BUCKET_NAME = "dasdd-core-stack-dasddadimages-qdzmhix51zg8";

// Make an temp directory to store temporary assets
const tmpDir = "./out/html";
if (!fs.existsSync(tmpDir)) {
  fs.mkdirSync(tmpDir, { recursive: true });
}

let ads = [];
(async () => {
  //convert csv into JSON
  let adsJson = await csv().fromFile("PATH_TO_CSV");
  adsJson.forEach((ad) => {
    let adProcessed = [];
    adProcessed.push(ad.image !== "" ? ad.image : null);
    adProcessed.push(ad.html !== "" ? ad.html : null);
    ads.push(adProcessed);
  });

  /*   ads = ads.slice(0, 200); // take small sample for testing */
  // For each tuple, download the images and html from the old S3 buckets and re-upload to our new S3 bucket
  for (const row of ads) {
    const [imageUrl, htmlUrl] = row;

    if (imageUrl) {
      const imageResourcePath = new URL(imageUrl).pathname.slice(1);

      const { data } = await axios.get(imageUrl, { responseType: "stream" });

      const file = fs.createWriteStream(`./out/${imageResourcePath}`);
      data.pipe(file);
      file.on("finish", async () => {
        file.close();

        const newImageParams = {
          Key: imageResourcePath,
          Bucket: NEW_BUCKET_NAME,
          Body: fs.readFileSync(`./out/${imageResourcePath}`),
        };
        s3.upload(newImageParams, (err, data) => {
          if (err) {
            console.error(err.message);
            throw err;
          }

          const newImagePath = data.Location;
          // Update the image path in the db
          ads[ads.indexOf(row)][0] = newImagePath;

          fs.unlinkSync(`./out/${imageResourcePath}`); // unlink temporarily downloaded asset
        });
      });
    }

    if (htmlUrl && isValidUrl(htmlUrl)) {
      const htmlResourcePath = new URL(htmlUrl).pathname.slice(1);

      const { data } = await axios.get(htmlUrl, { responseType: "stream" });

      const file = fs.createWriteStream(`./out/${htmlResourcePath}`);
      data.pipe(file);
      file.on("finish", async () => {
        file.close();

        const newHtmlParams = {
          Key: htmlResourcePath,
          Bucket: NEW_BUCKET_NAME,
          Body: fs.readFileSync(`./out/${htmlResourcePath}`),
        };
        s3.upload(newHtmlParams, (err, data) => {
          if (err) {
            console.error(err.message);
            throw err;
          }

          const newHtmlPath = data.Location;

          ads[ads.indexOf(row)][1] = newHtmlPath;

          fs.unlinkSync(`./out/${htmlResourcePath}`);
        });
      });
    }
  }

  //Replace old csv(still in JSON format) entries with updated image and html links
  adsJson.forEach((row, index) => {
    row.image = ads[index][0];
    row.html = ads[index][1];
  }, adsJson);

  //convert JSON back into csv
  const fields = [
    "id",
    "botId",
    "createdAt",
    "image",
    "headline",
    "html",
    "adLink",
    "loggedIn",
    "seenOn",
  ];
  const opts = { fields };
  try {
    const parser = new Parser(opts);
    const adsCsv = parser.parse(adsJson);
    fs.writeFile("SAVE_PATH_FOR_NEW_CSV", adsCsv, (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    });
  } catch (err) {
    console.error(err);
  }
})();

/* let mockDb = [
   [
     "https://fit4002.s3.ap-southeast-2.amazonaws.com/1602622580639_ad.png",
     "innerHTML",
   ], // scheme: image, html
   [
     null,
     "https://fit4002.s3.ap-southeast-2.amazonaws.com/html/1605715433450.html",
   ],
   [null, "innerHTML"],
   [
     "https://fit4002.s3.ap-southeast-2.amazonaws.com/1602435965483_ad.png",
     "innerHTML",
   ],
   
 ]; */
