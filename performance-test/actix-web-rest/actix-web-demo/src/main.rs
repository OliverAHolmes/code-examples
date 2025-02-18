use actix_web::{get, App, HttpResponse, HttpServer, Responder};
use serde::Serialize;

// A small struct representing your JSON response
#[derive(Serialize)]
struct HelloResponse {
    message: &'static str,
}

#[get("/actix-web")]
async fn hello() -> impl Responder {
    // Return a JSON object { "message": "Hello, world!" }
    HttpResponse::Ok().json(HelloResponse {
        message: "Hello, world!",
    })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let host = "0.0.0.0";
    let port = 8000;
    println!("Server running at http://{}:{}", host, port);

    HttpServer::new(|| {
        App::new()
            .service(hello)  // register the `#[get("/actix-web")]` route
    })
    .bind((host, port))?
    .run()
    .await
}
