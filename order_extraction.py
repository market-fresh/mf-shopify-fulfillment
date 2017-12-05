import shopify
import settings

#Simulated extracted order data
def simulate_extract_orders():
    columns = ['order_number', 'customer_name', 'delivery_day', 'delivery_time', 'address', 'zip_code', 'longitude', 'latitude']
    data = [(1567, 'Maggie Le', '05-12-2017', '9am-12nn', '8 Dover Rise  Heritage View 18-08 ', '138679', 103.783461, 1.304569), (1566, 'Fiona Yap', '05-12-2017', '9am-12nn', '941 Hougang Street 92 #06-01', '530941', 103.8791714, 1.3735857), (1565, 'Genevieve Lin', '05-12-2017', '9am-12nn', '19 WOODLANDS AVENUE 9 07-08 ', '738969', 103.784295, 1.447255), (1564, 'Connie Seah', '05-12-2017', '9am-12nn', '21 newton road 21 newton', '307954', None, None), (1563, 'Sheryl Yee', '05-12-2017', '12nn-3pm', 'Blk 215 Ang Mo Kio Ave 1 #09-907', '560215', 103.8415977, 1.3664997), (1562, 'Elisa Balaso', '05-12-2017', '9am-12nn', '50 Choa Chu Kang North 6 Yew Mei Green Condo / #15-08', '689574', 103.751334, 1.394469), (1561, 'HONG TAT NEO', '05-12-2017', 'Anytime (9am-6pm)', '35 Sommerville Road, #01-06 ', '358265', 103.8679479, 1.3450039), (1560, 'AGNES WONG', '06-12-2017', '9am-12nn', '11 Bukit Tunggal Road ', '309725', 103.838947, 1.320676), (1559, 'Quek Selina', '05-12-2017', '9am-12nn', '8 Butterworth Lane #01-11 ', '439423', 103.895453, 1.312019)]

    return columns, data

#Perform order extraction from Shopify store
def extract_orders():
    API_KEY = settings.API_KEY
    PASSWORD = settings.PASSWORD
    SHARED_SECRET = settings.SHARED_SECRET

    shop_url = "https://%s:%s@market-fresh.myshopify.com/admin" % (API_KEY, PASSWORD)
    shopify.ShopifyResource.set_site(shop_url)
    shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)
    shop = shopify.Shop.current()

    orders = shopify.Order.find()

    columns = ['order_number', 'customer_name', 'delivery_day', 'delivery_time', 'address', 'zip_code', 'longitude', 'latitude']
    data = list()

    for order in orders:
        customer_name = order.shipping_address.attributes['name']
        order_number = order.order_number
        delivery_day = order.note_attributes[0].attributes['value']
        delivery_time = order.note_attributes[1].attributes['value']
        shipping_address = order.shipping_address.attributes
        address = shipping_address['address1'] + ' ' + shipping_address['address2']
        zip_code = shipping_address['zip']
        longitude = shipping_address['longitude']
        latitude = shipping_address['latitude']

        data.append((order_number, customer_name, delivery_day, delivery_time, address, zip_code, longitude, latitude))

    return columns, data
