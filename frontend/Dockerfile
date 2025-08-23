# ---------- Build Stage ----------
FROM node:18 AS build
WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy source and build
COPY frontend/ ./
RUN npm run build   # Vite outputs to /app/dist

# ---------- Production Stage ----------
FROM nginx:stable-alpine

# Copy Vite output (dist folder)
COPY --from=build /app/dist /usr/share/nginx/html

# Custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
