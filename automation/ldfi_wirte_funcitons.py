from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE



def clean_LDIF(input):
    return input.replace('\r\n ', '').replace('version: 1\r\n', '').replace('\n', '')


def write_ldif(c,strategy,f):
    if strategy == LDIF:
        f.write(clean_LDIF(c.response))
    else:
        pass
        f.write(str(c.result))
    f.write('\r\n')
