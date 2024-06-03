from pystackql import StackQL
import os, time, schedule

def create_nic():
  """Insert into Network Interfaces."""
  query = """
  Insert into azure.network.interfaces
  (
    resourceGroupName,
    subscriptionId,
    networkInterfaceName,
    data__location,
    data__properties
  )
  select
    '%s',
    '%s',
    '%s',
    location,
    json_replace(json_remove(properties,
                                  '$.allowPort25Out',
                                  '$.auxiliarySku',
                                  '$.provisioningState',
                                  '$.resourceGuid',
                                  '$.macAddress',
                                  '$.vnetEncryptionSupported',
                                  '$.enableIPForwarding',
                                  '$.defaultOutboundAccess',
                                  '$.primary',
                                  '$.virtualMachine',
                                  '$.hostedWorkloads',
                                  '$.tapConfigurations',
                                  '$.nicType',
                                  '$.auxiliaryMode',
                                  '$.ipConfigurations[0].id',
                                  '$.ipConfigurations[0].etag',
                                  '$.ipConfigurations[0].type',
                                  '$.ipConfigurations[0].properties.provisioningState',
                                  '$.ipConfigurations[0].properties.privateIPAddress',
                                  '$.ipConfigurations[0].properties.privateIPAllocationMethod',
                                  '$.ipConfigurations[0].properties.primary',
                                  '$.ipConfigurations[0].properties.privateIPAddressVersion'
                                ),
                      '$.ipConfigurations[0].name',
                      'vmss-flex-vnet-nic01-defaultIpConfiguration'
                      )
  from
    azure.network.interfaces
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and networkInterfaceName = '%s'
  ;""" % (rg_name,subscription_id,nic_name,subscription_id,rg_name,vm['nic_name'])
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in create_nic for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {vm['nic_name']}: {e}")
  else:
    if res['message'] == success_message:
      global create_nic_ind
      create_nic_ind = True
      print(res)
    else:
      print(f"Error in create_nic for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {vm['nic_name']}: {res}")

def undo_create_nic():
  """Delete Network Interfaces."""
  query = """
  Delete from azure.network.interfaces
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and networkInterfaceName = '%s'
  ;""" % (rg_name,subscription_id,nic_name)
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in undo_create_nic for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {nic_name}: {e}")
  else:
    if res['message'] == success_message:
      print(res)
    else:
      print(f"Error in undo_create_nic for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {nic_name}: {res}")


def create_nic_dep():
  """Check if nic is deployed."""
  query = """
  select name
    from azure.network.interfaces
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and networkInterfaceName = '%s'
  ;""" % (subscription_id,rg_name,nic_name)
  try:
    res = stackql.execute(query)
  except Exception as e:
    print(f"Error in create_nic_dep for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {nic_name}: {e}")
  else:
    if nic_name == res[0]['name']:
      global create_nic_deployed
      create_nic_deployed = True
      print(res)
    else:
      print(f"Error in create_nic_dep for subscription_id = {subscription_id}, rg = {rg_name}, networkInterfaceName = {nic_name}: {res}")

def create_spot_vm():
  """Insert into Virtual Machines."""
  query = """
  Insert into azure.compute.virtual_machines
    (
    resourceGroupName,
    subscriptionId,
    vmName,
    data__location,
    data__properties
    )
  select
    '%s',
    '%s',
    '%s',
    location,
    json_set(
                  json_remove
                  (
                  properties,
                  '$.provisioningState',
                  '$.vmId',
                  '$.timeCreated',
                  '$.storageProfile.osDisk.managedDisk.id',
                  '$.osProfile.requireGuestProvisionSignal'
                  ),
                '$.storageProfile.osDisk.name',
                'vmss_OsDisk_1_' || '%s',
                '$.osProfile.computerName',
                'vmname-' || '%s',
                '$.osProfile.adminPassword',
                'Spotvm123@Apr2024',
                '$.networkProfile.networkInterfaces[0].id',
                '/subscriptions/' || '%s'|| '/resourceGroups/' || '%s' ||'/providers/Microsoft.Network/networkInterfaces/' || '%s',
                '$.priority',
                'Spot',
                '$.evictionPolicy',
                'Delete',
                '$.billingProfile.maxPrice',
                -1
                )
  from
    azure.compute.virtual_machines
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (rg_name,subscription_id,vm_name,vm_name,vm_name.replace('_','-'),subscription_id,rg_name,nic_name,subscription_id,rg_name,vm['vm_name'])
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in create_spot_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {e}")
  else:
    if res['message'] == success_message:
      global create_spot_vm_ind
      create_spot_vm_ind = True
      print(res)
    else:
      print(f"Error in create_spot_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {res}")

def undo_create_spot_vm():
  """Delete Virtual Machines."""
  query = """
  Delete from azure.compute.virtual_machines
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (subscription_id,rg_name,vm_name)
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in undo_create_spot_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {e}")
  else:
    if res['message'] == success_message:
      print(res)
    else:
      print(f"Error in create_spot_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {res}")

