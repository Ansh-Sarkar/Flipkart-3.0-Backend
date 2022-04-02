from elastic_enterprise_search import AppSearch

app_search = AppSearch(
    "https://flipkart-grid-3-0.ent.eastus2.azure.elastic-cloud.com",
    http_auth="private-b1ufp7shxq9tg88v23grmzyn"
)
app_search.index_documents(
    engine_name="dab",
    documents=[{
        "id": "park_rocky-mountain",
        "title": "Rocky Mountain",
        "nps_link": "https://www.nps.gov/romo/index.htm",
        "states": [
            "Colorado"
        ],
        "visitors": 4517585,
        "world_heritage_site": False,
        "location": "40.4,-105.58",
        "acres": 265795.2,
        "date_established": "1915-01-26T06:00:00Z"
    }, {
        "id": "park_saguaro",
        "title": "Saguaro",
        "nps_link": "https://www.nps.gov/sagu/index.htm",
        "states": [
            "Arizona"
        ],
        "visitors": 820426,
        "world_heritage_site": False,
        "location": "32.25,-110.5",
        "acres": 91715.72,
        "date_established": "1994-10-14T05:00:00Z"
    },{
        "id": "park_saguaro",
        "title": "Saguaro",
        "nps_link": "https://www.nps.gov/sagu/index.htm",
        "states": [
            "Arizona"
        ],
        "visitors": 820426,
        "world_heritage_site": False,
        "location": "32.25,-110.5",
        "acres": 91715.72,
        "date_established": "1994-10-14T05:00:00Z"
    },{
        "id": "park_saguaro",
        "title": "Saguaro",
        "nps_link": "https://www.nps.gov/sagu/index.htm",
        "states": [
            "Arizona"
        ],
        "visitors": 820426,
        "world_heritage_site": False,
        "location": "32.25,-110.5",
        "acres": 91715.72,
        "date_established": "1994-10-14T05:00:00Z"
    },{
        "id": "ansh_Sarkar",
        "title": "sarkar",
        "nps_link": "https://www.nps.gov/sagu/index.htm",
        "states": [
            "west_bengal"
        ],
        "visitors": 820426,
        "world_heritage_site": False,
        "location": "32.25,-110.5",
        "acres": 91715.72,
        "date_established": "1994-10-14T05:00:00Z"
    }]
)