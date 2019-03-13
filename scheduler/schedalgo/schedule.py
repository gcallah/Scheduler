import json
from collections import Counter


def sched(data):
    data_dict = json.loads(data)
    consumers = data_dict['consumers']
    resourses = data_dict['resources']

    sched = make_sched(consumers, resourses)
    unsched = get_unsched(consumers, sched)

    ret_val = {}
    ret_val['scheduled'] = sched
    ret_val['unscheduled'] = unsched
    return json.dumps(ret_val)


def make_sched(consumers, resources):

    scheduled_consumers = []
    counter_cnt = Counter([c['name'] for c in consumers])
    for consumer in consumers:
        for type_resource in consumer['type']:
            resource = resources[type_resource]
            for individ_resource in resource:
                scheduled_rnames = list(map(
                    lambda item: item['rname'], scheduled_consumers))
                scheduled_cnames = list(map(
                    lambda item: item['cname'], scheduled_consumers))

                tot_consumer_cnt = counter_cnt[consumer['name']]
                sched_consumer_cnt = scheduled_cnames.count(consumer["name"])

                if (individ_resource['name'] not in scheduled_rnames
                        and tot_consumer_cnt != sched_consumer_cnt):

                    for attribute in consumer['attributes']:
                        if attribute in individ_resource['attributes']:

                            ccap = consumer['attributes'][attribute]['value']
                            rcap = individ_resource['attributes'][attribute]['value']
                            if ccap <= rcap:
                                scheduled_consumer = {
                                    'rname': individ_resource['name'],
                                    'cname': consumer['name'],
                                    'course_capacity': ccap,
                                    'room_capacity': rcap,
                                }

                                scheduled_consumers.append(scheduled_consumer)

    return scheduled_consumers


def get_unsched(all_consumers, scheduled_consumers):
    unscheduled_consumers = []
    sched_consumer_names = [d['cname'] for d in scheduled_consumers]
    all_consumer_names = [d['name'] for d in all_consumers]

    for consumer in sched_consumer_names:
        try:
            all_consumer_names.remove(consumer)
        except ValueError:
            pass

    return all_consumer_names
