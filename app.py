from flask import Flask, render_template, request
from azure.identity import ClientSecretCredential
from azure.mgmt.media import AzureMediaServices
import random
from azure.mgmt.media.models import (
    IPRange,
    IPAccessControl,
    LiveEvent,
    LiveEventInputAccessControl,
    LiveEventPreviewAccessControl,
    LiveEventPreview,
    LiveEventInput,
    LiveEventEncoding,
    LiveEventEncodingType,
    LiveEventInputProtocol,
    StreamOptionsFlag
)

app = Flask(__name__)

# Tenant ID for your Azure Subscription
TENANT_ID = "31091900-0d4d-423b-b04e-fe4201c763bd"

# Your Application Client ID of your Service Principal
CLIENT_ID = "49252a39-ed92-45a1-9427-4b456fa3a4d7"

# Your Service Principal secret key
CLIENT_SECRET = "MLm8Q~51.W7AuZOzeZNDHqIsl-whM32gGc1X7aGj"

# Get the environment variables
subscription_id = "39c41e42-c205-40c1-b1bc-ef2eac9429b3"
resource_group ="Digiplus"
account_name ="digipluscamera"

# This is a random string that will be added to the naming of things so that you don't have to keep doing this during testing
uniqueness = random.randint(0,9999)
prefix = "myLiveEvent1"
live_event_name = f'{prefix}-{uniqueness}'

print("Starting the Live Streaming sample for Azure Media Services")
# The AMS Client
print("Creating AMS Client")


allow_all_input_range=IPRange(name="AllowAll", address="0.0.0.0", subnet_prefix_length=0)

live_event_input_access=LiveEventInputAccessControl(ip=IPAccessControl(allow=[allow_all_input_range]))

live_event_preview=LiveEventPreview(access_control=LiveEventPreviewAccessControl(ip=IPAccessControl(allow=[allow_all_input_range])))

# Create different element
accessToken='9eb1f703b149417c8448771867f48501'
live_event_create=LiveEvent(
    location="East US",
    description="Sample 720P Encoding Live Event from Python SDK sample",
    use_static_hostname=True,
    input=LiveEventInput(
        streaming_protocol=LiveEventInputProtocol.RTMP,
        access_control=live_event_input_access,
        access_token=accessToken
    ),

    encoding=LiveEventEncoding(
        encoding_type=LiveEventEncodingType.PASSTHROUGH_STANDARD,
    ),
    preview=live_event_preview,
    stream_options=[StreamOptionsFlag.LOW_LATENCY]
)

@app.route("/")
def hello_world():
    return render_template("script.html")

@app.route("/liveStart/")
def main():

    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_start(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
    ).result()
    output = str(response)

    live_output_name = 'myOutput1'
    response1 = client.live_outputs.begin_create(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        live_output_name=live_output_name,
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
    
    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_stop(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        parameters={"removeOutputsOnStop": True},
    ).result()
    output = str(response)
    return render_template("script.html")

@app.route('/liveCreate/')
def liveCreate():
    client = AzureMediaServices(
    credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
    subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response3 = client.live_events.begin_create(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        parameters=live_event_create
    ).result()
    output3 = str(response3)
    return (f"""<p>l'URL de l'ingestion est :</p> 
                <p> rtmp://{live_event_name}-{account_name}-usea.channel.media.azure.net:1935/live/{accessToken} </p>""")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)