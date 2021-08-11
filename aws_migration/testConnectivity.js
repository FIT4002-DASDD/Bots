const {
    S3Client,
    PutObjectCommand,
    CreateBucketCommand,
} = require("@aws-sdk/client-s3");
const {Pool} = require("pg");
require("dotenv").config();

const REGION = "us-east-1";
process.env.AWS_PROFILE = "educate";


const bucketName = "dasdd-bot-images";
const bucketParams = {Bucket: bucketName};
const keyName = "hello_world.txt";
const objectParams = {Bucket: bucketName, Key: keyName, Body: "Hello World!"};

const s3 = new S3Client({
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
        sessionToken: process.env.AWS_SESSION_TOKEN,
    },
    region: REGION,
});

const run = async () => {
    try {
        const data = await s3.send(new CreateBucketCommand(bucketParams));
        console.log("Success. Bucker created.", data);
    } catch (err) {
        console.error(err);
    }
    try {
        const results = await s3.send(new PutObjectCommand(objectParams));
        console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
    } catch (err) {
        console.error(err);
    }
}

const bucketName = "dasdd-core-stack-dasddadimages-qdzmhix51zg8";
const bucketParams = {Bucket: bucketName};
const keyName = "hello_world.txt";
const objectParams = {Bucket: bucketName, Key: keyName, Body: "Hello World!"};

const s3 = new S3Client({
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
        sessionToken: process.env.AWS_SESSION_TOKEN
    },
    region: REGION
});

const run = async () => {
    try {
        const data = await s3.send(new CreateBucketCommand(bucketParams));
        console.log('Success. Bucket created.', data);
    } catch (err) {
        console.error(err);
    }
    try {
        const results = await s3.send(new PutObjectCommand(objectParams));
        console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
    } catch (err) {
        console.error(err);
    }
};

run();

const pgClient = new Pool({
    user: process.env.PGUSER,
    host: process.env.PGHOST,
    database: process.env.PGDATABASE,
    password: process.env.PGPASSWORD,
    port: process.env.PGPORT,
});

pgClient.query("SELECT NOW() as now", (err, res) => {
    if (err) {
        console.log(err.stack);
    } else {
        console.log(res.rows[0]);
    }
});
