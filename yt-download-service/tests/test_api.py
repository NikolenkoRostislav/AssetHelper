from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_route():
    response = client.get("/yt-download/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_yt_download_video_no_url():
    response = client.get("/yt-download/video")
    assert response.status_code == 422

def test_yt_download_audio_no_url():
    response = client.get("/yt-download/audio")
    assert response.status_code == 422

def test_invalid_route():
    response = client.get("/yt-download/invalid")
    assert response.status_code == 404

def test_invalid_method():
    response = client.put("/yt-download/video")
    assert response.status_code == 405

def test_video_route():
    response = client.get("/yt-download/video", params={"url": "https://youtu.be/fxqE27gIZcc"})
    assert response.status_code == 200

def test_video_route_bad_data():
    response = client.get("/yt-download/video", params={"url": "Invalid URL"})
    assert response.status_code == 404

def test_audio_route():
    response = client.get("/yt-download/audio", params={"url": "https://youtu.be/fxqE27gIZcc"})
    assert response.status_code == 200

def test_audio_route_bad_data():
    response = client.get("/yt-download/audio", params={"url": "Invalid URL"})
    assert response.status_code == 404
