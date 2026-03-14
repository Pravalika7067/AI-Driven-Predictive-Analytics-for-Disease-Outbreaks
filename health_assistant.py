import google.generativeai as genai
from tavily import TavilyClient
import json

# Configuration
GEMINI_API_KEY = "AIzaSyBiTrG5Q98e2LCAr4waJp28wrlPaBMqbLk"
TAVILY_API_KEY = "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"

genai.configure(api_key=GEMINI_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def get_medical_advice(disease_name, risk_level, area):
    """
    Get medicine prescriptions and nearby recommendations using Gemini and Tavily.
    """
    
    try:
        # 1. Use Gemini for Prescriptions and Advice
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Disease: {disease_name}
        Risk Level: {risk_level}
        
        As an AI medical assistant, provide the following information:
        1. A list of commonly prescribed medicines for this condition (include a strong disclaimer that this is not a substitute for professional medical advice).
        2. General health advice and lifestyle changes for this condition.
        3. Emergency signs to watch out for.
        
        IMPORTANT: Provide the response in clean, user-friendly Markdown format with clear headings and bullet points. 
        DO NOT return code blocks, JSON, or raw dictionary structures. Use bold text for emphasis.
        """
        
        response = model.generate_content(prompt)
        prescription_advice = response.text
        
        # 2. Use Tavily for Nearby Medical Shops
        shop_query = f"top rated medical shops near {area} where medicines for {disease_name} are available"
        shop_results = tavily.search(query=shop_query, max_results=3)
        
        medical_shops = []
        for res in shop_results['results']:
            medical_shops.append({
                "name": res.get("title", "Unknown Shop"),
                "link": res.get("url", "#"),
                "snippet": res.get("content", "No information available.")
            })
            
        # 3. Use Tavily for Nearby Hospitals
        hospital_query = f"top rated hospitals and clinics near {area} specializing in {disease_name} or general medicine"
        hospital_results = tavily.search(query=hospital_query, max_results=3)
        
        hospitals = []
        for res in hospital_results['results']:
            hospitals.append({
                "name": res.get("title", "Unknown Hospital"),
                "link": res.get("url", "#"),
                "snippet": res.get("content", "No information available.")
            })
            
        return {
            "prescription_advice": prescription_advice,
            "medical_shops": medical_shops,
            "hospitals": hospitals
        }
    except Exception as e:
        return {
            "prescription_advice": f"Error fetching AI advice: {str(e)}",
            "medical_shops": [],
            "hospitals": []
        }
