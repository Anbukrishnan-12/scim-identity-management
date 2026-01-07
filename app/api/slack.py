from fastapi import APIRouter, HTTPException
from app.service.slack import SlackService
from app.schemas.identity import SlackUserRequest, SlackUserResponse

router = APIRouter()

@router.post("/provision", response_model=SlackUserResponse, summary="Provision User to Slack")
async def provision_slack_user(request: SlackUserRequest):
    """
    **Provision User to Slack Workspace**
    
    Creates or retrieves user in Slack and assigns to specified channels.
    
    **Process:**
    1. Check if user exists in Slack by email
    2. If user doesn't exist, create new user with provided details
    3. Assign user to specified channels based on requirements
    4. Return user details and provisioning status
    
    **Request Fields:**
    - `email`: User's email address (required)
    - `first_name`: User's first name (required for new users)
    - `last_name`: User's last name (optional)
    - `channels`: List of Slack channels to assign user to
    
    **Response Status:**
    - `existing`: User already exists in Slack
    - `created`: New user created successfully
    - `failed`: User creation or provisioning failed
    """
    service = SlackService()
    result = await service.create_user_account(
        request.email, 
        request.first_name, 
        request.last_name, 
        request.channels
    )
    
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "Slack provisioning failed"))
    
    return SlackUserResponse(**result)

@router.get("/user/{email}")
async def get_slack_user(email: str):
    service = SlackService()
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user