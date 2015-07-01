# -*- coding: utf-8 -*-

import urllib
import json
from pprint import pprint as pp
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

    # just have vCPU data for on demand instances
    # spot instances data doesn't have vCPU info in the supplied file
    top_ten_on_demand = top_ten(on_demand_data)


    return render_template('index.html', top_ten_on_demand=top_ten_on_demand, name='Price per vCPU instances across all regions')

@mod.route('/ondemand', methods=['POST', 'GET'])
def on_demand():
    """On Demand data."""
    url = 'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js'
    on_demand_data = get_json_data(url)

    return render_template('pricespread.html', pricing_data=on_demand_data, name='EC2 On Demand Data')

@mod.route('/spot', methods=['POST', 'GET'])
def spot():
    """EC2 Spot data."""
    url = 'http://spot-price.s3.amazonaws.com/spot.js'
    spot_data = get_json_data(url)

    return render_template('pricespread.html', pricing_data=spot_data, name='EC2 Spot Data')


def top_ten(instance_data):
    """Return the top 10 price per vCPU instances across all regions."""

    top_ten_instances = []
    for instance in instance_data:
        for type in instance['types']:
            for region in type['region_data']:
                if region['vCPU']:
                    vCPU = int(region['vCPU'])
                    size = region['size']
                    price = float(region['price'])
                    price_per_vCPU = price/vCPU

                    if len(top_ten_instances) < 10:
                        if top_ten_instances and price < top_ten_instances[-1]['price']:
                            for index, tt_instance in enumerate(top_ten_instances):
                                if price < tt_instance['price']:
                                    top_ten_instances.insert(index, {'name': instance['name'], 'size': size, 'price': price})
                                    break
                        else:
                            top_ten_instances.append({'name': instance['name'], 'size': size, 'price': price})
                    else:
                        for index, tt_instance in enumerate(top_ten_instances):
                            if price < tt_instance['price']:
                                top_ten_instances.insert(index, {'name': instance['name'], 'size': size, 'price': price})
                                top_ten_instances.remove(top_ten_instances[-1])
                                break
    return top_ten_instances


def cheapest_region():
    """Return the cheapest region overall.

    Disregarding vCPU.
    """
    pass

def get_json_data(url):
    r1 = requests.get(url)
    if r1.status_code == 200:
        content = r1.content
        content = content[content.find('(')+1:-1]
        content = content.rstrip(')')
        decoded = demjson.decode(content)
        regions_data = []
        for region in decoded['config']['regions']:
            region_name = region['region']
            region_types  = []
            for r_type in region['instanceTypes']:
                region_type = r_type['type']
                region_sizes = []
                for r_size in r_type['sizes']:
                    region_size = r_size['size']
                    region_price = r_size['valueColumns'][0]['prices']['USD']
                    try:
                        region_vCPU = r_size['vCPU']
                    except KeyError, e:
                        region_vCPU = None
                    # if r_size['vCPU']:
                    #
                    # else:
                    # import ipdb; ipdb.set_trace()
                    # region_vCPU = r_size['vCPU']

                    region_sizes.append({'size': region_size, 'price': region_price, 'vCPU': region_vCPU})
                region_types.append({'type': region_type, 'region_data': region_sizes})
            regions_data.append({'name': region_name, 'types':region_types})
    return regions_data