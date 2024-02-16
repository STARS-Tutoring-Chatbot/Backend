from supabase import create_client, Client
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter

router = APIRouter()
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv('API_KEY')
debug_mode = os.getenv('DEBUG')
client = OpenAI(
  api_key=os.getenv('OPEN_AI_DEV_KEY'),
)

@router.get("/admin")
def getAdmin():
  return {
    "route": "admin"
  }

def getSupabaseClient():
  dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
  load_dotenv(dotenv_path)
  # Access environment variables
  api_key = os.getenv('SUPABASE_KEY')
  project_url = os.getenv('SUPABASE_URL') 
  supabase: Client = create_client(project_url, api_key)
  
  return supabase

def session_is_valid(supabase: Client, session_id: str, user_id: str) -> bool:
    response = supabase.from_("users").select("id, instance_id, aud, role").eq("id", session_id).execute()
    if response.status_code == 200 and response.data:
        user_data = response.data[0]
        if user_data['instance_id'] == user_id:
            return True
    return False


@router.get("/testOpenAI")
def testingOpenAI():
  session_id = request.headers.get("id")
  user_id = request.headers.get("instance-id")
  if session_id and user_id:
    if session_is_valid(supabase, session_id, user_id):
      completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a unhelpful assistant by responding in broken english. However, you have a 1/2 probability of being literally a USMC drill instructor."},
          {"role": "user", "content": "Hello!"},
        ],
      )
      return completion
  raise HTTPException(status_code=401, detail="User not authenticated")


