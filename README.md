# Cheshire Cat Tenancy Plugin

## What is the Cheshire Cat Tenancy Plugin
This plugin enables enhances the ability of the cat to perform as a Single-RAG to Multiple Users, by applying **Tenant IDs** to **Users** and **Uploaded documents/Memories**.
By applying said Tenant IDs we can 'filter' the which user will view which document, giving the Cat the ability to handle multiple separated sessions without generating output from unwanted uploaded Documents/Episodic Memories.

### Where to use

This plugin was created with the idea of :
* Having the cat function as **single RAG for multiple users** 
* Using the same cat on different working environments, thus the rise in need of document filtering in relation to tenant_id.
* Handling Shadow-Users/Guest-users.


  If for example we made an application with the cat that can be installed in many different environments ( for example : different companies/websites ), we would not have to create multiple different instances of the cat, but we could have a single cat handling all the traffic ( this was not tested under heavy traffic , so the behavior of the cat could vary ) by filtering the documents needed to be generated for each user in relation to the origin-environment
 
                   Cat
                   / \
                  /   \
                 /     \
               envA    envB
              / \         /\  
             /   \       /  \
            /     \     /    \
        user1  user2  user3   user4



### How it works:

**In order to use the plugin , cat.user_data form Stray Cat must be available, if not add these on the looking_glass/stray_cat.py:**

On the ```__init__```:
* self.__user_data= user_data 

On the end of the file add:
* ```py @property
    def user_data(self):
        return self.__user_data```

**The steps described above are changes that will be implemented on next versions, check if they are available before adding** 
The way the plugin works is by simply adding the prefix of **"tenant_id=< ID >\n"** to the user prompt. For example:

If the user prompt is :
* "What is the weather today?"

and the tenant_id is :
* "8765"

The final prompt would have to look like :
* "**tenant_id=8765\n**What is the weather today?"


The plugin afterwards will cut the prefix from the prompt , filter out the **tenant_id** and assign it to the cat.user_data as a field { "tenant_id" : **tenant_id** }


To apply a tenant_id to a document that will go to the RAG , you only need to be able to upload the under the tenant_id that you want.

There are two extra functionalities applied for the "admin" user that may help where if the admin user types:
* show_id : the cat prints the current tenant_id of the admin user
* t_id='**id**' : changes the current id of the admin user to **id**

These could help with uploading documents under the hood of a desired tenant_id.

### Plugin Contents:

The contents of the plugin are the bellow:
* **get_tenant_id** : a function that gets the tenant_id out of the user.data field.
* **before_rabbithole_insert_memory** : an overwritten hook that adds the user's tenant_id to the metadata of any memory that is to be uploaded.
* **before_cat_recalls_declarative_memories** : an overwritten hook that filters the user's tenant_id to the metadata of the document that is to be recalled.
* **before_cat_recalls_episodic_memories** : an overwritten hook that filters the user's **userID** to the metadata of memory that is to be reccalled.
* **before_cat_reads_message** : an overwritten hook that checks whether the input contains the "tenant_id=" in the start of the user's prompt.
* **agent_fast_reply** : an overwritten hook that checks whether the user's prompt contains the "t_id=" or "show_id".





## Notes

* In order to see if your documents have assigned tenant_ids assigned to them , go to the Memory Category of the Cat's GUI  and click 'Export Memories'. A .json file will be downloaded that contains information regarding the uploaded files , plus the metadata field that contains the 'tenant_id' field.

* Information regarding Cheshire Cat's hooks: https://cheshire-cat-ai.github.io/docs/plugins/hooks/

* Shadow Users in Cheshire Cat: https://cheshire-cat-ai.github.io/docs/production/auth/user-management/

