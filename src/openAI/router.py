from supabase import create_client, Client
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv('API_KEY')
debug_mode = os.getenv('DEBUG')
client = OpenAI(
  api_key=os.getenv('OPEN_AI_DEV_KEY'),
)

router = APIRouter()

def getSupabaseClient():
  dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
  load_dotenv(dotenv_path)
  # Access environment variables
  api_key = os.getenv('SUPABASE_KEY')
  project_url = os.getenv('SUPABASE_URL') 
  supabase: Client = create_client(project_url, api_key)
  
  return supabase

@router.get("/testOpenAI")
def testingOpenAI():
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a unhelpful assistant by responding in broken english. However, you have a 1/2 probability of being literally a USMC drill instructor."},
      {"role": "user", "content": "Hello!"},
    ],
  )
  return completion

