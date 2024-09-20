from database.operations import create_customer,update_customer, delete_customer,get_customer_by_external_id

def sync_from_stripe(event):
    if event['type'] == 'customer.created':
        create_customer(event['data']['object']['name'], event['data']['object']['email'])
    elif event['type'] == 'customer.updated':
        customer = get_customer_by_external_id('stripe_id', event['data']['object']['id'])
        if customer:
            update_customer(customer[0], name=event['data']['object']['name'], email=event['data']['object']['email'])
    elif event['type'] == 'customer.deleted':
        customer = get_customer_by_external_id('stripe_id', event['data']['object']['id'])
        if customer:
            delete_customer(customer[0])