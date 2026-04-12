// cleanup-r2.mjs
// Empties and deletes all R2 buckets EXCEPT ones in KEEP_BUCKETS
// Uses S3-compatible API - works with R2 Access Key + Secret
//
// SETUP (one time, from D:\GitHub\genesis-to-quantum):
//   npm install @aws-sdk/client-s3
//
// RUN:
//   $env:R2_ACCESS_KEY_ID="YOUR_KEY_HERE"
//   $env:R2_SECRET_ACCESS_KEY="YOUR_SECRET_HERE"
//   node cleanup-r2.mjs

import { S3Client, ListBucketsCommand, ListObjectsV2Command, DeleteObjectsCommand, DeleteBucketCommand } from "@aws-sdk/client-s3";
import * as readline from "node:readline/promises";

// KEEP THESE - everything else gets wiped
const KEEP = new Set(["theophysics", "theophysics-media"]);

const ACCOUNT_ID = "d6e387eea4a4dda973d797ece5c5c40a";
const ACCESS_KEY = process.env.R2_ACCESS_KEY_ID;
const SECRET_KEY = process.env.R2_SECRET_ACCESS_KEY;

if (!ACCESS_KEY || !SECRET_KEY) {
  console.error("Missing env vars. Set R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY first.");
  process.exit(1);
}

const s3 = new S3Client({
  region: "auto",
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: { accessKeyId: ACCESS_KEY, secretAccessKey: SECRET_KEY },
});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function emptyBucket(name) {
  let total = 0;
  let token;
  do {
    const res = await s3.send(new ListObjectsV2Command({ Bucket: name, MaxKeys: 1000, ContinuationToken: token }));
    const objects = res.Contents ?? [];
    if (objects.length > 0) {
      await s3.send(new DeleteObjectsCommand({
        Bucket: name,
        Delete: { Objects: objects.map((o) => ({ Key: o.Key })), Quiet: true },
      }));
      total += objects.length;
      process.stdout.write(`\r  Deleted ${total} objects...`);
    }
    token = res.IsTruncated ? res.NextContinuationToken : null;
    if (token) await sleep(100);
  } while (token);
  console.log(total > 0 ? `\r  Emptied ${total} objects.       ` : "  Already empty.");
}

async function main() {
  const { Buckets } = await s3.send(new ListBucketsCommand({}));
  const all = (Buckets ?? []).map((b) => b.Name);

  console.log("\n=== ALL BUCKETS ===");
  all.forEach((b) => console.log(`  ${KEEP.has(b) ? "KEEP" : "DEL "} ${b}`));

  const toDelete = all.filter((b) => !KEEP.has(b));

  if (toDelete.length === 0) { console.log("\nNothing to delete."); return; }

  console.log(`\n${toDelete.length} buckets will be emptied and deleted.`);

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const answer = await rl.question("\nType  DELETE-ALL  to confirm: ");
  rl.close();

  if (answer.trim() !== "DELETE-ALL") { console.log("Aborted."); return; }

  for (const bucket of toDelete) {
    console.log(`\n[${toDelete.indexOf(bucket) + 1}/${toDelete.length}] Processing: ${bucket}`);
    try {
      await emptyBucket(bucket);
      await s3.send(new DeleteBucketCommand({ Bucket: bucket }));
      console.log("  Bucket deleted.");
    } catch (e) {
      console.error(`  ERROR: ${e.message}`);
    }
    await sleep(300);
  }

  console.log("\n=== DONE === Kept: theophysics, theophysics-media");
}

main().catch((e) => { console.error("Fatal:", e.message); process.exit(1); });
