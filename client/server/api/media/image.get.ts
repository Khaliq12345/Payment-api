export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const imageUrl = query.url as string;

  if (!imageUrl)
    throw createError({ statusCode: 400, message: "No URL provided" });

  console.log(imageUrl);
  const response = await fetch(imageUrl);
  const buffer = await response.arrayBuffer();
  const contentType = response.headers.get("content-type") || "image/jpeg";

  setHeader(event, "Content-Type", contentType);
  setHeader(event, "Cache-Control", "public, max-age=86400");

  return Buffer.from(buffer);
});
