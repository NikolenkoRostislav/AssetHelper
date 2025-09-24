from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_route():
    response = client.get("/bg-rm/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_bg_rem_image_no_file():
    response = client.post("/bg-rm/image")
    assert response.status_code == 422

def test_bg_rem_images_no_file():
    response = client.post("/bg-rm/images")
    assert response.status_code == 422

def test_bg_rem_images_zip_no_file():
    response = client.post("/bg-rm/images/zip")
    assert response.status_code == 422

def test_invalid_route():
    response = client.get("/bg-rm/invalid")
    assert response.status_code == 404

def test_invalid_method():
    response = client.put("/bg-rm/image")
    assert response.status_code == 405

def test_image_route():
    with open("tests/assets/test_image_1.jfif", "rb") as f:
        response = client.post("/bg-rm/image", files={"image": ("test.png", f, "image/png")})
    assert response.status_code == 200

def test_image_route_bad_data():
    with open("tests/assets/test_not_image.mp3", "rb") as f:
        response = client.post("/bg-rm/image", files={"image": ("test.png", f, "image/png")})
    assert response.status_code == 400

def test_images_route():
    with open("tests/assets/test_image_1.jfif", "rb") as f1, open("tests/assets/test_image_2.jpg", "rb") as f2:
        response = client.post("/bg-rm/images", files=[
            ("images", ("test1.png", f1, "image/png")),
            ("images", ("test2.png", f2, "image/png"))
        ])
    assert response.status_code == 200

def test_images_route_bad_data():
    with open("tests/assets/test_image_1.jfif", "rb") as f1, open("tests/assets/test_not_image.mp3", "rb") as f2:
        response = client.post("/bg-rm/images", files=[
            ("images", ("test1.png", f1, "image/png")),
            ("images", ("test2.png", f2, "image/png"))
        ])
    assert response.status_code == 400

def test_images_zip_route():
    with open("tests/assets/test_images_zip.zip", "rb") as f:
        response = client.post("/bg-rm/images/zip", files={"zip_file": ("test.zip", f, "application/zip")})
    assert response.status_code == 200

def test_images_zip_route_bad_data():
    with open("tests/assets/test_not_image.mp3", "rb") as f:
        response = client.post("/bg-rm/images/zip", files={"zip_file": ("test.zip", f, "application/zip")})
    assert response.status_code == 400
