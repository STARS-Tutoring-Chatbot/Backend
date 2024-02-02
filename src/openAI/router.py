from supabase import create_client, Client
import os
from dotenv import load_dotenv
from fastapi import APIRouter

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv('API_KEY')
debug_mode = os.getenv('DEBUG')

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
  pass




