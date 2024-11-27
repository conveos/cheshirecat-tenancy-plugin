from cat.mad_hatter.decorators import tool, hook, plugin
from langchain.docstore.document import Document
from typing import Dict


# TODO there is an error in this plugin, must fix it

def get_tenant_id(cat):
    """
    Helper function that returns the tenant_id (if any)
    of the current user
    """
    tenant_id = None
    if( "tenant_id" in cat.user_data):

        tenant_id = cat.user_data["tenant_id"]
        
    else:
        tenant_id = cat.user_id

    return tenant_id


@hook(priority=90)
def before_rabbithole_insert_memory(doc: Document, cat) -> Document:
    """
    Before the cat stores a memory ( either declarative, episodic or procedural),
    stamps the memory with a tenant_id.
    """
    tenant_id = get_tenant_id(cat)


    doc.metadata["tenant_id"] = tenant_id
    

    print(f"\n\n---Tenant Manager ---\nDocument uploaded with tenant_id: { tenant_id }\n")

    return doc




@hook(priority=90 )
def before_cat_recalls_declarative_memories(
    declarative_recall_config: dict ,
    cat
) -> dict:
    
    """
    Before the cat recalls declarative memories, adds to the 
    declarative _recall_config the tenant_id of the current user
    """
    tenant_id = get_tenant_id(cat)
   

    declarative_recall_config["metadata"] = { "tenant_id": tenant_id }

    return declarative_recall_config

@hook(priority=0)
def before_cat_recalls_episodic_memories(episodic_recall_config: dict, cat) -> dict:
    """
   This plugin tries to ensure that there are no episodic
   memories shared. So in the metadata , there is a ffield "source"
   that helps us filter the generated episodic memories.
   """ 

    episodic_recall_config["metadata"] = { "source": cat.user_id }
    return episodic_recall_config


@hook(priority=99)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    """
    Core functionality for the Tenant Plugin.
    If the input starts with "tenant_id=< id >\n", the 
    before_cat_reads_message will cut the text above , filter the tenant_id 
    given by input and then add it on the user_data as an extra field

    In order to use this , input must be like this:
    >tenant_id=WATERMELON\n<user prompt>

    This is useful especially in the case of Shadow Users.
    """
    print(f"===================\n\n\nUSER MESSAGE: {user_message_json} \nUSER_ID:{ cat.user_id }")
    if( "tenant_id" in cat.user_data ):
        print("USER_DATA TENANT_ID: ",cat.user_data["tenant_id"])

    print("===================\n\n\n")
    if "tenant_id=" in user_message_json["text"]:
    
        input_split = user_message_json["text"].split('\n') # NOTE this splits the input message on new lines
    
        id = input_split[0].replace('tenant_id=','')

        user_message_json["text"] = user_message_json["text"].replace(input_split[0],'')
        user_message_json["text"] = user_message_json["text"].replace( id ,'')

        cat.user_data["tenant_id"]=id



    return user_message_json


@hook(priority=80)
def agent_fast_reply(fast_reply, cat):
    """
    This hook is implements a helper functionality for user='admin'

    If the admin user types:
        - show_id : cat replies with the current tenant_id
        - t_id : changes the tenant_id of the admin  
    """
    user_message = cat.working_memory["user_message_json"]["text"]

    if( cat.user_id == 'admin'):
        
        if user_message.startswith("show_id") :
            if('tenant_id' in cat.user_data):
                fast_reply["output"] = f"The current Tenant Id is : { cat.user_data['tenant_id'] } ."
            else:
                fast_reply["output"] = 'No tenant_id has been assigned.'
        
        elif ( user_message.startswith("t_id=") ):
            inp_text = user_message.replace("t_id=",'')
            wannabe_id= inp_text.split() # splits whitespaces
            cat.user_data["tenant_id"] = wannabe_id[0]
            fast_reply["output"]= f"The tenant_id has been changed to : { cat.user_data['tenant_id'] }."

    return fast_reply




