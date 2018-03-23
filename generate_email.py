import jinja2 as j2

def generate_email(data):
    conds = [
        data['bedrooms'] != 0,
        data['bath_total'] != 0,
        data['sqft'] != 0,
        data['avm'] != 0,
        data['avm_low'] != 0,
        data['avm_high'] != 0,
        data['street'] != ''
    ]

    if all(conds):
        data['avm'] = "${:,.0f}".format(data['avm'])
        data['avm_low'] = "${:,.0f}".format(data['avm_low'])
        data['avm_high'] = "${:,.0f}".format(data['avm_high'])

        data = {k:str(v) for k, v in data.items()}

        data['address'] = (
            data['street'] 
            + '<br>' 
            + data['city'] 
            + ", " + data['state'] 
            + " " 
            + data['zip']
        )

        template = j2.Template(open('email.html.jinja2').read())
        html = template.render(data=data)
        env = j2.Environment(autoescape=True).from_string(html)
        
        print(env.render(data=data))
        '''
        -*--for testing and saving to a static file--*-

        env.stream(data=data).dump("jinja_test.html")
        '''
generate_email(data)