def create_spot_vm_dep():
  """Check if spot vm is deployed."""
  query = """
  select name
    from azure.compute.virtual_machines
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (subscription_id,rg_name,vm_name)
  try:
    res = stackql.execute(query)
  except Exception as e:
    print(f"Error in create_spot_vm_dep for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {e}")
  else:
    if vm_name == res[0]['name']:
      global create_spot_vm_deployed
      create_spot_vm_deployed = True
      print(res)
    else:
      print(f"Error in create_spot_vm_dep for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {res}")

def create_vm_extension():
  """Create vm Extension."""
  query = """
  Insert into azure.compute.virtual_machine_extensions
  (
    resourceGroupName,
    subscriptionId,
    vmExtensionName,
    vmName,
    data__location,
    data__properties
  )
  select
    '%s',
    '%s',
    name,
    '%s',
    location,
    json_remove(properties,'$.provisioningState')
  from
    azure.compute.virtual_machine_extensions
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (rg_name,subscription_id,vm_name,subscription_id,rg_name,vm['vm_name'])
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in create_vm_extension for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {e}")
  else:
    if res['message'] == success_message:
      global create_vm_extension_ind
      create_vm_extension_ind = True
      print(res)
    else:
      print(f"Error in create_vm_extension for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {res}")

def undo_create_vm_extension():
  """Delete vm Extension."""
  query = """
  Delete from azure.compute.virtual_machine_extensions
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  and vmExtensionName in (
    select name
    from
        azure.compute.virtual_machine_extensions
    where subscriptionId = '%s'
    and resourceGroupName = '%s'
    and vmName = '%s'       
    )
  ;""" % (subscription_id,rg_name,vm_name,subscription_id,rg_name,vm_name)
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in undo_create_vm_extension for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {e}")
  else:
    if res['message'] == success_message:
      print(res)
    else:
      print(f"Error in undo_create_vm_extension for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {e}")

