import base64

import pychrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# greate_swords = (
#     "lizard_greatsword",
#     "greatsword_of_damnation_greatsword",
#     "greatsword_of_solitude",
#     "bastard_sword",
#     "claymore",
#     "iron_greatsword_greatswords",
#     "lordsworns_greatsword",
#     "knights_greatsword",
#     "banished_knights_greatsword",
#     "forked_greatsword",
#     "flamberge",
#     "gargoyles_greatsword",
#     "gargoyles_blackblade",
#     "inseparable_sword",
#     "sword_of_milos",
#     "marais_executioners_sword",
#     "ordoviss_greatsword",
#     "alabaster_lords_sword",
#     "deaths_poker",
#     "helphens_steeple",
#     "blasphemous_blade",
#     "golden_order_greatsword",
#     "dark_moon_greatsword",
#     "sacred_relic_sword")

greate_swords = "greatsword_of_solitude"

fetch_to_url = "https://eldenring.wiki.fextralife.com/file/Elden-Ring/"

# Set up Chrome driver with remote debugging enabled
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

dev_tools = pychrome.Browser(url="http://localhost:9222/")
tab = dev_tools.list_tab()[0]
tab.start()

tab.Page.enable()
tab.Network.enable()


def gs_name(url) -> str:
    name = url.removesuffix("_weapon_elden_ring_wiki_guide_200px.png")
    name = name.removesuffix("_elden_ring_shadow_of_the_erdtree_dlc_wiki_guide_200px.png")
    name = name.removesuffix("_elden_ring_wiki_guide_200px.png")
    name = name.removesuffix(".png")
    name = name.removeprefix(fetch_to_url)
    return name


def save_image(content, url):
    filename = gs_name(url)
    if filename in greate_swords:
        with open(filename + ".png", "wb") as f:
            f.write(base64.b64decode(content))
        print(f"Image saved as {filename}")


def handle_response(**kwargs):
    response = kwargs.get('response', {})
    if response.get("mimeType").startswith("image/webp"):
        request_id = kwargs.get('requestId')
        # Get the response body
        response_body = tab.Network.getResponseBody(requestId=request_id)
        content = response_body.get('body')
        if response_body.get('base64Encoded', False):
            save_image(content, response["url"])


def request_will_be_sent(**kwargs):
    url = kwargs.get("request", {}).get("url")
    if url and url.endswith(".png"):
        print("PNG image requested:", url)


tab.Network.requestWillBeSent = request_will_be_sent
tab.Network.responseReceived = handle_response

driver.get("https://eldenring.wiki.fextralife.com/Greatswords")

input("Press Enter to exit...\n")
