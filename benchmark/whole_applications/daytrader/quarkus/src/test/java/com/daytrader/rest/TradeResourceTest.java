package com.daytrader.rest;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
class TradeResourceTest {
    @Test
    void testHelloEndpoint() {
        given()
          .when().get("/trade")
          .then()
             .statusCode(200)
             .body(is("Hello from Quarkus RESTiii"));
    }

}