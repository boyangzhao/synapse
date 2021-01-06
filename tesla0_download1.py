import synapseclient ### requires Python 3+ 
import boto3

syn = synapseclient.login("username", "password") ### please enter your Synapse username and password. 
FOLDER = "syn23446508" ### this is the 'TESLA phase 1 data release' folder under which all the data is hosted

sts_credentials = syn.restGET(f"/entity/{FOLDER}/sts?permission=read_only") ### this is your 12hr temporary credentials to access the data based on your synapse ID
client = boto3.client(
    's3',
    aws_access_key_id=sts_credentials['accessKeyId'],
    aws_secret_access_key=sts_credentials['secretAccessKey'],
    aws_session_token=sts_credentials['sessionToken'],
)

### get list of lung cancer file IDs
query = syn.tableQuery( " SELECT * FROM syn23534327 WHERE ( ( modifiedBy = 3382314 ) AND ( parentId = 'syn10141118' ) )" ) 
query_df = query.asDataFrame()
query_IDs = query_df['id'].values
for syn_id in query_IDs:
    ent = syn.get(syn_id, downloadFile=False)
    print(ent)

# test download one file
client.download_file(ent._file_handle['bucketName'], ent._file_handle['key'], ent.name)
