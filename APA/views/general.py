# -*- coding: utf-8 -*-

import urllib
import json
import simplejson
import requests
import demjson
from flask import Blueprint, render_template_string, render_template, flash
from flask import Flask, request, Response, g, session, redirect, url_for
from config import config


mod = Blueprint('general', __name__)


@mod.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@mod.app_errorhandler(500)
def internal_error(error):
    # uncomment if using a database
    # db.session.rollback()
    return render_template('500.html'), 500


@mod.route('/', methods=['POST', 'GET'])
def index():
    """Index."""
    url1 = 'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js'
    url2 = 'http://spot-price.s3.amazonaws.com/spot.js'

    on_demand_data = get_json_data(url1)
    spot_data = get_json_data(url2)
    return render_template('index.html')

@mod.route('/ondemand', methods=['POST', 'GET'])
def on_demand():
    """On Demand data."""
    url = 'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js'
    on_demand_data = get_json_data(url)

    return render_template('index.html', pricing_data=on_demand_data, name='EC2 On Demand Data')

@mod.route('/spot', methods=['POST', 'GET'])
def spot():
    """EC2 Spot data."""
    url = 'http://spot-price.s3.amazonaws.com/spot.js'
    spot_data = get_json_data(url)

    return render_template('index.html', pricing_data=spot_data, name='EC2 Spot Data')

def get_json_data(url):
    r1 = requests.get(url)
    if r1.status_code == 200:
        content = r1.content
        content = content[content.find('(')+1:-1]
        content = content.rstrip(')')
        # import ipdb; ipdb.set_trace()
        decoded = demjson.decode(content)
        regions_data = []
        for region in decoded['config']['regions']:
            region_name = region['region']
            region_types  = []
            # regions_data.append(region_name)
            # d = {'name':region_name}
            for r_type in region['instanceTypes']:
                region_type = r_type['type']
                # region_types.append(region_type)
            #     d['type'] = region_type
                region_sizes = []
                for r_size in r_type['sizes']:
                    region_size = r_size['size']
                    region_price = r_size['valueColumns'][0]['prices']['USD']
                    region_sizes.append({'size': region_size, 'price': region_price})
                region_types.append({'type': region_type, 'region_data': region_sizes})
            regions_data.append({'name': region_name, 'types':region_types})

    return regions_data