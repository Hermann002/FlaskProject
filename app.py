from flask import Flask, render_template
from azure.identity import ClientSecretCredential
from azure.mgmt.media import AzureMediaServices

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("script.html")

@app.route("/liveStart/")
def main():
    # Tenant ID for your Azure Subscription
    TENANT_ID = "31091900-0d4d-423b-b04e-fe4201c763bd"

    # Your Application Client ID of your Service Principal
    CLIENT_ID = "49252a39-ed92-45a1-9427-4b456fa3a4d7"

    # Your Service Principal secret key
    CLIENT_SECRET = "MLm8Q~51.W7AuZOzeZNDHqIsl-whM32gGc1X7aGj"
    
    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_start(
        resource_group_name="Digiplus",
        account_name="digipluscamera",
        live_event_name="digiplusstream",
    ).result()
    output = str(response)

    response1 = client.live_outputs.begin_create(
        resource_group_name="Digiplus",
        account_name="digipluscamera",
        live_event_name="digiplusstream",
        live_output_name="myLiveOutput1",
        parameters={
            "properties": {
                "archiveWindowLength": "PT5M",
                "assetName": "myAsset1",
                "description": "test live output 1",
                "hls": {"fragmentsPerTsSegment": 5},
                "manifestName": "testmanifest",
                "rewindWindowLength": "PT4M",
            }
        },
    ).result()
    output1 = str(response1)
    return render_template("script.html")
    
@app.route("/liveStop/")
def stop():
    
    # Tenant ID for your Azure Subscription
    TENANT_ID = "31091900-0d4d-423b-b04e-fe4201c763bd"

    # Your Application Client ID of your Service Principal
    CLIENT_ID = "49252a39-ed92-45a1-9427-4b456fa3a4d7"

    # Your Service Principal secret key
    CLIENT_SECRET = "MLm8Q~51.W7AuZOzeZNDHqIsl-whM32gGc1X7aGj"
    
    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_stop(
        resource_group_name="Digiplus",
        account_name="digipluscamera",
        live_event_name="digiplusstream",
        parameters={"removeOutputsOnStop": True},
    ).result()
    output = str(response)
    return render_template("script.html")

# @app.route('/liveCreate/')
# def liveCreate():
#     # Tenant ID for your Azure Subscription
#     TENANT_ID = "31091900-0d4d-423b-b04e-fe4201c763bd"

#     # Your Application Client ID of your Service Principal
#     CLIENT_ID = "49252a39-ed92-45a1-9427-4b456fa3a4d7"

#     # Your Service Principal secret key
#     CLIENT_SECRET = "MLm8Q~51.W7AuZOzeZNDHqIsl-whM32gGc1X7aGj"
    
#     client = AzureMediaServices(
#         credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
#         subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
#     )

#     response3 = client.live_events.begin_create(
#         resource_group_name="Digiplus",
#         account_name="digipluscamera",
#         live_event_name="myLiveEvent1",
#         parameters={
#             "location": "East US",
#             "properties": {
#                 "description": "test event 1",
#                 "input": {
#                     "accessControl": {
#                         "ip": {"allow": [{"address": "0.0.0.0", "name": "AllowAll", "subnetPrefixLength": 0}]}
#                     },
#                     "keyFrameIntervalDuration": "PT6S",
#                     "streamingProtocol": "RTMP",
#                 },
#                 "preview": {
#                     "accessControl": {
#                         "ip": {"allow": [{"address": "0.0.0.0", "name": "AllowAll", "subnetPrefixLength": 0}]}
#                     }
#                 },
#             },
#             "tags": {"tag1": "value1", "tag2": "value2"},
#         },
#     ).result()
#     output3 = str(response3)
#     return output3