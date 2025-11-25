# Production runtime for pre-built Nuxt.js frontend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy pre-built output folder
COPY .output /app/.output

# Start the application
CMD ["node", ".output/server/index.mjs"]
