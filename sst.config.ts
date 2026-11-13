/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "multistage-photo-admin",
      removal: input?.stage === "production" ? "retain" : "remove",
      protect: ["production"].includes(input?.stage),
      home: "aws",
    };
  },
  async run() {
    const bucketId = process.env.AWS_S3_BUCKET_ID;

    if (!bucketId) throw new Error("AWS_S3_BUCKET_ID is missing. Apply infra first");

    const media = sst.aws.Bucket.get("Media", bucketId);

    new sst.aws.Function("Hono", {
      url: true,
      handler: "./apps/api/src/index.handler",
      link: [media],
    });
  },
});
