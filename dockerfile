# ----------------- FRONTEND BUILD STAGE -----------------
FROM node:20-bookworm-slim AS frontend
WORKDIR /web

COPY package*.json ./
RUN npm ci

COPY next.config.js ./
COPY app ./app
RUN mkdir -p public

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build
RUN npm ci --omit=dev

# ----------------- FINAL IMAGE (MANIM + PY + NODE) -----------------
# Was: manimcommunity/manim:stable-nolatex  -> doesn't exist
FROM manimcommunity/manim:stable AS final
# (You can also pin: FROM manimcommunity/manim:v0.19.0)

USER root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    tini fonts-dejavu ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Python backend ----
COPY python/requirements.txt /app/python/requirements.txt
RUN pip install --no-cache-dir -r /app/python/requirements.txt || \
    pip install --no-cache-dir uvicorn fastapi pydantic python-dotenv openai requests
COPY python/ /app/python/

# ---- Frontend runtime bits ----
COPY --from=frontend /usr/local/bin/node /usr/local/bin/node
COPY --from=frontend /usr/local/bin/npm  /usr/local/bin/npm
COPY --from=frontend /usr/local/bin/npx  /usr/local/bin/npx
COPY --from=frontend /usr/local/lib/node_modules /usr/local/lib/node_modules

RUN mkdir -p /app/frontend
COPY --from=frontend /web/.next /app/frontend/.next
COPY --from=frontend /web/node_modules /app/frontend/node_modules
COPY --from=frontend /web/package.json /app/frontend/package.json
COPY --from=frontend /web/public /app/frontend/public

COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PYTHONUNBUFFERED=1 \
    NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    MANIM_RENDERER=cairo \
    MEDIA_DIR=/app/renders \
    PUBLIC_VIDEOS_DIR=/app/frontend/public/videos

RUN mkdir -p /app/renders /app/frontend/public/videos

RUN chown -R manimuser:manimuser /app
USER manimuser

EXPOSE 8000 3000
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["/app/start.sh"]
