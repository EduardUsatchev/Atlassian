from csv import reader
import mysql.connector
from mysql.connector import Error

# from itertools import izip
errfile = open('err.log','w')
try:
    connection = mysql.connector.connect(host='********',
                                         database='********',
                                         user='********',
                                         password='********')
    # cursor = None
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute('USE jiradb;')
        cursor.execute('SELECT DATABASE();')
        dbname = cursor.fetchone()
        print("You're connected to database: ", dbname)
        old = open("/tmp/oldGroups.txt", "r")
        new = open("/tmp/newGroups.txt", "r")
        old_lower = open("/tmp/oldGroupsLower.txt", "r")
        new_lower = open("/tmp/newGroupsLower.txt", "r")
        # cursor = connection.cursor()
        old = [o.strip() for o in old]
        new = [o.strip() for o in new]
        old_lower = [o.strip() for o in old_lower]
        new_lower = [o.strip() for o in new_lower]

        for o, n, oL, nL in zip(old, new, old_lower, new_lower):
            cursor = connection.cursor()
            try:
                cursor.execute("update cwd_group set group_name = %s, lower_group_name = %s where group_name = %s and group_type = 'GROUP';",(n, nL, o))
            except Error as e:
                print("Error while updating cwd_group", e)
                errfile.write('[cwd_group] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute(
                    "update cwd_membership set parent_name = %s, lower_parent_name = %s where parent_name = %s and membership_type = 'GROUP_USER';",
                    (n, nL, o))
            except Error as e:
                print("Error while updating cwd_membership", e)
                errfile.write('[cwd_membership] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute(
                    "update notification set notif_parameter = %s where notif_parameter = %s and notif_type = 'Group_Dropdown';",
                    (n, o))
            except Error as e:
                print("Error while updating notification", e)
                errfile.write('[notification] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute(
                    "update schemeissuesecurities set sec_parameter = %s where sec_parameter = %s and sec_type = 'group';",
                    (n, o))
            except Error as e:
                print("Error while updating schemeissuesecurities", e)
                errfile.write('[schemeissuesecurities] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute(
                    "update schemepermissions set perm_parameter = %s where perm_parameter = %s and perm_type = 'group';",
                    (n, o))
            except Error as e:
                print("Error while updating schemepermissions", e)
                errfile.write('[schemepermissions] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update sharepermissions set param1 = %s where param1 = %s and sharetype = 'group';",(n, o))
            except Error as e:
                print("Error while updating sharepermissions2", e)
                errfile.write('[sharepermissions] Error while updating {} users to {} group\r\n'.format(n,o))
                continue

            try:
                cursor.execute("update filtersubscription set groupname = %s where groupname = %s;", (n, o))
            except Error as e:
                print("Error while updating filtersubscription", e)
                errfile.write('[filtersubscription] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update jiraaction set actionlevel = %s where actionlevel = %s;", (n, o))
            except Error as e:
                print("Error while updating jiraaction", e)
                errfile.write('[jiraaction] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update worklog set grouplevel = %s where grouplevel = %s;", (n, o))
            except Error as e:
                print("Error while updating jiraaction", e)
                errfile.write('[worklog] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update searchrequest set groupname = %s where groupname = %s;", (n, o))
            except Error as e:
                print("Error while updating searchrequest", e)
                errfile.write('[searchrequest] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update projectroleactor set roletypeparameter = %s where roletypeparameter = %s and roletype = 'atlassian-group-role-actor';",(n, o))
            except Error as e:
                print("Error while updating searchrequest", e)
                errfile.write('[projectroleactor] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update globalpermissionentry set group_id = %s where group_id = %s;", (n, o))
            except Error as e:
                print("Error while updating globalpermissionentry", e)
                errfile.write('[globalpermissionentry] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute("update licenserolesgroup  set group_id = %s where group_id = %s;", (nL, oL))
            except Error as e:
                print("Error while updating licenserolesgroup", e)
                errfile.write('[licenserolesgroup] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
            try:
                cursor.execute(
                    "update customfieldvalue set stringvalue = %s where stringvalue = %s and customfield in (select id from customfield where customfieldtypekey in ('com.atlassian.jira.plugin.system.customfieldtypes:multigrouppicker', 'com.atlassian.jira.plugin.system.customfieldtypes:grouppicker'));",
                    (n, o,))
            except Error as e:
                print("Error while updating customfieldvalue and customfield", e)
                errfile.write('[customfieldvalue] Error while updating {} users to {} group\r\n'.format(n,o))
                continue
           
	
    if(connection is not None):
        connection.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
errfile.close()
