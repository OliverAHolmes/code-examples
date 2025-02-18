# --- 1) Build Stage ---
FROM rust:1.72-bullseye AS builder

WORKDIR /usr/src/app

# Copy Cargo.* first
COPY actix-web-demo/Cargo.toml actix-web-demo/Cargo.toml
COPY actix-web-demo/Cargo.lock actix-web-demo/Cargo.lock
RUN mkdir -p actix-web-demo/src

# Dummy main.rs to cache dependencies
RUN echo "fn main() {}" > actix-web-demo/src/main.rs

WORKDIR /usr/src/app/actix-web-demo
RUN cargo build --release || true

# Now copy your actual source code
COPY actix-web-demo/src/ src/
RUN cargo build --release

# --- 2) Runtime Stage ---
FROM debian:bullseye-slim

RUN useradd -m appuser
WORKDIR /usr/local/bin
COPY --from=builder /usr/src/app/actix-web-demo/target/release/actix-web-demo .
EXPOSE 8000
USER appuser
CMD ["./actix-web-demo"]
