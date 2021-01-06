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

query = syn.tableQuery( " SELECT * FROM syn23534327 WHERE ( ( modifiedBy = 3382314 ) AND ( parentId = 'syn10141118' ) )" ) ### get list of lung cancer file IDs
query_df = query.asDataFrame()
query_IDs = query_df['id'].values
for syn_id in query_IDs:
     ent = syn.get(syn_id, downloadFile=False)
     client.download_file(ent._file_handle['bucketName'],
                                   ent._file_handle['key'],
                                   ent.name) ### the file will be downloaded to your current folder 

query = syn.tableQuery( " SELECT * FROM syn23534327 WHERE ( ( modifiedBy = 3382314 ) AND ( parentId = 'syn16810855' OR parentId = 'syn8262420' ) ) " ) ### get list of 'melanoma 1' file IDs
query_df = query.asDataFrame()
query_IDs = query_df['id'].values
for syn_id in query_IDs:
     ent = syn.get(syn_id, downloadFile=False)
     client.download_file(ent._file_handle['bucketName'],
                                   ent._file_handle['key'],
                                   ent.name) 

query = syn.tableQuery( " SELECT * FROM syn23534327 WHERE ( ( modifiedBy = 3382314 ) AND ( parentId = 'syn15672147' ) )" ) ### get list of 'melanoma 2' file IDs
query_df = query.asDataFrame()
query_IDs = query_df['id'].values
for syn_id in query_IDs:
     ent = syn.get(syn_id, downloadFile=False)
     client.download_file(ent._file_handle['bucketName'],
                                   ent._file_handle['key'],
                                   ent.name)