def get_tenant_name(env_type, db_type):
    return env_type.upper() + '_' + db_type.upper()
