import pytest


class TestActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Arrange: Client ready | Act: GET /activities | Assert: 200 with activities"""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
    
    def test_get_activities_has_required_fields(self, client):
        """Arrange: Client ready | Act: GET /activities | Assert: Each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful(self, client):
        """Arrange: Valid email and activity | Act: POST signup | Assert: 200 and participant added"""
        email = "test@example.com"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
    
    def test_signup_duplicate_raises_400(self, client):
        """Arrange: Email already signed up | Act: POST signup with same email | Assert: 400 error"""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_invalid_activity_raises_404(self, client):
        """Arrange: Invalid activity name | Act: POST signup | Assert: 404 error"""
        email = "test@example.com"
        activity = "NonExistent Activity"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_successful(self, client):
        """Arrange: Email signed up | Act: DELETE unregister | Assert: 200 and participant removed"""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity]["participants"]
    
    def test_unregister_nonexistent_participant_raises_404(self, client):
        """Arrange: Email not in activity | Act: DELETE unregister | Assert: 404 error"""
        email = "notinactivity@example.com"
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_invalid_activity_raises_404(self, client):
        """Arrange: Invalid activity name | Act: DELETE unregister | Assert: 404 error"""
        email = "test@example.com"
        activity = "NonExistent Activity"
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
