from google import genai
from apify_client import ApifyClient
import requests



GEMINI_API_KEY = "AQ.Ab8RN6KogO9rmJRbRA-qIXDaLJwQtSyoSkRTmjW9f_ZY5HTuag"
APIFY_TOKEN = "apify_api_EjTVcwfUIWNWHpLEh1SQpa5uTj4Fog1gDRmx"
ALLIMAGES_API_KEY = "6798e1fc-3954-41f9-bd1b-aa186958a22d"
PINTEREST_TOKEN = "YOUR_PINTEREST_ACCESS_TOKEN"
BOARD_ID = "YOUR_PINTEREST_BOARD_ID"

client = genai.Client(api_key=GEMINI_API_KEY)
apify_client = ApifyClient(APIFY_TOKEN)


# AGENT 1: Find niche product
def agent_find_niche_product(prompt="Find a trending niche product which has high margin rate as well as high demand. Return only the product name in 3 to 5 words so it can be searched on Amazon."):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    product = response.text.strip()
    print("[Agent 1] Niche product:", product)
    return product

# AGENT 2: Scrape product details from Amazon
def agent_scrape_amazon(product_name):
    run_input = {
        "search": product_name,
        "maxResults": 1,
    }
    run = apify_client.actor("apify/amazon-scraper").call(run_input=run_input)
    items = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    if items:
        details = items[0]
        print("[Agent 2] Amazon details:", details)
        return details
    else:
        raise Exception("No product found on Amazon")


# AGENT 3: Create Pinterest description
def agent_create_description(product_details):
    text = f"Create a Pinterest SEO description for: {product_details}"
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=text
    )
    description = response.text.strip()
    print("[Agent 3] Pinterest description:", description)
    return description

# AGENT 4: Generate product image
def agent_generate_image(prompt):
    url = "https://api.all-images.ai/v1/generate"
    headers = {"Authorization": f"Bearer {ALLIMAGES_API_KEY}"}
    payload = {"prompt": prompt, "style": "guided"}
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        image_url = resp.json()["image_url"]
        print("[Agent 4] Image URL:", image_url)
        return image_url
    else:
        raise Exception(f"Image generation failed: {resp.text}")


# AGENT 5: Create Pinterest Pin
def agent_create_pin(board_id, image_url, description):
    url = "https://api.pinterest.com/v1/pins/"
    headers = {"Authorization": f"Bearer {PINTEREST_TOKEN}"}
    payload = {
        "board": board_id,
        "note": description,
        "image_url": image_url
    }
    resp = requests.post(url, data=payload, headers=headers)
    if resp.status_code == 201:
        print("[Agent 5] Pin created successfully!")
    else:
        print("[Agent 5] Pinterest error:", resp.text)


# MAIN PIPELINE
if __name__ == "__main__":
    try:
        niche_product = agent_find_niche_product()
        product_details = agent_scrape_amazon(niche_product)
        description = agent_create_description(product_details)
        image_url = agent_generate_image(niche_product)
        agent_create_pin(BOARD_ID, image_url, description)
    except Exception as e:
        print("Workflow failed:", e)
