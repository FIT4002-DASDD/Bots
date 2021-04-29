/**
 * This module downloads old assets from S3 temporarily and re-uploads them to the new S3 bucket.
 */
const fs = require("fs");
const https = require("https");
const axios = require("axios");
const csv = require("csvtojson");
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
  const adsJson = await csv().fromFile("./ads_postgres.csv");
  adsJson.forEach((ad) => {
    let adProcessed = [];
    adProcessed.push(ad.image !== "" ? ad.image : null);
    adProcessed.push(ad.html !== "" ? ad.html : null);
    ads.push(adProcessed);
  });

  ads = ads.slice(0, 5);  // take small sample for testing
  // For each tuple, download the images and html from the old S3 buckets and re-upload to our new S3 bucket
  for (const row of ads) {
    const [imageUrl, htmlUrl] = row;

    if (imageUrl) {
      const imageResourcePath = new URL(imageUrl).pathname.slice(1);

      const {data} = await axios.get(imageUrl, {responseType: 'stream'});
        const file = fs.createWriteStream(`./out/${imageResourcePath}`);
        data.pipe(file);
        file.on("finish", async () => {
          file.close();

          const newImageParams = {
            Key: imageResourcePath,
            Bucket: NEW_BUCKET_NAME,
            Body: fs.readFileSync(`./out/${imageResourcePath}`),
          };
          await s3
            .upload(newImageParams, (err, data) => {
              if (err) {
                console.error(err.message);
                throw err;
              }

              const newImagePath = data.Location;
              // Update the image path in the db
              mockDb[mockDb.indexOf(row)][0] = newImagePath;

              fs.unlinkSync(`./out/${imageResourcePath}`); // unlink temporarily downloaded asset
            })
            .promise();
        });
    }

    if (htmlUrl && isValidUrl(htmlUrl)) {
      const htmlResourcePath = new URL(htmlUrl).pathname.slice(1);

      const {data} = await axios.get(htmlUrl);
        const file = fs.createWriteStream(`./out/${htmlResourcePath}`);
        data.pipe(file);
        file.on("finish", async () => {
          file.close();

          const newHtmlParams = {
            Key: htmlResourcePath,
            Bucket: NEW_BUCKET_NAME,
            Body: fs.readFileSync(`./out/${htmlResourcePath}`),
          };
          await s3
            .upload(newHtmlParams, (err, data) => {
              if (err) {
                console.error(err.message);
                throw err;
              }

              const newHtmlPath = data.Location;
              mockDb[mockDb.indexOf(row)][1] = newHtmlPath;

              fs.unlinkSync(`./out/${htmlResourcePath}`);
            })
            .promise();
        });
    }
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
