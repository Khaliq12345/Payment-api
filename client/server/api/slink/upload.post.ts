import FormData from "form-data";

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const formData = await readFormData(event);
  const imageFile = formData.get("image") as File;

  if (!imageFile) {
    throw createError({ statusCode: 400, message: "No image provided" });
  }

  const arrayBuffer = await imageFile.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  const slinkForm = new FormData();
  slinkForm.append("image", buffer, {
    filename: imageFile.name,
    contentType: imageFile.type,
  });

  const response = await fetch(`${config.slinkUrl}/api/external/upload`, {
    method: "POST",
    headers: {
      ...slinkForm.getHeaders(), // correctly sets Content-Type with boundary
      Authorization: `Bearer ${config.slinkApiKey}`,
      Origin: config.slinkUrl,
      Referer: `${config.slinkUrl}/upload`,
      "User-Agent":
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0",
    },
    body: slinkForm.getBuffer(), // serialized buffer with boundary
  });

  if (!response.ok) {
    const err = await response.text();
    const parsed = JSON.parse(err);

    // Handle duplicate image - extract existing image ID
    const duplicate = parsed?.error?.violations?.find(
      (v: any) => v.property === "duplicate_image",
    );
    if (duplicate) {
      const imageId = duplicate.data.imageId;
      return {
        url: `https://digiproduct.tech2work.tech/image/public/${imageId}.jpg`,
        id: imageId,
      };
    }

    throw createError({
      statusCode: response.status,
      message: err || "Slink upload failed",
    });
  }

  const result = await response.json();
  return {
    url: `https://digiproduct.tech2work.tech/image/public/${result.id}.jpg`,
    id: result.id,
  };
});