def create_vm_extension_dep():
  """Check if vm Extension is deployed."""
  query = """
  select name
  from
    azure.compute.virtual_machine_extensions
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (subscription_id,rg_name,vm_name)
  try:
    res = stackql.execute(query)
  except Exception as e:
    print(f"Error in create_vm_extension_dep for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {e}")
  else:
    if res[0]['name']: 
      global create_vm_extension_deployed
      create_vm_extension_deployed = True
      print(res)
    else:
      print(f"Error in create_vm_extension_dep for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm_name}: {res}")

def delete_OD_vm():
  """Delete from Virtual Machines."""
  query = """
  Delete
    from azure.compute.virtual_machines
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and vmName = '%s'
  ;""" % (subscription_id,rg_name,vm['vm_name'])
  try:
    res = stackql.executeStmt(query)
  except Exception as e:
    print(f"Error in delete_OD_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {e}")
  else:
    if res['message'] == success_message:
      global delete_OD_vm_ind
      delete_OD_vm_ind = True
      print(res)
    else:
      print(f"Error in delete_OD_vm for subscription_id = {subscription_id}, rg = {rg_name}, vmName = {vm['vm_name']}: {res}")   

def process_for_each_rg():
  query = """
  select
          a.name as vmss_name,
          c.name as vm_name,
          SPLIT_PART(json_extract(c.properties,'$.networkProfile.networkInterfaces[0].id'), '/', -1)as nic_name
  from
    azure.compute.virtual_machine_scale_sets a
    inner join  azure.compute.virtual_machine_scale_set_vms b
      on a.name = b.virtualMachineScaleSetName
    inner join  azure.compute.virtual_machines c
      on b.name = c.name
  where subscriptionId = '%s'
  and resourceGroupName = '%s'
  and json_extract(c.properties,'$.priority') is null 
  %s 
  order by vmss_name, vm_name
  ;""" % (subscription_id,rg_name,query2)
  try:
    vms = stackql.execute(query)
  except Exception as e:
    print(f"Error in process_for_each_rg for subscription_id = {subscription_id}, rg = {rg_name} : {e}")
  else:
    print(vms)
    if not vms:
      print(f"No OD VMs to replace for Subscription_id = {subscription_id}, rg = {rg_name} ")
    else:
      global vm, i, create_nic_ind, create_spot_vm_ind, create_vm_extension_ind, delete_OD_vm_ind
      global create_nic_deployed, create_spot_vm_deployed, create_vm_extension_deployed

      for i, vm in enumerate(vms):

        #Reset the flag for every iteration
        create_nic_ind, create_spot_vm_ind, create_vm_extension_ind, delete_OD_vm_ind = False, False, False, False
        create_nic_deployed, create_spot_vm_deployed, create_vm_extension_deployed = False, False, False

        #skip the last vm in the vmss so there is atleast one OD VM
        if i == len(vms) -1:
          break
        elif (vms[i]['vmss_name'] != vms[i+1]['vmss_name']):
          continue

        global vm_name, nic_name
        vm_name = vm['vmss_name'] + '-manual-' + vm['vm_name']
        nic_name = vm_name + '-nic'

#1. create nic
        create_nic()
        #if error continue to next iteration
        if not create_nic_ind:
          continue

        for i in range(5):
          time.sleep(2)
          create_nic_dep()
          if create_nic_deployed:
            break

        #if not deployed continue to next iteration       
        if not create_nic_deployed:
          continue  

#2. create spot_vm 
        create_spot_vm()
        #if error continue to next iteration
        if not create_spot_vm_ind:
          undo_create_nic()
          continue

        for i in range(5):
          time.sleep(2)
          create_spot_vm_dep()
          if create_spot_vm_deployed:
            break

        #if not deployed continue to next iteration       
        if not create_spot_vm_deployed:
          undo_create_nic()
          continue  

#3. create vm_extension
        create_vm_extension()
        #if error continue to next iteration
        if not create_vm_extension_ind:
          undo_create_nic()
          undo_create_spot_vm()          
          continue

        for i in range(5):
          time.sleep(2)
          create_vm_extension_dep()
          if create_vm_extension_deployed:
            break

        #if not deployed continue to next iteration       
        if not create_vm_extension_deployed:
          undo_create_nic()
          undo_create_spot_vm()          
          continue  

#4. Delete OD VM
        delete_OD_vm()
        #if error continue to next iteration
        if not delete_OD_vm_ind:
          undo_create_nic()
          undo_create_spot_vm()  
          undo_create_vm_extension()        

def get_resource_group():
  query = """
  select name as rg_name
  from
    azure.resources.resource_groups
  where subscriptionId = '%s'
  order by rg_name
  ;""" % (subscription_id)
  try:
    rgs = stackql.execute(query)
  except Exception as e:
    print(f"Error in getting rg_name for subscription_id = {subscription_id} : {e}")
  else:
    for rg in rgs:
      print(rg)
      global rg_name
      rg_name = rg['rg_name']
      process_for_each_rg()

# start of main flow

stackql = StackQL()
stackql_query = "REGISTRY PULL azure"
result = stackql.executeStmt(stackql_query)
print(result)
success_message = 'The operation was despatched successfully\n'

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
convert_to_spot = os.environ["CONVERT_TO_SPOT"]
print(convert_to_spot)  
 
match convert_to_spot:
  case 'ALL':
    query2 = ''
  case 'TRUE':
    query2 = """ and JSON_EXTRACT(a.tags,'$.convert_to_spot') = 'True' """
  case 'FALSE':
    query2 = """ and JSON_EXTRACT(a.tags,'$.convert_to_spot') is null """
  case _:
    print(f"Unacceptable tag value for convert_to_spot: {convert_to_spot}")
    exit()

# schedule the task to run every hour
schedule.every().hour.at(":01").do(get_resource_group) 
#schedule.every(10).minutes.do(get_resource_group) 

# run all jobs now
#schedule.run_all()

while True:
  schedule.run_pending()
  time.sleep(1)
